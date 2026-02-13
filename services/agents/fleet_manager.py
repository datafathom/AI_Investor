import logging
import random
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class FleetManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FleetManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self.agents: Dict[str, Dict] = {}
        self._initialize_mock_fleet()
        self._initialized = True

    def _initialize_mock_fleet(self):
        """Initialize mock data for 84 agents across departments."""
        departments = [
            "Executive", "Strategist", "Researcher", "Analyst", "Quant", 
            "Risk", "Execution", "Portfolio", "Compliance", "Operations"
        ]
        
        roles = ["Manager", "Senior", "Junior", "Specialist"]
        statuses = ["IDLE", "WORKING", "THINKING", "OFFLINE", "ERROR"]
        
        count = 1
        for dept in departments:
            # 8-9 agents per department
            num_agents = random.randint(8, 9)
            for i in range(num_agents):
                agent_id = f"AGENT-{count:03d}"
                role = random.choice(roles)
                
                self.agents[agent_id] = {
                    "id": agent_id,
                    "name": f"{dept} {role} {i+1}",
                    "department": dept,
                    "role": role,
                    "status": random.choice(statuses),
                    "tpm": random.randint(0, 150),
                    "last_active": datetime.now().isoformat(),
                    "uptime_percent": round(random.uniform(95.0, 99.9), 2),
                    "version": "1.0.2"
                }
                count += 1

    async def list_agents(self, department: Optional[str] = None) -> List[Dict]:
        """List all agents, optionally filtered by department."""
        agents = list(self.agents.values())
        if department:
            agents = [a for a in agents if a["department"].lower() == department.lower()]
        return agents

    async def get_agent_details(self, agent_id: str) -> Optional[Dict]:
        """Get details for a specific agent."""
        return self.agents.get(agent_id)

    async def restart_agent(self, agent_id: str) -> Dict:
        """Restart a specific agent."""
        if agent_id in self.agents:
            self.agents[agent_id]["status"] = "RESTARTING"
            # In a real system, trigger restart logic here
            self.agents[agent_id]["status"] = "IDLE"
            self.agents[agent_id]["uptime_percent"] = 100.0
            return {"success": True, "message": f"Agent {agent_id} restarted"}
        return {"success": False, "message": "Agent not found"}
