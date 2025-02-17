from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class CreateGoogleEventRequest(BaseModel):
    summary: str
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    attendees: List[EmailStr]

class AddAttendeeToEventRequest(BaseModel):
    event_id: str
    email: EmailStr