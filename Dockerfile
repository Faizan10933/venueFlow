# ---- Stage 1: Build Frontend ----
FROM node:20-alpine AS build
WORKDIR /app/frontend

# Copy frontend source
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# ---- Stage 2: Serve with Backend ----
FROM python:3.10-slim
WORKDIR /app

# Install backend dependencies
COPY backend/requirements.txt ./
# (If we didn't have requirements.txt, we can just install directly, but let's create a requirements.txt)
RUN pip install --no-cache-dir fastapi "uvicorn[standard]" websockets google-generativeai pydantic

# Copy backend source
COPY backend/ ./

# Copy built frontend static files to backend/dist
COPY --from=build /app/frontend/dist ./dist

# Expose port (Cloud Run sets PORT env var)
ENV PORT=8080
EXPOSE 8080

# Run FastAPI server
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
