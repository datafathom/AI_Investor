import logging
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class LogStreamer:
    """Simulates log streaming from agents."""
    
    def get_logs(self, agent_id: str, limit: int = 50) -> List[Dict]:
        """Get recent logs for an agent."""
        levels = ["INFO", "DEBUG", "WARNING", "ERROR"]
        components = ["Memory", "Planner", "Executor", "Network"]
        messages = [
            "Analyzing market sentiment for SPY",
            "Fetching historical data",
            "Optimizing portfolio weights",
            "Connection timeout, retrying...",
            "Trade executed: BUY 100 AAPL @ 150.00",
            "Garbage collection triggered",
            "Updating knowledge graph",
            "Consensus reached with Agent-007"
        ]
        
        logs = []
        for i in range(limit):
            level = random.choice(levels)
            msg = random.choice(messages)
            if level == "ERROR":
                msg = f"Exception in {random.choice(components)}: {msg}"
            
            logs.append({
                "timestamp": datetime.now().isoformat(),
                "agent_id": agent_id,
                "level": level,
                "component": random.choice(components),
                "message": msg
            })
            
        return sorted(logs, key=lambda x: x["timestamp"])

log_streamer = LogStreamer()
