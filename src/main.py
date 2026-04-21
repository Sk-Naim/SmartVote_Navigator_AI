import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.routes import chat, locations, reminder

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

app.include_router(chat.router, tags=["Chat"])
app.include_router(locations.router, tags=["Locations"])
app.include_router(reminder.router, tags=["Reminders"])

# Mount frontend
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
os.makedirs(frontend_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.get("/health")
async def health_check():
    """Liveness probe for Google Cloud Run."""
    return {"status": "healthy"}
