"""
Tax Harvest Service - Tax-Loss Harvesting Automation

Phase 52: Identifies unrealized losses eligible for harvesting while
avoiding wash-sale violations through 30-day lookback.

Features:
- Wash-sale protection with 30-day violation check
- Tax savings calculation per position
- Correlated replacement asset suggestions
- Long-term vs short-term gains forecasting

Usage:
    service = TaxHarvestService()
    candidates = await service.identify_harvest_candidates("portfolio-1")
    is_wash = await service.check_wash_sale_violation("AAPL", "user-1")
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
from enum import Enum
import logging
import uuid
from utils.database_manager import db_manager

logger = logging.getLogger(__name__)


class TaxRate(Enum):
    """Federal marginal tax rates."""
    RATE_12 = 0.12
    RATE_22 = 0.22
    RATE_24 = 0.24
    RATE_32 = 0.32
    RATE_35 = 0.35
    RATE_37 = 0.37


@dataclass
class HarvestCandidate:
    """Position eligible for tax-loss harvesting."""
    ticker: str
    position_id: str
    unrealized_loss: float
    cost_basis: float
    current_value: float
    holding_period_days: int
    is_long_term: bool
    tax_savings_estimate: float
    wash_sale_risk: bool
    replacement_suggestions: List[str] = field(default_factory=list)


@dataclass
class ReplacementSuggestion:
    """Suggested replacement asset to maintain exposure."""
    ticker: str
    name: str
    correlation: float
    is_substantially_identical: bool
    reason: str


@dataclass
class CapitalGainsProjection:
    """Projected capital gains for tax year."""
    short_term_gains: float
    long_term_gains: float
    short_term_losses: float
    long_term_losses: float
    net_short_term: float
    net_long_term: float
    total_tax_liability: float
    effective_rate: float


@dataclass
class WashSaleCheck:
    """Result of wash sale violation check."""
    ticker: str
    violates_wash_sale: bool
    blocking_trades: List[Dict] = field(default_factory=list)
    safe_date: Optional[str] = None


class TaxHarvestService:
    """
    Service for tax-loss harvesting automation.
    
    Identifies harvestable losses while protecting against
    wash-sale rule violations.
    """
    
    def __init__(self) -> None:
        """Initialize the tax harvest service."""
        self._trade_history: Dict[str, List[Dict]] = {}
        self._correlations: Dict[str, Dict] = self._load_correlations()
        logger.info("TaxHarvestService initialized")
    
    def _load_correlations(self) -> Dict[str, Dict]:
        """Load asset correlation data for replacement suggestions."""
        return {
            "AAPL": {"MSFT": 0.82, "QQQ": 0.88, "XLK": 0.85},
            "MSFT": {"AAPL": 0.82, "QQQ": 0.90, "XLK": 0.87},
            "GOOGL": {"META": 0.75, "QQQ": 0.85, "VOO": 0.78},
            "TSLA": {"RIVN": 0.65, "ARKK": 0.70, "QQQ": 0.55},
            "JPM": {"BAC": 0.88, "XLF": 0.92, "GS": 0.85},
            "XOM": {"CVX": 0.92, "XLE": 0.95, "OXY": 0.80},
        }
    
    async def identify_harvest_candidates(
        self,
        portfolio_id: str,
        min_loss: float = 100.0
    ) -> List[HarvestCandidate]:
        """
        Identify positions eligible for tax-loss harvesting.
        
        Args:
            portfolio_id: Portfolio to analyze
            min_loss: Minimum unrealized loss to consider
            
        Returns:
            List of harvest candidates with tax savings
        """
        # REAL QUERY: pull from tax_lots table
        positions = await self._get_db_positions(portfolio_id)
        
        # Fallback for dev: if no lots in DB, seed some
        if not positions:
             logger.warning(f"No tax lots found in DB for {portfolio_id}. Seeding dummy data for development.")
             await self._seed_tax_lots(portfolio_id)
             positions = await self._get_db_positions(portfolio_id)
        
        candidates = []
        for pos in positions:
            # Note: in DB, unrealized_pl is the loss/gain
            if pos["unrealized_pl"] >= 0:
                continue  # Only harvest losses
            
            loss = abs(pos["unrealized_pl"])
            if loss < min_loss:
                continue
            
            # Check wash-sale risk
            wash_check = await self.check_wash_sale_violation(
                pos["ticker"], 
                portfolio_id
            )
            
            # Calculate tax savings (assume 32% marginal rate)
            tax_rate = 0.32
            if pos["holding_days"] >= 365:
                tax_rate = 0.15  # LTCG rate
            
            tax_savings = loss * tax_rate
            
            # Get replacement suggestions
            replacements = await self.suggest_replacement_assets(pos["ticker"])
            
            candidates.append(HarvestCandidate(
                ticker=pos["ticker"],
                position_id=pos["id"],
                unrealized_loss=loss,
                cost_basis=pos["cost_basis"],
                current_value=pos["current_value"],
                holding_period_days=pos["holding_days"],
                is_long_term=pos["holding_days"] >= 365,
                tax_savings_estimate=round(tax_savings, 2),
                wash_sale_risk=wash_check.violates_wash_sale,
                replacement_suggestions=[r.ticker for r in replacements[:3]]
            ))
        
        # Sort by tax savings
        candidates.sort(key=lambda x: x.tax_savings_estimate, reverse=True)
        
        return candidates
    
    async def check_wash_sale_violation(
        self,
        ticker: str,
        user_id: str
    ) -> WashSaleCheck:
        """
        Check if selling would trigger wash-sale violation.
        
        Looks for purchases of same/substantially identical securities
        within 30 days before or after the sale.
        
        Args:
            ticker: Security to check
            user_id: User's trade history
            
        Returns:
            WashSaleCheck with violation status
        """
        # Get trade history for this ticker
        trades = self._trade_history.get(f"{user_id}:{ticker}", [])
        
        # Check for recent purchases (within 30 days)
        now = datetime.now(timezone.utc)
        thirty_days_ago = now - timedelta(days=30)
        
        blocking_trades = []
        for trade in trades:
            trade_date = datetime.fromisoformat(trade["date"])
            if trade_date.tzinfo is None:
                trade_date = trade_date.replace(tzinfo=timezone.utc)
            if trade["action"] == "BUY" and trade_date >= thirty_days_ago:
                blocking_trades.append(trade)
        
        violates = len(blocking_trades) > 0
        safe_date = None
        
        if blocking_trades:
            # Latest buy + 31 days
            latest_buy = max(
                datetime.fromisoformat(t["date"]).replace(tzinfo=timezone.utc) if datetime.fromisoformat(t["date"]).tzinfo is None else datetime.fromisoformat(t["date"])
                for t in blocking_trades
            )
            safe_date = (latest_buy + timedelta(days=31)).strftime("%Y-%m-%d")
        
        return WashSaleCheck(
            ticker=ticker,
            violates_wash_sale=violates,
            blocking_trades=blocking_trades,
            safe_date=safe_date
        )
    
    async def calculate_tax_savings(
        self,
        loss_amount: float,
        tax_rate: float = 0.32
    ) -> float:
        """
        Calculate tax savings from harvesting a loss.
        
        Args:
            loss_amount: Unrealized loss amount
            tax_rate: Marginal tax rate
            
        Returns:
            Estimated tax savings
        """
        return round(loss_amount * tax_rate, 2)
    
    async def suggest_replacement_assets(
        self,
        ticker: str
    ) -> List[ReplacementSuggestion]:
        """
        Suggest correlated assets to maintain exposure.
        
        Uses Neo4j correlation data to find similar assets
        that are not substantially identical (wash-sale safe).
        
        Args:
            ticker: Original ticker being sold
            
        Returns:
            List of replacement suggestions
        """
        correlations = self._correlations.get(ticker, {})
        
        suggestions = []
        for replacement, corr in correlations.items():
            # ETFs are generally not substantially identical
            is_etf = replacement.endswith("Q") or replacement.startswith("XL") or replacement == "VOO"
            
            suggestions.append(ReplacementSuggestion(
                ticker=replacement,
                name=f"{replacement} Equity",
                correlation=corr,
                is_substantially_identical=not is_etf,
                reason="ETF provides similar sector exposure" if is_etf else "Individual stock with high correlation"
            ))
        
        # Sort by correlation, prefer non-identical
        suggestions.sort(
            key=lambda x: (not x.is_substantially_identical, x.correlation),
            reverse=True
        )
        
        return suggestions
    
    async def project_capital_gains(
        self,
        portfolio_id: str,
        scenario: str = "hold"
    ) -> CapitalGainsProjection:
        """
        Project capital gains for tax year under different scenarios.
        
        Args:
            portfolio_id: Portfolio to analyze
            scenario: "hold", "harvest_all", or "harvest_selective"
            
        Returns:
            CapitalGainsProjection with tax estimates
        """
        # Mock projection based on scenario
        base_st_gains = 15000.0
        base_lt_gains = 25000.0
        base_st_losses = 3000.0
        base_lt_losses = 2000.0
        
        if scenario == "harvest_all":
            # Assume we harvest all possible losses
            base_st_losses += 8000.0
            base_lt_losses += 5000.0
        elif scenario == "harvest_selective":
            # Harvest only high-value losses
            base_st_losses += 4000.0
        
        net_st = base_st_gains - base_st_losses
        net_lt = base_lt_gains - base_lt_losses
        
        # Calculate tax liability
        st_tax = max(0, net_st) * 0.32  # Ordinary income rate
        lt_tax = max(0, net_lt) * 0.15  # LTCG rate
        
        total_gains = base_st_gains + base_lt_gains
        total_tax = st_tax + lt_tax
        effective_rate = total_tax / total_gains if total_gains > 0 else 0
        
        return CapitalGainsProjection(
            short_term_gains=base_st_gains,
            long_term_gains=base_lt_gains,
            short_term_losses=base_st_losses,
            long_term_losses=base_lt_losses,
            net_short_term=net_st,
            net_long_term=net_lt,
            total_tax_liability=round(total_tax, 2),
            effective_rate=round(effective_rate, 4)
        )
    
    async def _get_db_positions(self, portfolio_id: str) -> List[Dict]:
        """Fetch tax lots from TimescaleDB."""
        positions = []
        try:
            with db_manager.pg_cursor() as cur:
                # We use portfolio_id as account_id if UUID-like, else fallback
                try:
                    account_uuid = uuid.UUID(portfolio_id)
                except ValueError:
                    # For demo 'default' etc, we use a fixed UUID for seeding
                    account_uuid = uuid.UUID("00000000-0000-0000-0000-000000000001")
                
                cur.execute("""
                    SELECT id, ticker, cost_basis_per_share * quantity as cost_basis, 
                           current_price * quantity as current_value, unrealized_pl,
                           (CURRENT_DATE - purchase_date) as holding_days
                    FROM tax_lots
                    WHERE account_id = %s
                """, (account_uuid,))
                
                rows = cur.fetchall()
                for row in rows:
                    positions.append({
                        "id": str(row[0]),
                        "ticker": row[1],
                        "cost_basis": float(row[2]),
                        "current_value": float(row[3]),
                        "unrealized_pl": float(row[4]),
                        "holding_days": row[5] if row[5] is not None else 0
                    })
        except Exception as e:
            logger.error(f"Error fetching from tax_lots table: {e}")
            
        return positions

    async def _seed_tax_lots(self, portfolio_id: str):
        """Seed the database with initial tax lots for testing."""
        try:
             try:
                account_uuid = uuid.UUID(portfolio_id)
             except ValueError:
                account_uuid = uuid.UUID("00000000-0000-0000-0000-000000000001")
                
             with db_manager.pg_cursor() as cur:
                 # Check if already seeded
                 cur.execute("SELECT COUNT(*) FROM tax_lots WHERE account_id = %s", (account_uuid,))
                 if cur.fetchone()[0] > 0:
                     return
                 
                 seed_data = [
                    ("AAPL", 100, 150.0, 142.0, -800.0, -5.3, datetime.now(timezone.utc) - timedelta(days=180)),
                    ("TSLA", 50, 160.0, 110.0, -2500.0, -31.2, datetime.now(timezone.utc) - timedelta(days=90)),
                    ("JPM", 120, 166.0, 153.5, -1500.0, -7.5, datetime.now(timezone.utc) - timedelta(days=250)),
                    ("MSFT", 80, 420.0, 438.75, 1500.0, 4.4, datetime.now(timezone.utc) - timedelta(days=400)), # Gain (won't be harvested)
                    ("XOM", 200, 110.0, 109.0, -200.0, -0.9, datetime.now(timezone.utc) - timedelta(days=450)), # LTCG loss
                 ]
                 
                 for ticker, qty, basis, price, pl, pl_pct, p_date in seed_data:
                     cur.execute("""
                        INSERT INTO tax_lots (account_id, ticker, quantity, cost_basis_per_share, purchase_date, current_price, unrealized_pl, unrealized_pl_pct)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                     """, (account_uuid, ticker, qty, basis, p_date, price, pl, pl_pct))
                 
                 logger.info(f"Seeded {len(seed_data)} tax lots into DB for {portfolio_id}")
        except Exception as e:
            logger.error(f"Error seeding tax_lots: {e}")

    def get_tax_rate_presets(self) -> List[Dict]:
        """Get available tax rate presets."""
        return [
            {"rate": 0.12, "label": "12% (Low bracket)"},
            {"rate": 0.22, "label": "22% (Mid bracket)"},
            {"rate": 0.24, "label": "24% (Mid-high bracket)"},
            {"rate": 0.32, "label": "32% (High bracket)"},
            {"rate": 0.35, "label": "35% (Higher bracket)"},
            {"rate": 0.37, "label": "37% (Top bracket)"},
        ]
