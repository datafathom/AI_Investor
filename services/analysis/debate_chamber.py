"""
==============================================================================
FILE: services/analysis/debate_chamber.py
ROLE: The Moderator
PURPOSE:
    Orchestrate a multi-persona LLM debate to achieve consensus on market trades.
    
    1. Personas:
       - The Bull: Looks for growth and upward momentum.
       - The Bear: Scrutinizes risks and potential downsides.
       - The Risk Manager: Focuses on capital preservation and stop-losses.
       - The CIO (Chief Investment Officer): Aggregate moderator.
       
    2. Logic:
       - Trigger agents with specific system prompts.
       - Collect scores/reasoning.
       - Calculate consensus score.
       
CONTEXT: 
    Phase 38: The Debate Chamber.
==============================================================================
"""

import logging
from typing import Dict, List, Any
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class DebateAgentResponse(BaseModel):
    persona: str
    signal: str # "BUY", "SELL", "HOLD"
    score: float # 0.0 to 1.0
    reasoning: str

class DebateChamber:
    def __init__(self):
        self.personas = {
            "The Bull": "You are a high-conviction bullish analyst. Focus on technical breakouts, growth potential, and positive catalysts.",
            "The Bear": "You are a skeptical, risk-averse bearish analyst. Look for overvaluation, technical failures, and macro headwinds.",
            "The Risk Manager": "You focus exclusively on capital preservation. Evaluate the trade's risk-to-reward ratio and potential max drawdown."
        }
    
    def simulate_debate(self, ticker: str, data_summary: str) -> Dict[str, Any]:
        """
        Simulate a debate (Mocked until real LLM integration).
        """
        responses = []
        
        # In a real scenario, we'd call an LLM for each persona
        # For now, we simulate diverse opinions
        
        # Bull Response
        responses.append(DebateAgentResponse(
            persona="The Bull",
            signal="BUY",
            score=0.85,
            reasoning=f"{ticker} shows strong accumulation on the daily chart with volume expansion."
        ))
        
        # Bear Response
        responses.append(DebateAgentResponse(
            persona="The Bear",
            signal="HOLD",
            score=0.3,
            reasoning=f"Overbought conditions on RSI for {ticker}. Waiting for a mean reversion."
        ))
        
        # Risk Manager Response
        responses.append(DebateAgentResponse(
            persona="The Risk Manager",
            signal="BUY",
            score=0.7,
            reasoning="Entry at current levels allows for a tight stop-loss at the 50-day EMA."
        ))
        
        # Calculate Consensus
        buy_votes = sum(1 for r in responses if r.signal == "BUY")
        avg_score = sum(r.score for r in responses) / len(responses)
        consensus_reached = (buy_votes / len(responses)) >= 0.66 # 2/3 majority
        
        return {
            "ticker": ticker,
            "responses": [r.dict() for r in responses],
            "consensus": {
                "decision": "BUY" if consensus_reached else "NO_CONSENSUS",
                "buy_ratio": buy_votes / len(responses),
                "avg_score": round(avg_score, 2),
                "is_approved": consensus_reached and avg_score > 0.6
            }
        }

# Singleton instance
_debate_chamber = None

def get_debate_chamber() -> DebateChamber:
    global _debate_chamber
    if _debate_chamber is None:
        _debate_chamber = DebateChamber()
    return _debate_chamber
