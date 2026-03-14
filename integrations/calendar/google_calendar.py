"""
Google Calendar integration.
Syncs AI-generated schedules to the user's Google Calendar.
Requires: google-auth, google-api-python-client

Set GOOGLE_CALENDAR_ENABLED=true in your .env to activate.
Without it, all calendar functions raise a clear RuntimeError instead of
crashing silently or opening a browser on a headless server.
"""
from datetime import datetime
import os

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
TOKEN_FILE = "token.json"
CALENDAR_ENABLED = os.getenv("GOOGLE_CALENDAR_ENABLED", "false").lower() == "true"


def _check_enabled():
    if not CALENDAR_ENABLED:
        raise RuntimeError(
            "Google Calendar integration is disabled. "
            "Set GOOGLE_CALENDAR_ENABLED=true in your .env and provide credentials.json."
        )


def get_calendar_service():
    """Authenticate and return a Google Calendar service object."""
    _check_enabled()

    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if not os.path.exists(CREDENTIALS_FILE):
            raise FileNotFoundError(
                f"Google credentials file not found: {CREDENTIALS_FILE}. "
                "Download it from Google Cloud Console."
            )
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        # run_local_server opens a browser — only safe on a local dev machine.
        # On a headless server, use flow.run_console() or a service account instead.
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def create_calendar_event(task_title: str, start_time: datetime, end_time: datetime, description: str = "") -> dict:
    """
    Create a Google Calendar event for a scheduled task.

    Args:
        task_title:  Title of the task
        start_time:  Start datetime (UTC)
        end_time:    End datetime (UTC)
        description: Optional task description

    Returns:
        Created event dict
    """
    _check_enabled()
    service = get_calendar_service()

    event = {
        "summary": f"[Momentum AI] {task_title}",
        "description": description,
        "start": {"dateTime": start_time.isoformat() + "Z", "timeZone": "UTC"},
        "end":   {"dateTime": end_time.isoformat() + "Z", "timeZone": "UTC"},
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "popup", "minutes": 15}
            ]
        }
    }

    created = service.events().insert(calendarId="primary", body=event).execute()
    return created


def sync_schedule_to_calendar(schedule_slots: list) -> list:
    """
    Sync an entire schedule (list of slots) to Google Calendar.

    Args:
        schedule_slots: List of dicts with task_id, title, start_time, end_time

    Returns:
        List of created event IDs
    """
    _check_enabled()
    event_ids = []
    for slot in schedule_slots:
        event = create_calendar_event(
            task_title=slot.get("title", "Scheduled Task"),
            start_time=slot["start_time"],
            end_time=slot["end_time"],
            description=slot.get("description", "")
        )
        event_ids.append(event.get("id"))
    return event_ids