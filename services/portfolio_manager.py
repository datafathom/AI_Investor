"""
==============================================================================
AI Investor - Portfolio Manager
==============================================================================
PURPOSE:
    Manages the dual-portfolio system: Defensive and Aggressive.
    
    DEFENSIVE PORTFOLIO:
        - Risk management and hedging
        - Iron Condors, covered calls, protective puts
        - VIX-based protection
        - Target: Preserve capital, generate steady income
    
    AGGRESSIVE PORTFOLIO:
        - High-conviction "Sure Thing" plays
        - Leveraged instruments (2x/3x ETFs, options)
        - Value plays with structural moats
        - Target: Maximum returns on high-conviction bets

ARCHITECTURE:
    The two portfolios hedge each other:
    - Aggressive gains offset by Defensive hedges during volatility
    - Defensive income provides runway during Aggressive drawdowns
==============================================================================
"""
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class PortfolioType(Enum):
    """Portfolio type classification."""
    DEFENSIVE = "DEFENSIVE"
    AGGRESSIVE = "AGGRESSIVE"


class ConvictionLevel(Enum):
    """Conviction level for aggressive plays."""
    LOW = 1       # Standard position sizing
    MEDIUM = 2    # 1.5x position size
    HIGH = 3      # 2x position size
    SURE_THING = 4  # 3x position size, leverage allowed


@dataclass
class Position:
    """Represents a single position in a portfolio."""
    symbol: str
    quantity: float
    entry_price: float
    current_price: float
    portfolio_type: PortfolioType
    conviction_level: ConvictionLevel = ConvictionLevel.LOW
    is_leveraged: bool = False
    leverage_ratio: float = 1.0
    thesis: str = ""
    
    @property
    def market_value(self) -> float:
        return self.quantity * self.current_price
    
    @property
    def pnl(self) -> float:
        return (self.current_price - self.entry_price) * self.quantity
    
    @property
    def pnl_percent(self) -> float:
        if self.entry_price == 0:
            return 0.0
        return (self.current_price - self.entry_price) / self.entry_price


@dataclass
class Portfolio:
    """Represents a single portfolio (Defensive or Aggressive)."""
    portfolio_type: PortfolioType
    cash: float = 0.0
    positions: List[Position] = field(default_factory=list)
    max_drawdown_limit: float = 0.10  # 10% default
    
    @property
    def total_value(self) -> float:
        positions_value = sum(p.market_value for p in self.positions)
        return self.cash + positions_value
    
    @property
    def total_pnl(self) -> float:
        return sum(p.pnl for p in self.positions)


