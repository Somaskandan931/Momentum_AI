from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class TrendAnalysis(BaseModel):
    competition_level: str = "unknown"
    suggested_improvements: List[str] = []

class ProjectCreate(BaseModel):
    title: str
    description: str

class ProjectOut(BaseModel):
    id: str
    title: str
    description: str
    creator_id: str
    team_members: List[str] = []
    roles: Dict[str, str] = {}
    idea_survival_score: Optional[float] = None
    trend_analysis: TrendAnalysis = Field(default_factory=TrendAnalysis)
    status: str = "active"
    created_at: datetime

class ProjectInDB(BaseModel):
    title: str
    description: str
    creator_id: str
    team_members: List[str] = []
    roles: Dict[str, str] = {}
    idea_survival_score: Optional[float] = None
    trend_analysis: TrendAnalysis = Field(default_factory=TrendAnalysis)
    status: str = "active"
    created_at: datetime = Field(default_factory=datetime.utcnow)
