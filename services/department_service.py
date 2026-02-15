import logging
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.database import SessionLocal, Base
import os

# Department ID to Name mapping for MOCK mode
DEPT_NAMES = {
    1: "Infrastructure",
    2: "Wealth Planning",
    3: "Intelligence (Columnist)",
    4: "Strategist",
    5: "Execution (Trader)",
    6: "Risk (Sentry)",
    7: "Private Equity (Hunter)",
    8: "Security (Sovereign)",
    9: "Refiner",
    10: "Data Scientist",
    11: "Architect",
    12: "Stress Tester",
    13: "Steward",
    14: "Media Team"
}


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
        self.sql_mock = os.getenv("SQL_MODE") == "MOCK"
        logger.info(f"DepartmentService initialized (Mock Mode: {self.sql_mock})")


    async def get_all_departments(self) -> List[Dict[str, Any]]:
        """
        Retrieves all departments and their associated agents.
        """
        try:
            if self.sql_mock:
                return self._get_mock_departments()
                
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self._get_all_departments_sync)
        except Exception as e:
            logger.error(f"Failed to fetch all departments: {e}")
            if "does not exist" in str(e) or "no such table" in str(e).lower():
                logger.warning("Database table 'departments' missing. Falling back to MOCK data.")
                return self._get_mock_departments()
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
            if self.sql_mock:
                depts = self._get_mock_departments()
                return next((d for d in depts if d["id"] == dept_id), None)

            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self._get_department_by_id_sync, dept_id)
        except Exception as e:
            logger.error(f"Failed to fetch department {dept_id}: {e}")
            if "does not exist" in str(e) or "no such table" in str(e).lower():
                 depts = self._get_mock_departments()
                 return next((d for d in depts if d["id"] == dept_id), None)
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

    def _get_mock_departments(self) -> List[Dict[str, Any]]:
        """Static data for UI rendering when DB is missing/mocked."""
        from datetime import datetime, timezone
        results = []
        for d_id, d_name in DEPT_NAMES.items():
            slug = d_name.lower().replace(" ", "-").replace("(", "").replace(")", "")
            results.append({
                "id": d_id,
                "name": d_name,
                "slug": slug,
                "quadrant": "NW" if d_id < 4 else "NE" if d_id < 8 else "SW" if d_id < 12 else "SE",
                "status": "active",
                "metrics": {
                    "Health": 98.5,
                    "Efficiency": 92.0
                },
                "agents": [], # Simplified for dashboard view
                "last_update": datetime.now(timezone.utc).isoformat()
            })
        return results

