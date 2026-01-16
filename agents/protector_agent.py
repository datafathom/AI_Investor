"""
==============================================================================
AI Investor - Protector Agent
==============================================================================
PURPOSE:
    Monitors VIX levels and portfolio drawdown to enforce the balancing loop.
    Triggers "Bunker Mode" (capital preservation) when oscillations detected.

SAFETY:
    - Checks STOP_ALL_TRADING env var every second
    - Triggers capital outflow to "Storage Homes" on VIX spike
    - Implements Max Drawdown Halt (2% threshold)
==============================================================================
"""
import os
from typing import Any, Dict, Optional
import logging

from agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class ProtectorAgent(BaseAgent):
    """
    The Protector Agent - Guardian of the Set Point.
    
    Monitors market conditions and portfolio health to prevent
    "Oscillations Hell" by triggering protective measures.
    """
    
    def __init__(self) -> None:
        super().__init__(name='ProtectorAgent')
        self.max_drawdown_threshold = float(os.getenv('MAX_DRAWDOWN_PERCENT', '0.02'))
        self.bunker_mode = False
    
    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process market events and check for danger signals.
        
        Args:
            event: Market event containing VIX level or portfolio data.
            
        Returns:
            Action command if protective measure needed.
        """
        # Global Kill Switch check
        if os.getenv('STOP_ALL_TRADING', 'FALSE').upper() == 'TRUE':
            logger.critical("KILL SWITCH ACTIVATED - Halting all operations")
            return {'action': 'HALT_ALL', 'reason': 'Kill switch activated'}
        
        event_type = event.get('type')
        
        if event_type == 'VIX_UPDATE':
            return self._handle_vix_update(event)
        elif event_type == 'PORTFOLIO_UPDATE':
            return self._handle_portfolio_update(event)
        
        return None
    
    def _handle_vix_update(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Check VIX levels for volatility spikes."""
        vix_level = event.get('vix_level', 0)
        
        # VIX > 30 is considered high volatility
        if vix_level > 30:
            logger.warning(f"VIX spike detected: {vix_level}")
            self.bunker_mode = True
            return {
                'action': 'ENTER_BUNKER_MODE',
                'reason': f'VIX at {vix_level}',
                'strategy': 'Reduce exposure, increase hedges'
            }
        
        return None
    
    def _handle_portfolio_update(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Check portfolio for max drawdown breach."""
        current_value = event.get('current_value', 0)
        set_point = event.get('set_point', 0)
        
        if set_point > 0:
            drawdown = (set_point - current_value) / set_point
            
            if drawdown >= self.max_drawdown_threshold:
                logger.critical(f"MAX DRAWDOWN BREACH: {drawdown:.2%}")
                return {
                    'action': 'MAX_DRAWDOWN_HALT',
                    'reason': f'Drawdown {drawdown:.2%} exceeds threshold',
                    'drawdown': drawdown
                }
        
        return None
