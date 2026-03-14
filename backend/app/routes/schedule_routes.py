"""
Schedule Routes — generate and retrieve time-blocked schedules for a project.
"""

from fastapi import APIRouter, Depends

from backend.app.auth.jwt_handler import get_current_user
from backend.app.models.schedule_model import ScheduleCreate
from backend.app.services.schedule_service import generate_schedule, get_schedule

router = APIRouter()


@router.post("/generate")
async def create_schedule(
    data: ScheduleCreate,
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["user_id"]
    return await generate_schedule(user_id, data.project_id, data.task_ids)


@router.get("/{project_id}")
async def fetch_schedule(
    project_id: str,
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["user_id"]
    return await get_schedule(user_id, project_id)