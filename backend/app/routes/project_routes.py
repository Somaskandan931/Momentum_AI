from fastapi import APIRouter, Depends, HTTPException
from app.auth.jwt_handler import get_current_user
from app.database.mongodb import get_db
from app.models.project_model import ProjectCreate, ProjectInDB
from app.services.survival_score_service import compute_survival_score
from bson import ObjectId
from datetime import datetime

router = APIRouter()

def _serialize(doc: dict) -> dict:
    doc["id"] = str(doc.pop("_id"))
    return doc

@router.post("/", status_code=201)
async def create_project(project: ProjectCreate, current_user: dict = Depends(get_current_user)):
    db = get_db()
    user_id = current_user["user_id"]
    doc = ProjectInDB(
        title=project.title,
        description=project.description,
        creator_id=user_id
    )
    result = await db.projects.insert_one(doc.dict())
    created = await db.projects.find_one({"_id": result.inserted_id})
    return _serialize(created)

@router.get("/")
async def list_projects(current_user: dict = Depends(get_current_user)):
    db = get_db()
    user_id = current_user["user_id"]
    projects = []
    async for p in db.projects.find({"$or": [{"creator_id": user_id}, {"team_members": user_id}]}):
        projects.append(_serialize(p))
    return projects

@router.get("/{project_id}")
async def get_project(project_id: str, current_user: dict = Depends(get_current_user)):
    db = get_db()
    project = await db.projects.find_one({"_id": ObjectId(project_id)})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return _serialize(project)

@router.delete("/{project_id}")
async def delete_project(project_id: str, current_user: dict = Depends(get_current_user)):
    db = get_db()
    await db.projects.delete_one({"_id": ObjectId(project_id)})
    return {"message": "Project deleted"}

@router.get("/{project_id}/survival-score")
async def get_survival_score(project_id: str, current_user: dict = Depends(get_current_user)):
    score = await compute_survival_score(project_id, current_user["user_id"])
    await get_db().projects.update_one(
        {"_id": ObjectId(project_id)},
        {"$set": {"idea_survival_score": score}}
    )
    return {"project_id": project_id, "idea_survival_score": score}
