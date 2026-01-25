"""
Margin Service - Leverage & Collateral Management
Phase 64: Calculates margin requirements, liquidation distances, and de-leveraging.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import logging
from services.portfolio_manager import PortfolioManager, PortfolioType
from services.risk.risk_monitor import RiskMonitor, get_risk_monitor

logger = logging.getLogger(__name__)

@dataclass
class MarginStatus:
    margin_buffer: float
    margin_used: float
    margin_available: float
    liquidation_distance: float
    maintenance_margin: float

@dataclass
class DeleveragePlan:
    positions_to_close: List[Dict[str, Any]]
    total_to_sell: float
    new_buffer: float
    urgency: str

class MarginService:
    def __init__(self, portfolio_manager: Optional[PortfolioManager] = None, risk_monitor: Optional[RiskMonitor] = None) -> None:
        self.pm = portfolio_manager or PortfolioManager(total_capital=3247500.0) # Default to demo value if not provided
        self.risk_monitor = risk_monitor or get_risk_monitor()
        # In a real system, margin_used would come from a broker API or recorded loans
        self._margin_used = 450000.0 
        logger.info("MarginService initialized with PortfolioManager and RiskMonitor")
    
    async def calculate_margin_buffer(self, portfolio_id: str = "default") -> float:
        """
        Calculates the margin buffer based on real portfolio equity and maintenance requirements.
        """
        total_value = self.pm.get_combined_value()
        equity = total_value - self._margin_used
        
        # Calculate maintenance requirement based on asset risk factors (simulated for now, but using real positions)
        maint_req = 0.0
        all_positions = self.pm.defensive.positions + self.pm.aggressive.positions
        
        for pos in all_positions:
            # Volatility-aware maintenance requirement
            # Aggressive positions (leveraged) have higher requirements
            base_req = 0.30 if pos.portfolio_type == PortfolioType.AGGRESSIVE else 0.15
            if pos.is_leveraged:
                base_req *= pos.leverage_ratio
                
            maint_req += pos.market_value * base_req
            
        if equity <= 0:
            return 0.0
            
        buffer = ((equity - maint_req) / equity) * 100
        return max(0.0, buffer)
    
    async def get_margin_status(self, portfolio_id: str = "default") -> MarginStatus:
        buffer = await self.calculate_margin_buffer(portfolio_id)
        total_value = self.pm.get_combined_value()
        
        # Available margin is typically 50% of equity minus used margin (Reg T)
        equity = total_value - self._margin_used
        available = (total_value * 0.5) - self._margin_used
        
        return MarginStatus(
            margin_buffer=buffer,
            margin_used=self._margin_used,
            margin_available=max(0.0, available),
            liquidation_distance=buffer * 1.5, # Heuristic: distance to 0 buffer
            maintenance_margin=self._margin_used * 0.25 # Simplified
        )
    
    async def get_liquidation_distance(self, position_id: str) -> float:
        # Per-position liquidation distance would require more complex modeling
        return 25.5 
    
    async def generate_deleverage_plan(self, target_buffer: float) -> DeleveragePlan:
        current_buffer = await self.calculate_margin_buffer()
        if current_buffer >= target_buffer:
            return DeleveragePlan([], 0, current_buffer, "none")
        
        total_value = self.pm.get_combined_value()
        # How much equity we need to "free up" or how much debt to pay down
        # This is a simplified calculation for the plan
        to_sell = (target_buffer - current_buffer) / 100 * total_value
        
        plan_positions = []
        sold_so_far = 0.0
        
        # Prioritize selling from aggressive portfolio first (Yellowstone principle: sacrifice the weak/volatile)
        sorted_positions = sorted(
            self.pm.aggressive.positions + self.pm.defensive.positions,
            key=lambda p: (p.portfolio_type == PortfolioType.DEFENSIVE, -p.market_value)
        )
        
        for pos in sorted_positions:
            if sold_so_far >= to_sell:
                break
                
            sell_amt = min(pos.market_value, to_sell - sold_so_far)
            shares = sell_amt / pos.current_price
            
            plan_positions.append({
                "ticker": pos.symbol,
                "shares": round(shares, 2),
                "value": round(sell_amt, 2),
                "portfolio": pos.portfolio_type.value
            })
            sold_so_far += sell_amt
            
        return DeleveragePlan(
            positions_to_close=plan_positions,
            total_to_sell=round(sold_so_far, 2),
            new_buffer=target_buffer,
            urgency="critical" if current_buffer < 10 else "high" if current_buffer < 20 else "low"
        )
    
    async def check_danger_zone(self, portfolio_id: str = "default") -> bool:
        buffer = await self.calculate_margin_buffer(portfolio_id)
        return buffer < 20

_margin_service: Optional[MarginService] = None
def get_margin_service() -> MarginService:
    global _margin_service
    if _margin_service is None:
        # In real usage, we might want to pass the actual PM instance
        _margin_service = MarginService()
    return _margin_service
