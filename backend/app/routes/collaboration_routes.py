"""
Collaboration Routes — team member management for projects.
"""

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from backend.app.auth.jwt_handler import get_current_user
from backend.app.database.mongodb import get_db

router = APIRouter()


class MemberAdd(BaseModel):
    project_id: str
    user_id: str
    role: str


class RoleUpdate(BaseModel):
    project_id: str
    user_id: str
    role: str


@router.post("/add-member")
async def add_member(
    data: MemberAdd,
    current_user: dict = Depends(get_current_user),
):
    db = get_db()
    result = await db.projects.update_one(
        {"_id": ObjectId(data.project_id)},
        {
            "$addToSet": {"team_members": data.user_id},
            "$set": {f"roles.{data.user_id}": data.role},
        },
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": f"User {data.user_id} added with role {data.role}"}


@router.post("/update-role")
async def update_role(
    data: RoleUpdate,
    current_user: dict = Depends(get_current_user),
):
    db = get_db()
    result = await db.projects.update_one(
        {"_id": ObjectId(data.project_id)},
        {"$set": {f"roles.{data.user_id}": data.role}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": f"Role updated to {data.role}"}


@router.delete("/remove-member")
async def remove_member(
    project_id: str,
    user_id: str,
    current_user: dict = Depends(get_current_user),
):
    db = get_db()
    result = await db.projects.update_one(
        {"_id": ObjectId(project_id)},
        {
            "$pull": {"team_members": user_id},
            "$unset": {f"roles.{user_id}": ""},
        },
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": f"User {user_id} removed from project"}


@router.get("/{project_id}/members")
async def list_members(
    project_id: str,
    current_user: dict = Depends(get_current_user),
):
    db = get_db()
    project = await db.projects.find_one({"_id": ObjectId(project_id)})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {
        "team_members": project.get("team_members", []),
        "roles": project.get("roles", {}),
    }