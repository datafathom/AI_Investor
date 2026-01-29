"""
Sentiment Engine.
Analyzes user inputs for signs of emotional tilt.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SentimentEngine:
    """Analyzes text for emotional tilt."""
    
    TILT_KEYWORDS = ["revenge", "stupid", "idiot", "all in", "must win", "rigged", "scam"]
    
    def analyze(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        score = 0
        detected_words = []
        
        for word in self.TILT_KEYWORDS:
            if word in text_lower:
                score += 1
                detected_words.append(word)
        
        is_tilted = score >= 1
        
        if is_tilted:
            logger.info(f"TILT_DETECTED: Found keywords {detected_words}")
            
        return {
            "is_tilted": is_tilted,
            "score": score,
            "detected_keywords": detected_words
        }
