"""
Front Office Department Agents (14.1)
Phase 8 Implementation: The Global HQ

The Front Office manages the CEO's time, focus, and noise levels.
"""

import logging
from typing import Any, Dict, Optional
from agents.base_agent import BaseAgent, AgentState
from services.admin.inbox_service import get_inbox_service

logger = logging.getLogger(__name__)

class InboxGatekeeperAgent(BaseAgent):
    """
    AGENT 14.1: The Inbox Gatekeeper
    Protects the CEO from administrative 'Noise'.
    """
    def __init__(self):
        super().__init__("frontoffice.gatekeeper.14.1")
        self.inbox_service = get_inbox_service()

    async def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Triage new incoming emails.
        """
        if event.get("type") != "admin.new_email":
            return None

        await self.transition_to(AgentState.SCANNING, "Reviewing sender and metadata")
        
        subject = event.get("subject", "")
        sender = event.get("sender", "")
        body = event.get("body", "")
        
        await self.transition_to(AgentState.ANALYZING, f"Classifying email from {sender}: {subject}")
        
        triage = await self.inbox_service.classify_email(subject, sender, body[:500])
        
        classification = triage.get("classification", "NOISE")
        urgency = triage.get("urgency", 1)
        
        await self.emit_trace("INBOX_TRIAGE", f"Result: {classification} (Urgency: {urgency})")

        if classification == "ACTIONABLE" and urgency >= 7:
            await self.transition_to(AgentState.COMPLETED, "Promoting high-urgency actionable item")
            return {
                "action": "PROMOTE_TO_HUD",
                "triage": triage
            }

        await self.transition_to(AgentState.COMPLETED, f"Archived as {classification}")
        return {
            "action": "ARCHIVE",
            "triage": triage
        }
