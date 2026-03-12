from app.database.mongodb import get_db
from app.models.task_model import TaskInDB, TaskCreate, TaskUpdate
from bson import ObjectId
from datetime import datetime

def _serialize(task: dict) -> dict:
    task["id"] = str(task.pop("_id"))
    if task.get("assigned_to"):
        task["assigned_to"] = str(task["assigned_to"])
    return task

async def create_task(task_data: TaskCreate, created_by_ai: bool = False) -> dict:
    db = get_db()
    doc = TaskInDB(**task_data.dict(), created_by_ai=created_by_ai)
    result = await db.tasks.insert_one(doc.dict())
    created = await db.tasks.find_one({"_id": result.inserted_id})
    return _serialize(created)

async def get_tasks_by_project(project_id: str) -> list:
    db = get_db()
    tasks = []
    async for task in db.tasks.find({"project_id": project_id}):
        tasks.append(_serialize(task))
    return tasks

async def update_task(task_id: str, updates: TaskUpdate) -> dict:
    db = get_db()
    update_data = {k: v for k, v in updates.dict().items() if v is not None}
    await db.tasks.update_one({"_id": ObjectId(task_id)}, {"$set": update_data})
    updated = await db.tasks.find_one({"_id": ObjectId(task_id)})
    return _serialize(updated)

async def delete_task(task_id: str):
    db = get_db()
    await db.tasks.delete_one({"_id": ObjectId(task_id)})
    return {"message": "Task deleted"}

async def log_task_completion(user_id: str, task_id: str, completion_time: int, delay_minutes: int, focus_score: float):
    db = get_db()
    log = {
        "user_id": user_id,
        "task_id": task_id,
        "completion_time": completion_time,
        "delay_minutes": delay_minutes,
        "focus_score": focus_score,
        "timestamp": datetime.utcnow()
    }
    await db.productivity_logs.insert_one(log)
