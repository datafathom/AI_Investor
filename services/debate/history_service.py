import logging
import uuid
from typing import List, Dict, Optional, Any
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class HistoryService:
    """Manages storage and retrieval of past debate transcripts and outcomes."""
    
    def __init__(self):
         # Mock database
        self.history_db = self._generate_mock_history()

    def _generate_mock_history(self) -> List[Dict]:
        """Generate mock history for UI development."""
        tickers = ["NVDA", "TSLA", "AMD", "PLTR", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NFLX"]
        outcomes = ["BULLISH", "BEARISH", "NEUTRAL"]
        
        history = []
        for i in range(25):
            ticker = random.choice(tickers)
            outcome = random.choice(outcomes)
            date = datetime.now().isoformat()
            
            # Generate a consistent ID based on loop index for stability if needed, or random
            session_id = str(uuid.uuid4())
            
            history.append({
                "id": session_id,
                "ticker": ticker,
                "date": date,
                "outcome": outcome,
                "score": random.randint(30, 95),
                "turns_count": random.randint(5, 50),
                "participants": ["The Bull", "The Bear", "Risk Manager", "Sentinel"]
            })
        return sorted(history, key=lambda x: x["date"], reverse=True)

    async def list_history(self, ticker: Optional[str] = None, outcome: Optional[str] = None) -> List[Dict]:
        """List past debates with optional filtering."""
        # Refresh mock data occasionally or just return static
        results = self.history_db
        if ticker:
            results = [r for r in results if ticker.upper() in r["ticker"]]
        if outcome:
            results = [r for r in results if r["outcome"] == outcome.upper()]
        return results

    async def get_transcript(self, session_id: str) -> Dict[str, Any]:
        """Get full transcript for a specific session."""
        # Find session meta
        session = next((s for s in self.history_db if s["id"] == session_id), None)
        if not session:
            # Fallback for dev: if not found, generate a lively one
            return {
                "meta": {
                    "id": session_id,
                    "ticker": "UNKNOWN",
                    "date": datetime.now().isoformat(),
                    "outcome": "NEUTRAL",
                    "score": 50,
                    "turns_count": 0
                },
                "transcript": [
                    {"id": "sys-1", "speaker": "System", "text": "Session not found in mock DB. Showing placeholder.", "timestamp": datetime.now().isoformat()}
                ]
            }
            
        # Generate mock transcript details on the fly
        transcript = []
        participants = session.get("participants", ["The Bull", "The Bear"])
        
        # Generate a realistic-looking conversation
        phrases = [
            "The technicals differ from the fundamentals here.",
            "RSI is overbought on the daily timeframe.",
            "Revenue growth requires more scrutiny.",
            "Institutional flow is positive.",
            "Geopolitical risk factors are increasing.",
            "Option implied volatility is elevated.",
            "We should hedge the downside exposure.",
            "Taking a long position is justified.",
            "I recommend a neutral stance for now.",
            "The macro environment is deteriorating."
        ]
        
        for i in range(session["turns_count"]):
             speaker = participants[i % len(participants)]
             text = random.choice(phrases)
             transcript.append({
                 "id": f"msg-{i}",
                 "speaker": speaker,
                 "text": f"{text} (Turn {i+1})",
                 "timestamp": session["date"]
             })
             
        return {
            "meta": session,
            "transcript": transcript
        }

history_service = HistoryService()
