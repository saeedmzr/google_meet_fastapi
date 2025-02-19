from fastapi import APIRouter, Depends, HTTPException
from app.services.google_calendar import GoogleCalendarService
from app.schemas.event import CreateGoogleEventRequest, AddAttendeeToEventRequest
from app.database.session import SessionLocal
from app.models.meeting import Meeting
from app.models.attendee import Attendee

router = APIRouter()
google_service = GoogleCalendarService()

@router.post("/google/event")
async def create_event(request: CreateGoogleEventRequest):
    db = SessionLocal()
    try:
        event_details = google_service.create_event(
            request.summary,
            request.start_time,
            request.end_time,
            request.attendees,
            request.description
        )
        # meeting = Meeting(
        #     requested_data=request.dict(),
        #     response_data=event_details,
        #     meeting_url=event_details['url'],
        #     event_id=event_details['id']
        # )
        # db.add(meeting)
        # db.commit()
        # for attendee in request.attendees:
        #     db_attendee = Attendee(email=attendee, meeting_id=meeting.id)
        #     db.add(db_attendee)
        # db.commit()
        return event_details
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.post("/google/event/add-attendee")
async def add_attendee_to_event(request: AddAttendeeToEventRequest):
    db = SessionLocal()
    try:
        event_details = google_service.add_attendee_to_event(request.event_id, request.email)
        meeting = db.query(Meeting).filter(Meeting.event_id == request.event_id).first()
        if not meeting:
            raise HTTPException(status_code=404, detail="Event not found")
        db_attendee = Attendee(email=request.email, meeting_id=meeting.id)
        db.add(db_attendee)
        db.commit()
        return event_details
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()