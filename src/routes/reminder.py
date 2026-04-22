from fastapi import APIRouter
from src.models.schemas import ReminderRequest, ReminderResponse
from src.services.google_calendar import calendar_service

router = APIRouter()


@router.post("/reminder", response_model=ReminderResponse)
async def create_reminder(request: ReminderRequest):
    """
    Generates a Google Calendar event link for Election Day reminders.
    """
    return await calendar_service.create_election_reminder()
