"""
Inbox Service
Phase 8 Implementation: The Global HQ

Handles email classification and triage using Local LLMs (via Ollama).
"""

import logging
from typing import Dict, Any, List, Optional
from services.system.model_manager import get_model_manager, ModelConfig, ModelProvider

logger = logging.getLogger(__name__)

class InboxService:
    """
    Manages Zero-Noise Inbox triage.
    """
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InboxService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.model_manager = get_model_manager()
        self.local_config = ModelConfig(
            provider=ModelProvider.OLLAMA,
            model_id="llama3" # Default local model
        )
        self._initialized = True
        logger.info("InboxService initialized")

    async def classify_email(self, subject: str, sender: str, snippet: str) -> Dict[str, Any]:
        """
        Triage an incoming email using Local LLM.
        """
        prompt = f"""
        Triage the following email for the CEO:
        FROM: {sender}
        SUBJECT: {subject}
        CONTENT: {snippet}

        Classify as: ACTIONABLE, PROMO, or NOISE.
        Return ONLY a JSON object: {{"classification": "X", "reason": "Y", "urgency": 1-10}}
        """
        
        response_text = await self.model_manager.get_completion(
            prompt=prompt,
            config=self.local_config,
            system_message="You are a strict executive assistant filter."
        )
        
        # Simple extraction logic (robustness would depend on model output quality)
        try:
            import json
            import re
            match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if match:
                result = json.loads(match.group())
                return result
        except Exception as e:
            logger.error(f"Failed to parse classification: {e}")
            
        return {
            "classification": "NOISE",
            "reason": "Classification engine failure",
            "urgency": 1
        }

def get_inbox_service() -> InboxService:
    return InboxService()
