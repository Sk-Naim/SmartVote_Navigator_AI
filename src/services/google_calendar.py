import urllib.parse
from datetime import datetime, timedelta
from src.models.schemas import ReminderResponse

class GoogleCalendarService:
    async def create_election_reminder(self) -> ReminderResponse:
        """
        Mock implementation of Google Calendar Event generation.
        """
        election_date = datetime.utcnow() + timedelta(days=30)
        date_str = election_date.strftime("%Y%M%d")
        
        base_url = "https://calendar.google.com/calendar/r/eventedit?"
        params = {
            "text": "Election Day Reminder",
            "dates": f"{date_str}/{date_str}",
            "details": "Remember to cast your vote! Brought to you by SmartVote Navigator.",
            "location": "Your Polling Station"
        }
        
        link = base_url + urllib.parse.urlencode(params)
        return ReminderResponse(status="success", calendar_link=link)

calendar_service = GoogleCalendarService()
