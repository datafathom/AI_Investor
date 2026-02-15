import logging
from typing import Any, Dict, List, Optional
from agents.base_agent import BaseAgent
from services.system.model_manager import ModelProvider

logger = logging.getLogger(__name__)

class RedTeamSentryAgent(BaseAgent):
    """
    Agent 1.5: The Red-Team Sentry
    
    Syscall monitoring and security enforcement.
    
    Acceptance Criteria:
    - Immediate SIGKILL on any agent attempting os.system or eval outside whitelist
    """

    # Dangerous patterns that should never be executed
    BLOCKED_PATTERNS = [
        "os.system", "subprocess.call", "subprocess.run", "subprocess.Popen",
        "eval(", "exec(", "__import__", "compile(",
    ]

    # Whitelist of agents allowed to use restricted syscalls (empty by default)
    SYSCALL_WHITELIST: List[str] = []

    def __init__(self) -> None:
        super().__init__(name="orchestrator.red_team_sentry", provider=ModelProvider.GEMINI)
        self.violation_count: int = 0
        self.killed_agents: List[str] = []

    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Monitor for security violations."""
        event_type = event.get("type", "")
        
        if event_type == "syscall.audit":
            return self._audit_syscall(event)
        elif event_type == "code.review":
            return self._review_code(event)
        
        return None

    def _audit_syscall(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Audit a syscall attempt from an agent."""
        agent_id = event.get("agent_id", "unknown")
        syscall = event.get("syscall", "")
        
        # Check if agent is whitelisted
        if agent_id in self.SYSCALL_WHITELIST:
            return {"status": "allowed", "agent_id": agent_id, "reason": "whitelisted"}
        
        # Check for blocked patterns
        for pattern in self.BLOCKED_PATTERNS:
            if pattern in syscall:
                self.violation_count += 1
                self.killed_agents.append(agent_id)
                
                logger.critical(
                    f"SECURITY VIOLATION: Agent '{agent_id}' attempted blocked syscall: {pattern}"
                )
                
                return {
                    "status": "SIGKILL",
                    "agent_id": agent_id,
                    "violation": pattern,
                    "action": "immediate_termination",
                    "total_violations": self.violation_count,
                }
        
        return {"status": "allowed", "agent_id": agent_id}

    def _review_code(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Review code for security violations before execution."""
        code = event.get("code", "")
        agent_id = event.get("agent_id", "unknown")
        
        violations = []
        for pattern in self.BLOCKED_PATTERNS:
            if pattern in code:
                violations.append(pattern)
        
        if violations:
            return {
                "status": "rejected",
                "agent_id": agent_id,
                "violations": violations,
                "message": "Code contains blocked patterns",
            }
        
        return {"status": "approved", "agent_id": agent_id}
