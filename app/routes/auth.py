from fastapi import APIRouter, Depends
from app.services.google_calendar import GoogleCalendarService

router = APIRouter()
google_service = GoogleCalendarService()

@router.get("/google/redirect")
async def redirect_to_google():
    auth_url = google_service.get_auth_url()
    return {"auth_url": auth_url}

@router.get("/google/callback")
async def handle_google_callback(code: str):
    google_service.handle_oauth_callback(code)
    return {"message": "Google account connected successfully!"}