"""
Schedule Service — generates or retrieves a time-blocked schedule for a project.
Falls back to a priority-based heuristic if the RL scheduler is unavailable.
"""

from bson import ObjectId
from datetime import datetime, timedelta

from backend.app.database.mongodb import get_db
from backend.app.models.schedule_model import ScheduleInDB, ScheduleSlot
from backend.app.auth.jwt_handler import GUEST_USER_ID


# ── Helpers ───────────────────────────────────────────────────────────────────

def _serialize(doc: dict) -> dict:
    """Convert MongoDB _id to string id."""
    doc["id"] = str(doc.pop("_id"))
    return doc


def _heuristic_schedule(tasks: list) -> list[ScheduleSlot]:
    """
    Simple priority-first scheduler used when the RL agent is unavailable.
    Slots tasks starting at 09:00 UTC with 15-minute breaks between them.
    """
    priority_order = {"high": 0, "medium": 1, "low": 2}
    sorted_tasks = sorted(
        tasks,
        key=lambda t: priority_order.get(t.get("priority", "medium"), 1),
    )

    slots: list[ScheduleSlot] = []
    current_time = datetime.utcnow().replace(hour=9, minute=0, second=0, microsecond=0)

    for task in sorted_tasks:
        duration = task.get("estimated_time", 60)
        end_time = current_time + timedelta(minutes=duration)
        slots.append(
            ScheduleSlot(
                task_id=str(task["_id"]),
                start_time=current_time,
                end_time=end_time,
            )
        )
        current_time = end_time + timedelta(minutes=15)

    return slots


# ── Service functions ─────────────────────────────────────────────────────────

async def generate_schedule(user_id: str, project_id: str, task_ids: list[str]) -> dict:
    """
    Build a schedule for the given task IDs and persist it to MongoDB.
    Replaces any existing schedule for the project.
    """
    db = get_db()

    # Fetch task documents (support both ObjectId and plain string _id)
    tasks = []
    for tid in task_ids:
        task = None
        try:
            task = await db.tasks.find_one({"_id": ObjectId(tid)})
        except Exception:
            pass
        if task is None:
            task = await db.tasks.find_one({"_id": tid})
        if task:
            tasks.append(task)

    # Try RL agent, fall back to heuristic
    try:
        from ai_engine.rl_scheduler.scheduler_agent import schedule_with_agent
        slots = schedule_with_agent(tasks)
    except Exception:
        slots = _heuristic_schedule(tasks)

    schedule_doc = ScheduleInDB(
        user_id=user_id,
        project_id=project_id,
        tasks=task_ids,
        schedule_slots=slots,
        generated_by_rl=True,
    )

    await db.schedules.delete_many({"project_id": project_id})
    result = await db.schedules.insert_one(schedule_doc.dict())
    created = await db.schedules.find_one({"_id": result.inserted_id})
    return _serialize(created)


async def get_schedule(user_id: str, project_id: str) -> dict:
    """
    Retrieve the most recent schedule for a project.
    Guest users can see any schedule for the project.
    """
    db = get_db()

    if user_id == GUEST_USER_ID:
        doc = await db.schedules.find_one({"project_id": project_id})
    else:
        doc = await db.schedules.find_one({"user_id": user_id, "project_id": project_id})
        if not doc:
            # Fall back to any schedule for this project
            doc = await db.schedules.find_one({"project_id": project_id})

    return _serialize(doc) if doc else {}