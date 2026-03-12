from fastapi import APIRouter, Depends
from app.auth.jwt_handler import get_current_user
from app.models.schedule_model import ScheduleCreate
from app.services.schedule_service import generate_schedule, get_schedule

router = APIRouter()

@router.post("/generate")
async def create_schedule(data: ScheduleCreate, current_user: dict = Depends(get_current_user)):
    return await generate_schedule(current_user["user_id"], data.project_id, data.task_ids)

@router.get("/{project_id}")
async def fetch_schedule(project_id: str, current_user: dict = Depends(get_current_user)):
    return await get_schedule(current_user["user_id"], project_id)
