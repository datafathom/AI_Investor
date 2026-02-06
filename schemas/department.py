from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class AgentRead(BaseModel):
    agent_id: str
    role: Optional[str] = None
    status: str

class DepartmentRead(BaseModel):
    id: int
    name: str
    slug: str
    quadrant: str
    status: str
    metrics: Dict[str, float]
    agents: List[AgentRead]
    last_update: Optional[str] = None

    class Config:
        from_attributes = True

class DepartmentUpdate(BaseModel):
    status: Optional[str] = None
    primary_metric_value: Optional[float] = None
