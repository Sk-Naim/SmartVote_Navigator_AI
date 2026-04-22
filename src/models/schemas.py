from pydantic import BaseModel
from typing import Optional, Dict, Any


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    triggered_action: Optional[str] = None
    action_data: Optional[Dict[str, Any]] = None


class LocationRequest(BaseModel):
    zip_code: str


class LocationResponse(BaseModel):
    address: str
    maps_url: str
    distance_miles: float


class ReminderRequest(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None


class ReminderResponse(BaseModel):
    status: str
    calendar_link: str
