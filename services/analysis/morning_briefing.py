"""
==============================================================================
FILE: services/analysis/morning_briefing.py
ROLE: Daily Report Generator
PURPOSE:
    Generate a natural language summary of the market and portfolio plan.
    "The AI talks to you."
    
    Data Sources:
    - User Portfolio Performance
    - Fear & Greed Index
    - Major Market Moves (SPY, VIX)
       
ROADMAP: Phase 29 - User Personalization
==============================================================================
"""

import random

class MorningBriefingService:
    
    def generate_briefing(self, 
                         user_name: str,
                         portfolio_value: float,
                         fear_index: float,
                         market_sentiment: str) -> str:
        """
        Constructs a personalized morning briefing.
        In a full version, this would use an LLM (OpenAI/Anthropic) to write the text.
        Here we use a robust template engine.
        """
        
        # 1. Opening
        openings = [
            f"Good morning, {user_name}.",
            f"Rise and grind, {user_name}.",
            f"Market inputs processed. Hello, {user_name}."
        ]
        opening = random.choice(openings)
        
        # 2. Market Context
        if fear_index > 75:
            context = "The market is overheated (Greed territory). Caution is advised."
            action = "We are trimming high-beta positions and adding to shields."
        elif fear_index < 25:
            context = "There is blood in the streets (Fear territory). Opportunity detected."
            action = "We are deploying cash into high-quality oversold assets."
        else:
            context = "Markets are neutral. Typical volatility expected."
            action = "Maintaining current balanced allocation."
            
        # 3. Portfolio Update
        perf_emoji = "🚀" if market_sentiment == "BULLISH" else "🛡️"
        status = f"Your portfolio stands at ${portfolio_value:,.2f}."
        
        # 4. Closing
        closing = "Monitoring systems active. Good luck."
        
        # Assemble
        report = f"""
{opening}

**Market Intelligence**
{context}

**Tactical Plan**
{action}

**Status**
{status} {perf_emoji}

{closing}
"""
        return report.strip()

# Singleton
_instance = None

def get_briefing_service() -> MorningBriefingService:
    global _instance
    if _instance is None:
        _instance = MorningBriefingService()
    return _instance