class PortfolioManager:
    """
    Manages the dual-portfolio system.
    
    Allocates capital between Defensive and Aggressive portfolios
    based on market conditions and conviction levels.
    """
    
    # Default allocation: 60% Defensive, 40% Aggressive
    DEFAULT_DEFENSIVE_ALLOCATION = 0.60
    DEFAULT_AGGRESSIVE_ALLOCATION = 0.40
    
    def __init__(
        self,
        total_capital: float = 100000.0,
        defensive_allocation: float = 0.60
    ) -> None:
        """
        Initialize the Portfolio Manager.
        
        Args:
            total_capital: Starting capital to allocate.
            defensive_allocation: Percentage allocated to defensive (0.0-1.0).
        """
        self.total_capital = total_capital
        self.defensive_allocation = defensive_allocation
        self.aggressive_allocation = 1.0 - defensive_allocation
        
        # Initialize portfolios
        defensive_capital = total_capital * defensive_allocation
        aggressive_capital = total_capital * self.aggressive_allocation
        
        self.defensive = Portfolio(
            portfolio_type=PortfolioType.DEFENSIVE,
            cash=defensive_capital,
            max_drawdown_limit=0.05  # 5% max drawdown for defensive
        )
        
        self.aggressive = Portfolio(
            portfolio_type=PortfolioType.AGGRESSIVE,
            cash=aggressive_capital,
            max_drawdown_limit=0.20  # 20% max drawdown for aggressive
        )
        
        logger.info(f"PortfolioManager initialized: Defensive=${defensive_capital:,.2f}, Aggressive=${aggressive_capital:,.2f}")
    
    def get_combined_value(self) -> float:
        """Get total value across both portfolios."""
        return self.defensive.total_value + self.aggressive.total_value
    
    def get_combined_pnl(self) -> float:
        """Get total P&L across both portfolios."""
        return self.defensive.total_pnl + self.aggressive.total_pnl
    
    def add_position(
        self,
        portfolio_type: PortfolioType,
        symbol: str,
        quantity: float,
        price: float,
        conviction: ConvictionLevel = ConvictionLevel.LOW,
        leverage: float = 1.0,
        thesis: str = ""
    ) -> Dict[str, Any]:
        """
        Add a position to the specified portfolio.
        
        Args:
            portfolio_type: Which portfolio to add to.
            symbol: Ticker symbol.
            quantity: Number of shares/contracts.
            price: Entry price.
            conviction: Conviction level (for sizing).
            leverage: Leverage ratio (1.0 = no leverage).
            thesis: Investment thesis/reasoning.
        """
        portfolio = self.defensive if portfolio_type == PortfolioType.DEFENSIVE else self.aggressive
        
        cost = quantity * price
        
        if cost > portfolio.cash:
            return {
                'success': False,
                'reason': f'Insufficient cash. Need ${cost:,.2f}, have ${portfolio.cash:,.2f}'
            }
        
        position = Position(
            symbol=symbol,
            quantity=quantity,
            entry_price=price,
            current_price=price,
            portfolio_type=portfolio_type,
            conviction_level=conviction,
            is_leveraged=leverage > 1.0,
            leverage_ratio=leverage,
            thesis=thesis
        )
        
        portfolio.positions.append(position)
        portfolio.cash -= cost
        
        logger.info(f"Added {portfolio_type.value} position: {symbol} x{quantity} @ ${price}")
        
        return {
            'success': True,
            'position': {
                'symbol': symbol,
                'quantity': quantity,
                'cost': cost,
                'conviction': conviction.name,
                'leverage': leverage
            }
        }
    
    def add_sure_thing(
        self,
        symbol: str,
        thesis: str,
        capital_percentage: float = 0.10,
        leverage: float = 2.0
    ) -> Dict[str, Any]:
        """
        Add a "Sure Thing" high-conviction play to Aggressive portfolio.
        
        Examples:
        - NVIDIA at $17 (CUDA moat for ML/AI/gaming)
        - CrowdStrike after airport incident (corporate insurance)
        - Biotech with government contract
        
        Args:
            symbol: Ticker symbol.
            thesis: Detailed reasoning for high conviction.
            capital_percentage: % of aggressive portfolio to allocate.
            leverage: Leverage ratio (default 2x).
        """
        available_capital = self.aggressive.cash * capital_percentage
        
        # For demo, assume price = 100
        # In production, this would fetch from market data
        mock_price = 100.0
        quantity = (available_capital * leverage) / mock_price
        
        return self.add_position(
            portfolio_type=PortfolioType.AGGRESSIVE,
            symbol=symbol,
            quantity=quantity,
            price=mock_price,
            conviction=ConvictionLevel.SURE_THING,
            leverage=leverage,
            thesis=thesis
        )
    
    def add_hedge(
        self,
        symbol: str,
        hedge_type: str,
        quantity: float,
        price: float
    ) -> Dict[str, Any]:
        """
        Add a hedging position to Defensive portfolio.
        
        Args:
            symbol: Typically VIX products, puts, etc.
            hedge_type: 'PUT', 'IRON_CONDOR', 'VIX_CALL', etc.
            quantity: Position size.
            price: Entry price.
        """
        return self.add_position(
            portfolio_type=PortfolioType.DEFENSIVE,
            symbol=symbol,
            quantity=quantity,
            price=price,
            conviction=ConvictionLevel.LOW,
            thesis=f"Hedge: {hedge_type}"
        )
    
    def rebalance(self) -> Dict[str, Any]:
        """
        Rebalance portfolios to target allocations.
        
        Called periodically to maintain risk balance.
        """
        total = self.get_combined_value()
        target_defensive = total * self.defensive_allocation
        target_aggressive = total * self.aggressive_allocation
        
        current_defensive = self.defensive.total_value
        current_aggressive = self.aggressive.total_value
        
        defensive_diff = target_defensive - current_defensive
        aggressive_diff = target_aggressive - current_aggressive
        
        return {
            'action': 'REBALANCE_REQUIRED' if abs(defensive_diff) > total * 0.05 else 'BALANCED',
            'current': {
                'defensive': current_defensive,
                'aggressive': current_aggressive
            },
            'target': {
                'defensive': target_defensive,
                'aggressive': target_aggressive
            },
            'adjustment': {
                'defensive': defensive_diff,
                'aggressive': aggressive_diff
            }
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of both portfolios."""
        return {
            'total_value': self.get_combined_value(),
            'total_pnl': self.get_combined_pnl(),
            'defensive': {
                'value': self.defensive.total_value,
                'cash': self.defensive.cash,
                'positions': len(self.defensive.positions),
                'pnl': self.defensive.total_pnl
            },
            'aggressive': {
                'value': self.aggressive.total_value,
                'cash': self.aggressive.cash,
                'positions': len(self.aggressive.positions),
                'pnl': self.aggressive.total_pnl
            },
            'allocation': {
                'defensive_target': self.defensive_allocation,
                'aggressive_target': self.aggressive_allocation
            }
        }
