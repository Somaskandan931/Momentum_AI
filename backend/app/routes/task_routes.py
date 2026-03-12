from fastapi import APIRouter, Depends
from app.auth.jwt_handler import get_current_user
from app.models.task_model import TaskCreate, TaskUpdate
from app.services.task_service import (
    create_task, get_tasks_by_project,
    update_task, delete_task, log_task_completion
)
from pydantic import BaseModel

router = APIRouter()

class CompletionLog(BaseModel):
    task_id: str
    completion_time: int
    delay_minutes: int
    focus_score: float

@router.post("/", status_code=201)
async def add_task(task: TaskCreate, current_user: dict = Depends(get_current_user)):
    return await create_task(task)

@router.get("/project/{project_id}")
async def list_tasks(project_id: str, current_user: dict = Depends(get_current_user)):
    return await get_tasks_by_project(project_id)

@router.patch("/{task_id}")
async def patch_task(task_id: str, updates: TaskUpdate, current_user: dict = Depends(get_current_user)):
    return await update_task(task_id, updates)

@router.delete("/{task_id}")
async def remove_task(task_id: str, current_user: dict = Depends(get_current_user)):
    return await delete_task(task_id)

@router.post("/log-completion")
async def log_completion(log: CompletionLog, current_user: dict = Depends(get_current_user)):
    await log_task_completion(
        current_user["user_id"],
        log.task_id,
        log.completion_time,
        log.delay_minutes,
        log.focus_score
    )
    return {"message": "Completion logged"}
