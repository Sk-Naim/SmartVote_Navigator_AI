"""
Data models and schemas for the FastAPI application.
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Schema for incoming chat messages."""
    session_id: str
    message: str


class ChatHistoryResponse(BaseModel):
    """Schema for chat history retrieval."""
    history: List[Dict[str, Any]]


class ChatResponse(BaseModel):
    """Schema for outgoing chat responses."""
    session_id: str
    reply: str
    triggered_action: Optional[str] = None
    action_data: Optional[Dict[str, Any]] = None


class FlowTriggerRequest(BaseModel):
    """Schema for triggering specific chat flows."""
    session_id: str


class LocationRequest(BaseModel):
    zip_code: str


class LocationResponse(BaseModel):
    """Schema for returning polling station locations."""
    address: str
    maps_url: str
    distance_miles: float


class ReminderRequest(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None


class ReminderResponse(BaseModel):
    """Schema for calendar reminder links."""
    status: str
    calendar_link: str
