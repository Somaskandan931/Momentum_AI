from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.auth.jwt_handler import get_current_user
from app.services.idea_service import generate_roadmap
from app.services.trend_service import analyze_trend
from app.services.task_service import create_task
from app.models.task_model import TaskCreate
from app.database.mongodb import get_db
from datetime import datetime, timedelta

router = APIRouter()

class IdeaRequest(BaseModel):
    idea: str
    project_id: str

@router.post("/analyze")
async def analyze_idea(request: IdeaRequest, current_user: dict = Depends(get_current_user)):
    """Analyze an idea: generate roadmap + trend analysis."""
    roadmap = await generate_roadmap(request.idea)
    trend = await analyze_trend(request.idea)
    return {"roadmap": roadmap, "trend_analysis": trend}

@router.post("/generate-tasks")
async def generate_tasks_from_idea(request: IdeaRequest, current_user: dict = Depends(get_current_user)):
    """Generate roadmap and automatically create Kanban tasks."""
    roadmap = await generate_roadmap(request.idea)

    created_tasks = []
    base_date = datetime.utcnow()
    for item in roadmap:
        task_data = TaskCreate(
            project_id=request.project_id,
            title=item["title"],
            description=item.get("description", ""),
            priority=item.get("priority", "medium"),
            estimated_time=item.get("estimated_time", 60),
            deadline=base_date + timedelta(days=item.get("day", 1))
        )
        task = await create_task(task_data, created_by_ai=True)
        created_tasks.append(task)

    return {"tasks_created": len(created_tasks), "tasks": created_tasks}
