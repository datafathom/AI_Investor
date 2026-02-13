"""
Mission Manager Service
Handles the lifecycle of strategic missions, goals, and milestones.
"""
from typing import List, Dict, Optional, Any
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MissionManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MissionManager, cls).__new__(cls)
            cls._instance._missions = []
            cls._instance._init_mock_data()
        return cls._instance

    def _init_mock_data(self):
        """Initialize with some mock missions for development."""
        self._missions = [
            {
                "id": "m1",
                "title": "Establish Market Dominance",
                "status": "in_progress",
                "progress": 45,
                "deadline": "2026-12-31",
                "priority": "high",
                "milestones": [
                    {"id": "ms1", "title": "Deploy Alpha Strategy", "completed": True, "date": "2026-01-15"},
                    {"id": "ms2", "title": "Achieve 15% ROI", "completed": False, "target_date": "2026-06-30"},
                    {"id": "ms3", "title": "Scale to $10M AUM", "completed": False, "target_date": "2026-12-31"}
                ]
            },
            {
                "id": "m2",
                "title": "Risk Mitigation Overhaul",
                "status": "planning",
                "progress": 10,
                "deadline": "2026-06-30",
                "priority": "critical",
                "milestones": [
                    {"id": "ms4", "title": "Audit Current Protocols", "completed": True, "date": "2026-02-01"},
                    {"id": "ms5", "title": "Implement Circuit Breakers", "completed": False, "target_date": "2026-03-30"}
                ]
            }
        ]

    def list_missions(self) -> List[Dict]:
        return self._missions

    def create_mission(self, mission_data: Dict) -> Dict:
        new_mission = {
            "id": str(uuid.uuid4()),
            "title": mission_data.get("title", "New Mission"),
            "status": "planning",
            "progress": 0,
            "deadline": mission_data.get("deadline"),
            "priority": mission_data.get("priority", "medium"),
            "milestones": []
        }
        self._missions.append(new_mission)
        logger.info(f"Created mission: {new_mission['id']}")
        return new_mission

    def update_mission(self, mission_id: str, updates: Dict) -> Optional[Dict]:
        for mission in self._missions:
            if mission["id"] == mission_id:
                mission.update(updates)
                logger.info(f"Updated mission: {mission_id}")
                return mission
        return None

    def get_mission(self, mission_id: str) -> Optional[Dict]:
        for mission in self._missions:
            if mission["id"] == mission_id:
                return mission
        return None

    def add_milestone(self, mission_id: str, milestone_data: Dict) -> Optional[Dict]:
        mission = self.get_mission(mission_id)
        if mission:
            new_milestone = {
                "id": str(uuid.uuid4()),
                "title": milestone_data.get("title"),
                "completed": False,
                "target_date": milestone_data.get("target_date")
            }
            mission["milestones"].append(new_milestone)
            return new_milestone
        return None

def get_mission_manager():
    return MissionManager()
