"""
Debate Chamber 2.0 (Persona GUI).
Orchestrates debate between financial personas.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class DebateChamber:
    """Orchestrates multi-agent debate."""
    
    PERSONAS = ["AGGRESSIVE_GROWTH", "CONSERVATIVE_YIELD", "MACRO_BEAR", "QUANT_ARBITRAGE"]
    
    def __init__(self):
        self.points = []
    
    def add_point(self, persona: str, argument: str, confidence: float):
        if persona not in self.PERSONAS:
            logger.warning(f"Unknown persona: {persona}")
            return
            
        self.points.append({
            "persona": persona,
            "argument": argument,
            "confidence": confidence
        })
        
    def get_consensus(self) -> Dict[str, Any]:
        if not self.points:
            return {"verdict": "NO_DATA", "score": 0}
            
        bull_score = sum(p["confidence"] for p in self.points if "GROWTH" in p["persona"] or "ARBITRAGE" in p["persona"])
        bear_score = sum(p["confidence"] for p in self.points if "CONSERVATIVE" in p["persona"] or "BEAR" in p["persona"])
        
        total = bull_score + bear_score
        if total == 0: return {"verdict": "NEUTRAL", "score": 0.5}
        
        return {
            "verdict": "BULLISH" if bull_score > bear_score else "BEARISH",
            "bull_sentiment": bull_score / total,
            "bear_sentiment": bear_score / total
        }
