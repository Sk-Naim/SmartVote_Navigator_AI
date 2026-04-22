import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Dict
from src.routes import chat, locations, reminder

# Configure Enterprise Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SmartVote Navigator AI Cloud API",
    description="A production-ready REST API for assisting users in the voting process.",
    version="1.0.0"
)

# Optmizing CORS for Cloud Run deployment environments.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add GZip Compression for API Efficiency Optimization
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(chat.router, tags=["Chat"])
app.include_router(locations.router, tags=["Locations"])
app.include_router(reminder.router, tags=["Reminders"])

# Mount frontend
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
os.makedirs(frontend_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
async def serve_frontend() -> FileResponse:
    """Serves the main HTML interface."""
    logger.info("Serving frontend interface.")
    return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Liveness probe for Google Cloud Run ensuring deployment stability."""
    logger.info("Health check endpoint pinged.")
    return {"status": "healthy"}
