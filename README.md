# VenueFlow — AI-Powered Smart Stadium Companion

VenueFlow is a high-performance, real-time crowd management solution designed for large-scale physical events like IPL matches. It leverages **Google Cloud Platform** and **Gemini AI** to provide fans with live insights and predictive recommendations, ensuring a seamless stadium experience.

## 🚀 Technology Stack
- **Frontend**: React (Vite), Glassmorphism UI, WebSockets (wss://).
- **Backend**: FastAPI (Python 3.11+), Uvicorn, Asynchronous I/O.
- **AI**: Google Gemini 1.5 Pro (via `google-generativeai`).
- **Infrastructure**: Google Cloud Run (Serverless), CI/CD via GitHub Actions.
- **Monitoring**: Google Cloud Logging & Health Checks.

## 🛠️ Key Features & Implementation
### 1. Real-Time Crowd Heatmap
We implemented a custom simulation engine (`crowd_simulator.py`) that uses Perlin-noise-inspired fluctuations to model realistic crowd density across gates, seating blocks, food courts, and restrooms. Data is streamed to the frontend via persistent WebSockets with a heartbeat mechanism to ensure 100% connectivity on Google Cloud Run.

### 2. Gemini-Powered MatchDay Assistant
The "MatchDay AI" uses a specialized prompt engineering layer to analyze live stadium occupancy data. It provides fans with:
- **Smart Routing**: Recommending the food court with the shortest wait time.
- **Crowd Alerts**: Predictive warnings before zones hit 90% capacity.
- **Contextual Support**: Answering match-related questions using real-time simulation state.

### 3. Production Hardening
- **Security**: Content Security Policy (CSP) headers, CORS protection, and secure WebSocket protocols.
- **Efficiency**: Lru-cache for API responses, GZip compression for static assets, and lazy-loading for React components.
- **Testing**: Automated unit tests for simulation logic and API endpoints.

## ☁️ Google Cloud Integration
- **Cloud Run**: Scales to zero for cost-efficiency, handles concurrent WebSocket connections.
- **Gemini AI SDK**: Direct integration for real-time analysis.
- **Cloud Logging**: Integrated structured logging for production debugging.

---
*Created for the Google Cloud x Hack2skill Hackathon.*
