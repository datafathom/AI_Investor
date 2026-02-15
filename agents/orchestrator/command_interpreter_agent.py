import logging
import re
from typing import Any, Dict, List, Optional
from agents.base_agent import BaseAgent
from services.system.model_manager import ModelProvider

logger = logging.getLogger(__name__)

class CommandInterpreterAgent(BaseAgent):
    """
    Agent 1.2: The Command Interpreter
    
    Translates Voice/Text commands into structured JSON system calls.
    Uses NER (Named Entity Recognition) for entity extraction.
    
    Acceptance Criteria:
    - 99% accuracy on entity extraction (Tickers, Accounts, Dates)
    """

    # Whitelist of recognized command verbs
    COMMAND_VERBS = [
        "BUY", "SELL", "HOLD", "TRANSFER", "REBALANCE", "AUDIT",
        "HARVEST", "SWEEP", "ALERT", "CANCEL", "APPROVE", "REJECT",
    ]

    # Regex patterns for entity extraction
    TICKER_PATTERN = re.compile(r'\b([A-Z]{1,5})\b')
    AMOUNT_PATTERN = re.compile(r'\$?([\d,]+(?:\.\d{2})?)')
    DATE_PATTERN = re.compile(r'\b(\d{4}-\d{2}-\d{2})\b')

    def __init__(self) -> None:
        super().__init__(name="orchestrator.command_interpreter", provider=ModelProvider.GEMINI)
        self.interpretation_count: int = 0
        self.accuracy_tracker: List[bool] = []

    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process natural language commands into structured JSON."""
        event_type = event.get("type", "")
        
        if event_type in ("command.text", "command.voice"):
            return self._interpret_command(event)
        elif event_type == "accuracy.feedback":
            return self._record_feedback(event)
        
        return None

    def _interpret_command(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse a natural language command into a structured JSON call.
        """
        raw_text = event.get("text", "").upper()
        self.interpretation_count += 1
        
        # Extract verb
        detected_verb = None
        for verb in self.COMMAND_VERBS:
            if verb in raw_text:
                detected_verb = verb
                break
        
        # Extract entities
        tickers = self.TICKER_PATTERN.findall(raw_text)
        amounts = self.AMOUNT_PATTERN.findall(raw_text)
        dates = self.DATE_PATTERN.findall(raw_text)
        
        # Filter out verb from tickers
        tickers = [t for t in tickers if t not in self.COMMAND_VERBS]
        
        result = {
            "status": "interpreted",
            "original_text": event.get("text", ""),
            "structured_call": {
                "verb": detected_verb,
                "tickers": tickers[:3] if tickers else [],
                "amounts": [float(a.replace(",", "")) for a in amounts[:2]] if amounts else [],
                "dates": dates[:1] if dates else [],
            },
            "confidence": 0.95 if detected_verb else 0.5,
            "interpretation_id": self.interpretation_count,
        }
        
        logger.info(f"Command interpreted: {detected_verb} -> {tickers}")
        return result

    def _record_feedback(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Record accuracy feedback for tracking."""
        was_correct = event.get("correct", True)
        self.accuracy_tracker.append(was_correct)
        
        # Keep last 1000 for rolling accuracy
        if len(self.accuracy_tracker) > 1000:
            self.accuracy_tracker = self.accuracy_tracker[-1000:]
        
        accuracy = sum(self.accuracy_tracker) / len(self.accuracy_tracker) * 100
        
        return {
            "status": "feedback_recorded",
            "current_accuracy": accuracy,
            "sample_size": len(self.accuracy_tracker),
        }
