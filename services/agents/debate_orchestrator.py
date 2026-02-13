import logging
import random
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import uuid

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
        session_id = str(uuid.uuid4())
        self.active_session = {
            "id": session_id,
            "ticker": ticker,
            "status": "ACTIVE",
            "start_time": datetime.now(timezone.utc).isoformat(),
            "transcript": [],
            "sentiment_history": [],
            "consensus": {
                "score": 50.0, # 0-100 scale
                "decision": "NEUTRAL",
                "bullish_votes": 0,
                "bearish_votes": 0,
                "total_votes": 0
            },
            "participants": [
                {"name": "The Bull", "role": "Optimist", "avatar": "🐂"},
                {"name": "The Bear", "role": "Skeptic", "avatar": "🐻"},
                {"name": "The Risk Manager", "role": "Pragmatist", "avatar": "🛡️"}
            ]
        }
        
        # Seed with initial opening statements
        self._add_turn("The Bull", "Optimist", f"I believe {ticker} is poised for significant growth due to recent sector rotation.", "BULLISH")
        self._add_turn("The Bear", "Skeptic", f"While growth is possible, {ticker} faces severe headwinds from macro conditions.", "BEARISH")
        
        return self.active_session

    def get_session(self, session_id: Optional[str] = None) -> Optional[Dict]:
        """Get the current active session."""
        if not self.active_session:
            return None
        if session_id and self.active_session["id"] != session_id:
            return None # Simulating single active session for now
        return self.active_session

    def inject_argument(self, user_id: str, argument_text: str, sentiment: str = "NEUTRAL") -> Dict[str, Any]:
        """
        Injects a user argument into the debate and triggers agent responses.
        """
        if not self.active_session:
            raise ValueError("No active debate session")

        # 1. Add User Argument to Transcript
        self._add_turn("Human Trader", "Intervenor", argument_text, sentiment, is_human=True)
        
        # 2. Trigger Agent Response (Mock)
        responder = "The Bear" if sentiment == "BULLISH" else "The Bull"
        response_text = f"That is an interesting point about '{argument_text}', but we must consider the counter-evidence."
        self._add_turn(responder, "Responder", response_text, "NEUTRAL")
        
        return self.active_session

    def _add_turn(self, speaker: str, role: str, text: str, sentiment: str, is_human: bool = False):
        """Adds a turn to the transcript and updates state."""
        turn = {
            "id": str(uuid.uuid4()),
            "speaker": speaker,
            "role": role,
            "text": text,
            "sentiment": sentiment, # BULLISH, BEARISH, NEUTRAL
            "is_human": is_human,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.active_session["transcript"].append(turn)
        self._update_consensus(sentiment)

    def _update_consensus(self, sentiment: str):
        """Update consensus score based on turn sentiment."""
        current_score = self.active_session["consensus"]["score"]
        
        impact = 0
        if sentiment == "BULLISH":
            impact = random.uniform(2, 5)
            self.active_session["consensus"]["bullish_votes"] += 1
        elif sentiment == "BEARISH":
            impact = random.uniform(-5, -2)
            self.active_session["consensus"]["bearish_votes"] += 1
        
        self.active_session["consensus"]["total_votes"] += 1
            
        new_score = max(0, min(100, current_score + impact))
        self.active_session["consensus"]["score"] = round(new_score, 1)
        self.active_session["sentiment_history"].append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "score": new_score
        })
        
        if new_score > 60:
            self.active_session["consensus"]["decision"] = "BULLISH"
        elif new_score < 40:
            self.active_session["consensus"]["decision"] = "BEARISH"
        else:
            self.active_session["consensus"]["decision"] = "NEUTRAL"
