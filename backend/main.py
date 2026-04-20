import asyncio
import json
import time
import os
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from stadium_data import STADIUM_INFO, ZONES, FOOD_MENU, MATCH_TIMELINE
from crowd_simulator import CrowdSimulator
from gemini_service import GeminiService

app = FastAPI(title="VenueFlow API", version="1.0.0")

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
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
def get_stadium_info():
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
def get_recommendation(zone_type: str):
    """Get recommendation for best zone of a type (food_court, restroom, gate)."""
    return simulator.get_zone_recommendation(zone_type)


class ChatRequest(BaseModel):
    message: str


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Chat with MatchDay AI assistant."""
    live_data = simulator.tick()
    response = await gemini.chat(request.message, live_data)
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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
