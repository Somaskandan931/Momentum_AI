"""
Command parser — converts transcribed text into structured system actions.
"""
import re
from datetime import datetime, timedelta


COMMAND_PATTERNS = {
    "add_task":       r"add task[:\-]?\s*(.+?)(?:\s+(?:due|by|tomorrow|today|on)\s+(.+))?$",
    "show_schedule":  r"show\s+(today'?s?\s+)?schedule",
    "move_task":      r"move\s+(.+?)\s+to\s+(.+)",
    "complete_task":  r"(?:mark|complete|finish)\s+(.+?)\s+(?:as\s+)?(?:done|complete|finished)",
    "list_tasks":     r"(?:show|list|get)\s+(?:my\s+)?tasks",
    "delay_task":     r"delay\s+(.+?)\s+(?:by\s+)?(.+)",
}


def parse_command(text: str) -> dict:
    """
    Parse a natural language voice command into a structured action.

    Args:
        text: Transcribed speech text

    Returns:
        Dict with 'action' and relevant parameters, or 'unknown' action
    """
    text = text.strip().lower()

    # Add task
    m = re.search(COMMAND_PATTERNS["add_task"], text, re.IGNORECASE)
    if m:
        task_title = m.group(1).strip()
        due_str = m.group(2).strip() if m.group(2) else None
        deadline = _parse_date(due_str) if due_str else None
        return {
            "action": "add_task",
            "title": task_title,
            "deadline": deadline.isoformat() if deadline else None
        }

    # Show schedule
    if re.search(COMMAND_PATTERNS["show_schedule"], text, re.IGNORECASE):
        return {"action": "show_schedule", "date": datetime.utcnow().date().isoformat()}

    # Move task
    m = re.search(COMMAND_PATTERNS["move_task"], text, re.IGNORECASE)
    if m:
        return {
            "action": "move_task",
            "task": m.group(1).strip(),
            "to": m.group(2).strip()
        }

    # Complete task
    m = re.search(COMMAND_PATTERNS["complete_task"], text, re.IGNORECASE)
    if m:
        return {"action": "complete_task", "task": m.group(1).strip()}

    # List tasks
    if re.search(COMMAND_PATTERNS["list_tasks"], text, re.IGNORECASE):
        return {"action": "list_tasks"}

    # Delay task
    m = re.search(COMMAND_PATTERNS["delay_task"], text, re.IGNORECASE)
    if m:
        return {
            "action": "delay_task",
            "task": m.group(1).strip(),
            "by": m.group(2).strip()
        }

    return {"action": "unknown", "raw_text": text}


def _parse_date(date_str: str) -> datetime:
    """Parse informal date strings into datetime objects."""
    today = datetime.utcnow().replace(hour=9, minute=0, second=0, microsecond=0)
    date_str = date_str.lower().strip()

    if "tomorrow" in date_str:
        return today + timedelta(days=1)
    if "today" in date_str:
        return today
    if "evening" in date_str:
        return today.replace(hour=18)
    if "morning" in date_str:
        return today.replace(hour=9)
    if "afternoon" in date_str:
        return today.replace(hour=14)

    # Try day names
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    for i, day in enumerate(days):
        if day in date_str:
            days_ahead = (i - today.weekday()) % 7
            return today + timedelta(days=days_ahead or 7)

    return today + timedelta(days=1)
