from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from decimal import Decimal

class TaxLot(BaseModel):
    lot_id: str
    symbol: str
    quantity: Decimal
    cost_basis: Decimal
    acquisition_date: datetime
    current_price: Decimal = Decimal("0.0")

    @property
    def unrealized_p_l(self) -> Decimal:
        return (self.current_price - self.cost_basis) * self.quantity

class TaxOverlayService:
    def __init__(self):
        self.portfolios: Dict[str, List[TaxLot]] = {}
        self.wash_sale_period_days = 30

    def add_lot(self, portfolio_id: str, lot: TaxLot):
        if portfolio_id not in self.portfolios:
            self.portfolios[portfolio_id] = []
        self.portfolios[portfolio_id].append(lot)

    def identify_harvest_opportunities(self, portfolio_id: str, loss_threshold: Decimal = Decimal("-500.0")) -> List[TaxLot]:
        """
        Identify lots with paper losses greater than the threshold.
        """
        if portfolio_id not in self.portfolios:
            return []
            
        lots = self.portfolios[portfolio_id]
        opportunities = [lot for lot in lots if lot.unrealized_p_l <= loss_threshold]
        
        # Sort by largest loss first
        opportunities.sort(key=lambda x: x.unrealized_p_l)
        return opportunities

    def optimize_sma(self, portfolio_id: str, target_exposure: Dict[str, Decimal]) -> Dict[str, Decimal]:
        """
        Optimizes SMA by balancing tracking error vs tax alpha.
        Placeholder for complex quadratic programming optimization.
        """
        if portfolio_id not in self.portfolios:
            return target_exposure
            
        opportunities = self.identify_harvest_opportunities(portfolio_id)
        adjustments = {}
        
        for lot in opportunities:
            # If we harvest this loss, we need to replace it with a highly correlated asset
            # to minimize tracking error (Direct Indexing overlay)
            adjustments[lot.symbol] = Decimal("-1.0") * lot.quantity
            # Suggesting a placeholder replacement (Proxy)
            adjustments[f"{lot.symbol}_PROXY"] = lot.quantity
            
        return adjustments

    def check_wash_sale_risk(self, portfolio_id: str, symbol: str, trade_date: datetime) -> bool:
        """
        Simplified wash sale risk check.
        """
        # Logic to check if the symbol was sold at a loss within the last 30 days
        # or will be bought within the next 30 days.
        # This requires trade history which we would integrate from TradeJournalService
        return False
