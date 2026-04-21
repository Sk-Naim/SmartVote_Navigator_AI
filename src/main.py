from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

@app.get("/health")
async def health_check():
    """Liveness probe for Google Cloud Run."""
    return {"status": "healthy"}
