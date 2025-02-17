from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import json
from fastapi import HTTPException, status

class GoogleCalendarService:
    def __init__(self):
        self.creds = None
        self.load_token()

    def load_token(self):
        if os.path.exists('token.json'):
            with open('token.json', 'r') as token:
                self.creds = Credentials.from_authorized_user_file(token)

    def save_token(self, creds):
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    def get_auth_url(self):
        flow = Flow.from_client_secrets_file(
            'credentials.json',
            scopes=['https://www.googleapis.com/auth/calendar'],
            redirect_uri='http://localhost:8000/google/callback'
        )
        auth_url, _ = flow.authorization_url(prompt='consent')
        return auth_url

    def handle_oauth_callback(self, code: str):
        flow = Flow.from_client_secrets_file(
            'credentials.json',
            scopes=['https://www.googleapis.com/auth/calendar'],
            redirect_uri='http://localhost:8000/google/callback'
        )
        flow.fetch_token(code=code)
        self.creds = flow.credentials
        self.save_token(self.creds)

    def create_event(self, summary: str, start_time: datetime, end_time: datetime, attendees: List[str], description: Optional[str] = None):
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

        service = build('calendar', 'v3', credentials=self.creds)
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC',
            },
            'attendees': [{'email': email} for email in attendees],
            'conferenceData': {
                'createRequest': {
                    'requestId': 'sample123',
                    'conferenceSolutionKey': {'type': 'hangoutsMeet'},
                },
            },
        }
        event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
        return {
            'id': event['id'],
            'url': event['hangoutLink'],
            'data': event
        }

    def add_attendee_to_event(self, event_id: str, attendee_email: str):
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

        service = build('calendar', 'v3', credentials=self.creds)
        event = service.events().get(calendarId='primary', eventId=event_id).execute()
        attendees = event.get('attendees', [])
        attendees.append({'email': attendee_email})
        event['attendees'] = attendees
        updated_event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
        return {
            'id': updated_event['id'],
            'url': updated_event['hangoutLink'],
        }