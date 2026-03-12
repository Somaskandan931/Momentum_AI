from app.database.mongodb import get_db
from app.models.schedule_model import ScheduleInDB, ScheduleSlot
from bson import ObjectId
from datetime import datetime, timedelta
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../"))

def _serialize(doc: dict) -> dict:
    doc["id"] = str(doc.pop("_id"))
    return doc

async def generate_schedule(user_id: str, project_id: str, task_ids: list[str]) -> dict:
    db = get_db()

    # Fetch tasks
    tasks = []
    for tid in task_ids:
        task = await db.tasks.find_one({"_id": ObjectId(tid)})
        if task:
            tasks.append(task)

    # Try to use trained RL agent, fall back to heuristic
    slots = []
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
        generated_by_rl=True
    )
    result = await db.schedules.insert_one(schedule_doc.dict())
    created = await db.schedules.find_one({"_id": result.inserted_id})
    return _serialize(created)

def _heuristic_schedule(tasks: list) -> list[ScheduleSlot]:
    """Priority-based fallback scheduler."""
    priority_order = {"high": 0, "medium": 1, "low": 2}
    sorted_tasks = sorted(tasks, key=lambda t: priority_order.get(t.get("priority", "medium"), 1))

    slots = []
    current_time = datetime.utcnow().replace(hour=9, minute=0, second=0, microsecond=0)
    for task in sorted_tasks:
        duration = task.get("estimated_time", 60)
        end_time = current_time + timedelta(minutes=duration)
        slots.append(ScheduleSlot(
            task_id=str(task["_id"]),
            start_time=current_time,
            end_time=end_time
        ))
        current_time = end_time + timedelta(minutes=15)  # 15 min buffer
    return slots

async def get_schedule(user_id: str, project_id: str) -> dict:
    db = get_db()
    doc = await db.schedules.find_one({"user_id": user_id, "project_id": project_id})
    if doc:
        return _serialize(doc)
    return {}
