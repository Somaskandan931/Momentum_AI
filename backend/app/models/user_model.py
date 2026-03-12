from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class ProductivityProfile(BaseModel):
    peak_hours: List[int] = []
    avg_task_completion_time: float = 0.0

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    skills: List[str] = []
    role: str = "Developer"

class UserOut(BaseModel):
    id: str
    name: str
    email: str
    skills: List[str]
    role: str
    created_at: datetime
    productivity_profile: ProductivityProfile

class UserInDB(BaseModel):
    name: str
    email: str
    password_hash: str
    skills: List[str] = []
    role: str = "Developer"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    productivity_profile: ProductivityProfile = Field(default_factory=ProductivityProfile)
