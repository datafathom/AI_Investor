import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class TrailingStopService:
    """
    Monitors holdings for breach of trailing stop levels.
    Designed to 'Raise Cash' automatically if portfolio value drops significantly.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TrailingStopService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("TrailingStopService initialized")

    def check_stop_loss(self, position: Dict[str, Any], current_price: float) -> str:
        """
        Logic: 
        - Track High Water Mark (HWM).
        - If (HWM - Current) / HWM > Threshold -> SELL.
        Standard threshold: 10% from peak.
        """
        ticker = position.get('ticker')
        high_water_mark = position.get('high_water_mark', 0.0)
        
        # Update HWM if new peak
        if current_price > high_water_mark:
            position['high_water_mark'] = current_price
            return "HOLD" # New High, Keep holding
        
        # Calculate Drawdown
        if high_water_mark > 0:
            drawdown_pct = (high_water_mark - current_price) / high_water_mark
            
            # Stop Loss Threshold
            if drawdown_pct >= 0.10: # 10% Trailing Stop
                logger.warning(f"STOP LOSS TRIGGERED for {ticker}: Down {drawdown_pct:.1%} from Peak ${high_water_mark}")
                return "SELL_SIGNAL"
                
        return "HOLD"
