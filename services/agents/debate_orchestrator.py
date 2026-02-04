import logging
from typing import List, Dict, Any, Optional
import random
from datetime import timezone, datetime

logger = logging.getLogger(__name__)

class DebateOrchestrator:
    """
    Singleton service that orchestrates the multi-agent debate session.
    Manages state, turn-taking, and consensus calculation.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DebateOrchestrator, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.active_session = None
        logger.info("DebateOrchestrator initialized")

    def start_debate(self, ticker: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Initializes a new debate session for a given ticker.
        """
        logger.info(f"Starting debate for {ticker}")
        self.active_session = {
            "id": f"DBT-{random.randint(1000,9999)}",
            "ticker": ticker,
            "start_time": datetime.now(timezone.utc).isoformat(),
            "transcript": [],
            "consensus": {
                "score": 5.0,
                "decision": "HOLD",
                "buy_ratio": 0.5
            },
            "participants": ["The Bull", "The Bear", "The Risk Manager"]
        }
        
        # Seed with initial opening statements (Simulated LLM calls)
        self._generate_turn("The Bull", f"Opening statement regarding {ticker}")
        
        return self.active_session

    def inject_argument(self, user_id: str, argument_text: str) -> Dict[str, Any]:
        """
        Injects a user argument into the debate and triggers agent responses.
        """
        if not self.active_session:
            raise ValueError("No active debate session")

        # 1. Add User Argument to Transcript
        last_msg = self.active_session["transcript"][-1] if self.active_session["transcript"] else None
        
        user_entry = {
            "id": f"MSG-{len(self.active_session['transcript']) + 1}",
            "parent_id": last_msg["id"] if last_msg else None,
            "persona": "User",
            "role": "Human Intervenor",
            "signal": "NEUTRAL",
            "reasoning": argument_text,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.active_session["transcript"].append(user_entry)
        
        # 2. Trigger Agent Response
        responder = "The Bear" if "bullish" in argument_text.lower() else "The Bull"
        self._generate_turn(responder, f"Response to user argument: '{argument_text}'", user_entry["id"])
        
        return self.active_session

    def _generate_turn(self, persona: str, prompt_context: str, parent_id: Optional[str] = None):
        """
        Simulates an agent taking a turn.
        """
        # Auto-link to last message if parent_id not provided
        if not parent_id and self.active_session["transcript"]:
             parent_id = self.active_session["transcript"][-1]["id"]

        # Mock responses
        mock_responses = [
            f"Based on {prompt_context}, I must emphasize the volatility risk.",
            f"I see your point, but {self.active_session['ticker']} fundamentals remain strong.",
            f"Technical indicators suggest a reversal contradicts {prompt_context}.",
            f"We must consider the macro environment impact on {self.active_session['ticker']}."
        ]
        
        response_text = random.choice(mock_responses)
        signal = "BUY" if persona == "The Bull" else "SELL" if persona == "The Bear" else "HOLD"
        
        entry = {
            "id": f"MSG-{len(self.active_session['transcript']) + 1}",
            "parent_id": parent_id,
            "persona": persona,
            "role": "AI Agent",
            "signal": signal,
            "reasoning": response_text,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        self.active_session["transcript"].append(entry)
        self._recalculate_consensus()

    def _recalculate_consensus(self):
        """
        Simple heuristic update of consensus based on recent transcript sentiment.
        """
        # Mock logic: Randomly drift the consensus
        current_score = self.active_session["consensus"]["score"]
        drift = random.uniform(-1.0, 1.0)
        new_score = max(0.0, min(10.0, current_score + drift))
        
        self.active_session["consensus"]["score"] = round(new_score, 1)
        self.active_session["consensus"]["buy_ratio"] = new_score / 10.0
        
        if new_score > 7.0:
            self.active_session["consensus"]["decision"] = "BUY"
        elif new_score < 3.0:
            self.active_session["consensus"]["decision"] = "SELL"
        else:
            self.active_session["consensus"]["decision"] = "HOLD"
