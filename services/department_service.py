import logging
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.database import SessionLocal, Base

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════
# MODELS
# ═══════════════════════════════════════════════

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    quadrant = Column(String(50), nullable=False)
    status = Column(String(20), default="active")
    primary_metric_label = Column(String(100))
    primary_metric_value = Column(Float, default=0.0)
    last_update = Column(DateTime, default=datetime.now(timezone.utc))
    
    agents = relationship("DepartmentAgent", back_populates="department")

class DepartmentAgent(Base):
    __tablename__ = "department_agents"
    
    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    agent_id = Column(String(100), nullable=False)
    role = Column(String(100))
    status = Column(String(20), default="idle")
    last_invocation = Column(DateTime)
    
    department = relationship("Department", back_populates="agents")

# ═══════════════════════════════════════════════
# SERVICE
# ═══════════════════════════════════════════════

class DepartmentService:
    """
    Service layer for managing Agent Departments.
    Implements the Singleton pattern.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DepartmentService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("DepartmentService initialized")

    async def get_all_departments(self) -> List[Dict[str, Any]]:
        """
        Retrieves all departments and their associated agents.
        """
        try:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self._get_all_departments_sync)
        except Exception as e:
            logger.error(f"Failed to fetch all departments: {e}")
            return []

    def _get_all_departments_sync(self) -> List[Dict[str, Any]]:
        db = SessionLocal()
        try:
            depts = db.query(Department).all()
            result = []
            for d in depts:
                dept_dict = {
                    "id": d.id,
                    "name": d.name,
                    "slug": d.slug,
                    "quadrant": d.quadrant,
                    "status": d.status,
                    "metrics": {
                        d.primary_metric_label: d.primary_metric_value
                    },
                    "agents": [
                        {"agent_id": a.agent_id, "role": a.role, "status": a.status}
                        for a in d.agents
                    ],
                    "last_update": d.last_update.isoformat() if d.last_update else None
                }
                result.append(dept_dict)
            return result
        finally:
            db.close()

    async def get_department_by_id(self, dept_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieves a single department by its ID.
        """
        try:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self._get_department_by_id_sync, dept_id)
        except Exception as e:
            logger.error(f"Failed to fetch department {dept_id}: {e}")
            return None

    def _get_department_by_id_sync(self, dept_id: int) -> Optional[Dict[str, Any]]:
        db = SessionLocal()
        try:
            d = db.query(Department).filter(Department.id == dept_id).first()
            if not d:
                return None
            return {
                "id": d.id,
                "name": d.name,
                "slug": d.slug,
                "quadrant": d.quadrant,
                "status": d.status,
                "metrics": {
                    d.primary_metric_label: d.primary_metric_value
                },
                "agents": [
                    {"agent_id": a.agent_id, "role": a.role, "status": a.status}
                    for a in d.agents
                ],
                "last_update": d.last_update.isoformat() if d.last_update else None
            }
        finally:
            db.close()

    async def update_department_metric(self, dept_id: int, metric_value: float) -> bool:
        """
        Updates the primary metric for a department.
        """
        try:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self._update_metric_sync, dept_id, metric_value)
        except Exception as e:
            logger.error(f"Failed to update metric for dept {dept_id}: {e}")
            return False

    def _update_metric_sync(self, dept_id: int, value: float) -> bool:
        db = SessionLocal()
        try:
            d = db.query(Department).filter(Department.id == dept_id).first()
            if not d:
                return False
            d.primary_metric_value = value
            d.last_update = datetime.now(timezone.utc)
            db.commit()
            return True
        finally:
            db.close()
