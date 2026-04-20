import asyncio
import json
import time
import os
import re
from typing import List, Dict, Any, Optional
from functools import lru_cache
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel, Field

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from stadium_data import STADIUM_INFO, ZONES, FOOD_MENU, MATCH_TIMELINE
from crowd_simulator import CrowdSimulator
from gemini_service import GeminiService

app = FastAPI(title="VenueFlow API", version="1.0.0")

# Rate Limiter setup
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Middleware: GZip Compression for Efficiency
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Security Middleware: Basic Security Headers
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Strict CSP to prevent unauthorized scripts, styles, or data exfiltration
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://apis.google.com https://www.gstatic.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https://www.google.com https://lh3.googleusercontent.com; "
            "connect-src 'self' ws: wss: https://*.googleapis.com https://*.firebaseio.com; "
            "frame-src 'self' https://www.google.com https://*.firebaseapp.com; "
            "object-src 'none'; "
            "base-uri 'self';"
        )
        response.headers["Content-Security-Policy"] = csp
        return response

app.add_middleware(SecurityHeadersMiddleware)

# Security: Tighten CORS to known origins (local + Cloud Run dynamic)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://localhost:8000",
        "https://venueflow.promptwars.in" # Example production origin
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Global instances
simulator = CrowdSimulator()
gemini = GeminiService()
connected_clients: List[WebSocket] = []

# Background task reference
background_task = None


# ─── REST Endpoints ───────────────────────────────────────────────

@app.get("/api/stadium")
@limiter.limit("60/minute")
@lru_cache(maxsize=1)
def get_stadium_info(request: Request) -> Dict[str, Any]:
    """Get static stadium information."""
    return {
        "info": STADIUM_INFO,
        "zones": ZONES,
        "food_menu": FOOD_MENU,
        "match_timeline": MATCH_TIMELINE,
    }


@app.get("/api/state")
def get_current_state():
    """Get current simulation state (snapshot)."""
    return simulator.tick()


@app.get("/api/recommend/{zone_type}")
@limiter.limit("60/minute")
def get_recommendation(request: Request, zone_type: str) -> Dict[str, Any]:
    """Get recommendation for best zone of a type (food_court, restroom, gate)."""
    return simulator.get_zone_recommendation(zone_type)


class ChatRequest(BaseModel):
    message: str = Field(
        ..., 
        min_length=1, 
        max_length=500, 
        description="The chat message from the user",
        # Pattern ensures no crazy control characters, but allows standard punctuation and multiple languages
        pattern=r"^[\w\s\.,\?!\-'\":;\(\)\[\]{}@#%&\*+=\/<>\\|\n\r\t\u0900-\u097F]+$"
    )
    language: str = Field(default="English", max_length=50)


@app.post("/api/chat")
@limiter.limit("10/minute")
async def chat_endpoint(request: Request, body: ChatRequest) -> Dict[str, str]:
    """Chat with MatchDay AI assistant."""
    live_data = simulator.tick()
    response = await gemini.chat(body.message, live_data, body.language)
    return {"response": response, "sim_time": live_data["sim_time"]["display"]}


# ─── WebSocket for real-time updates ─────────────────────────────

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Real-time crowd data via WebSocket."""
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        # Send initial state
        state = simulator.tick()
        await websocket.send_json(state)

        # Keep connection alive, listen for pings
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=0.5)
                # Handle any client messages if needed
                if data == "ping":
                    await websocket.send_text("pong")
            except asyncio.TimeoutError:
                pass
            except WebSocketDisconnect:
                break
    except WebSocketDisconnect:
        pass
    finally:
        if websocket in connected_clients:
            connected_clients.remove(websocket)


async def broadcast_state():
    """Broadcast simulation state to all connected WebSocket clients."""
    while True:
        await asyncio.sleep(2)  # Update every 2 seconds
        if connected_clients:
            state = simulator.tick()
            dead_clients = []
            for client in connected_clients:
                try:
                    await client.send_json(state)
                except Exception:
                    dead_clients.append(client)
            for client in dead_clients:
                if client in connected_clients:
                    connected_clients.remove(client)
        else:
            # Still tick even without clients to keep simulation running
            simulator.tick()


@app.on_event("startup")
async def startup_event():
    """Start background simulation broadcast."""
    global background_task
    background_task = asyncio.create_task(broadcast_state())


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up background tasks."""
    global background_task
    if background_task:
        background_task.cancel()


# ─── Static Files & Catch-All for React Router ────────────────────

# Mount static files
if os.path.exists("dist"):
    app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")

    # Catch-all route to serve index.html for client-side routing
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Serve favicon or other top-level files if they exist
        if full_path and os.path.exists(os.path.join("dist", full_path)):
            return FileResponse(os.path.join("dist", full_path))
        # Otherwise serve index.html for React Router
        return FileResponse(os.path.join("dist", "index.html"))

# ─── Run ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    # Respect PORT environment variable for Cloud Run
    port = int(os.environ.get("PORT", 8000))
    # Disable reload in production for efficiency
    is_dev = os.environ.get("ENVIRONMENT", "development") == "development"
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=is_dev)
