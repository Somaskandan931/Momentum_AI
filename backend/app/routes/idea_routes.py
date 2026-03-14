"""
Idea Routes — endpoints for AI roadmap generation and trend analysis.
"""

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from backend.app.auth.jwt_handler import get_current_user
from backend.app.services.idea_service import generate_roadmap
from backend.app.services.trend_service import analyze_trend
from backend.app.services.task_service import create_task
from backend.app.models.task_model import TaskCreate

router = APIRouter()


class IdeaRequest(BaseModel):
    idea: str
    project_id: str


@router.post("/analyze")
async def analyze_idea(
    request: IdeaRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Generate a roadmap AND run trend analysis for a project idea.
    Returns both results in a single response.
    """
    try:
        roadmap = await generate_roadmap(request.idea)
        trend = await analyze_trend(request.idea)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

    return {"roadmap": roadmap, "trend_analysis": trend}


@router.post("/generate-tasks")
async def generate_tasks_from_idea(
    request: IdeaRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Generate a roadmap for a project idea and persist each step as a Task.
    Returns the number of tasks created and their full details.
    """
    try:
        roadmap = await generate_roadmap(request.idea)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

    base_date = datetime.utcnow()
    created_tasks = []

    for item in roadmap:
        task_data = TaskCreate(
            project_id=request.project_id,
            title=item["title"],
            description=item.get("description", ""),
            priority=item.get("priority", "medium"),
            estimated_time=item.get("estimated_time", 60),
            deadline=base_date + timedelta(days=item.get("day", 1)),
        )
        task = await create_task(task_data, created_by_ai=True)
        created_tasks.append(task)

    return {"tasks_created": len(created_tasks), "tasks": created_tasks}