"""
SMS notification service using Twilio.
Install: pip install twilio
"""
import os
from twilio.rest import Client

TWILIO_SID   = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM  = os.getenv("TWILIO_FROM_NUMBER", "")


def send_sms(to: str, message: str):
    """
    Send an SMS via Twilio.

    Args:
        to:      Recipient phone number in E.164 format (+1234567890)
        message: SMS body text
    """
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    client.messages.create(body=message, from_=TWILIO_FROM, to=to)


def send_task_sms_reminder(to: str, task_title: str, deadline: str):
    message = f"[Momentum AI] Reminder: '{task_title}' is due {deadline}. Log in to update your progress."
    send_sms(to, message)


def send_schedule_ready_sms(to: str, project_title: str):
    message = f"[Momentum AI] Your RL-generated schedule for '{project_title}' is ready. Check the app."
    send_sms(to, message)
