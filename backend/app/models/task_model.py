from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    project_id: str
    title: str
    description: str = ""
    priority: str = "medium"
    assigned_to: Optional[str] = None
    deadline: Optional[datetime] = None
    estimated_time: int = 60  # minutes


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[str] = None
    status: Optional[str] = None
    deadline: Optional[datetime] = None


class TaskOut(BaseModel):
    id: str
    project_id: str
    title: str
    description: str
    priority: str
    assigned_to: Optional[str]
    status: str
    deadline: Optional[datetime]
    estimated_time: int
    created_by_ai: bool


class TaskInDB(BaseModel):
    project_id: str
    title: str
    description: str = ""
    priority: str = "medium"
    assigned_to: Optional[str] = None
    status: str = "To Do"
    deadline: Optional[datetime] = None
    estimated_time: int = 60
    created_by_ai: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)