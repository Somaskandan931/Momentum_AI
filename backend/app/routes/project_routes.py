"""
Project Routes — CRUD endpoints for projects and survival score retrieval.
"""

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from backend.app.auth.jwt_handler import get_current_user, GUEST_USER_ID
from backend.app.database.mongodb import get_db
from backend.app.models.project_model import ProjectCreate, ProjectInDB
from backend.app.services.survival_score_service import compute_survival_score

router = APIRouter()


def _serialize(doc: dict) -> dict:
    doc["id"] = str(doc.pop("_id"))
    return doc


@router.post("/", status_code=201)
async def create_project(
    project: ProjectCreate,
    current_user: dict = Depends(get_current_user),
):
    db = get_db()
    user_id = current_user["user_id"]
    doc = ProjectInDB(
        title=project.title,
        description=project.description,
        creator_id=user_id,
    )
    result = await db.projects.insert_one(doc.dict())
    created = await db.projects.find_one({"_id": result.inserted_id})
    return _serialize(created)


@router.get("/")
async def list_projects(current_user: dict = Depends(get_current_user)):
    db = get_db()
    user_id = current_user["user_id"]
    projects = []

    if user_id == GUEST_USER_ID:
        # Guests can browse all projects
        async for p in db.projects.find():
            projects.append(_serialize(p))
    else:
        async for p in db.projects.find(
            {"$or": [{"creator_id": user_id}, {"team_members": user_id}]}
        ):
            projects.append(_serialize(p))

    return projects


@router.get("/{project_id}")
async def get_project(
    project_id: str,
    current_user: dict = Depends(get_current_user),
):
    db = get_db()
    project = await db.projects.find_one({"_id": ObjectId(project_id)})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return _serialize(project)


@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    current_user: dict = Depends(get_current_user),
):
    db = get_db()
    result = await db.projects.delete_one({"_id": ObjectId(project_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted"}


@router.get("/{project_id}/survival-score")
async def get_survival_score(
    project_id: str,
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["user_id"]
    score = await compute_survival_score(project_id, user_id)

    db = get_db()
    await db.projects.update_one(
        {"_id": ObjectId(project_id)},
        {"$set": {"idea_survival_score": score}},
    )

    return {"project_id": project_id, "idea_survival_score": score}