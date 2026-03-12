from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ScheduleSlot(BaseModel):
    task_id: str
    start_time: datetime
    end_time: datetime

class ScheduleCreate(BaseModel):
    project_id: str
    task_ids: List[str]

class ScheduleOut(BaseModel):
    id: str
    user_id: str
    project_id: str
    tasks: List[str]
    schedule_slots: List[ScheduleSlot]
    generated_by_rl: bool
    updated_at: datetime

class ScheduleInDB(BaseModel):
    user_id: str
    project_id: str
    tasks: List[str] = []
    schedule_slots: List[ScheduleSlot] = []
    generated_by_rl: bool = False
    updated_at: datetime = Field(default_factory=datetime.utcnow)
