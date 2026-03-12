"""
Email notification service using SMTP.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")


def send_email(to: str, subject: str, body: str, html: bool = False):
    """
    Send an email notification.

    Args:
        to:      Recipient email address
        subject: Email subject line
        body:    Email body (plain text or HTML)
        html:    Set True if body is HTML
    """
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to

    part = MIMEText(body, "html" if html else "plain")
    msg.attach(part)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, to, msg.as_string())


def send_task_reminder(to: str, task_title: str, deadline: str):
    subject = f"[Momentum AI] Reminder: {task_title}"
    body = f"""
    <h2>Task Reminder</h2>
    <p>Your task <strong>{task_title}</strong> is due on <strong>{deadline}</strong>.</p>
    <p>Log in to Momentum AI to update your progress.</p>
    """
    send_email(to, subject, body, html=True)


def send_project_invite(to: str, project_title: str, role: str, invited_by: str):
    subject = f"[Momentum AI] You've been invited to {project_title}"
    body = f"""
    <h2>Project Invitation</h2>
    <p><strong>{invited_by}</strong> has added you to the project <strong>{project_title}</strong>
    as a <strong>{role}</strong>.</p>
    <p>Log in to Momentum AI to view your tasks.</p>
    """
    send_email(to, subject, body, html=True)


def send_survival_score_alert(to: str, project_title: str, score: float):
    subject = f"[Momentum AI] Survival Score Alert: {project_title}"
    color = "#e74c3c" if score < 50 else "#f39c12" if score < 70 else "#27ae60"
    body = f"""
    <h2>Idea Survival Score Update</h2>
    <p>Project: <strong>{project_title}</strong></p>
    <p>Survival Score: <strong style="color:{color}">{score}/100</strong></p>
    <p>{"Your score is low. Consider reducing scope or adding collaborators." if score < 50 else "Your project is on track!"}</p>
    """
    send_email(to, subject, body, html=True)
