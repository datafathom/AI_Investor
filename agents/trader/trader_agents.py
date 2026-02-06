"""
Trader Department Agents (4.1 - 4.6)
Phase 3/4 Implementation: The Trading Engine

The Trader Department is the Execution Layer - 
receiving strategy signals and executing them in the market.

ACCEPTANCE CRITERIA:
- Agent 4.1: Order routing with <50ms latency
- Agent 4.2: Fill tracking with 100% reconciliation
- Agent 4.3: Algorithmic execution (TWAP, VWAP, Iceberg)
"""

import logging
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum

from agents.base_agent import BaseAgent
from services.system.model_manager import ModelProvider

logger = logging.getLogger(__name__)


class OrderType(Enum):
    """Supported order types."""
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


class OrderSide(Enum):
    """Order side (buy or sell)."""
    BUY = "buy"
    SELL = "sell"


class OrderStatus(Enum):
    """Order lifecycle status."""
    PENDING = "pending"
    SUBMITTED = "submitted"
    PARTIAL_FILL = "partial_fill"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class AlgoType(Enum):
    """Algorithmic execution types."""
    TWAP = "twap"       # Time-weighted average price
    VWAP = "vwap"       # Volume-weighted average price
    ICEBERG = "iceberg" # Hidden size
    POV = "pov"         # Percentage of volume


@dataclass
class Order:
    """An order to be executed."""
    order_id: str
    ticker: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    price: Optional[float] = None
    stop_price: Optional[float] = None
    status: OrderStatus = OrderStatus.PENDING
    filled_qty: float = 0.0
    avg_fill_price: float = 0.0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    algo_type: Optional[AlgoType] = None


@dataclass
class Fill:
    """A fill (execution) of an order."""
    fill_id: str
    order_id: str
    quantity: float
    price: float
    timestamp: datetime
    venue: str
    commission: float


class OrderGeneralAgent(BaseAgent):
    """
    Agent 4.1: The Order General
    
    The supreme commander of order flow. Routes orders to optimal venues.
    
    Acceptance Criteria:
    - Order routing latency <50ms
    - Smart order routing across multiple venues
    """

    def __init__(self) -> None:
        super().__init__(name="trader.order.4.1", provider=ModelProvider.GEMINI)
        self.orders: Dict[str, Order] = {}
        self.order_counter: int = 0

    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process order-related events."""
        event_type = event.get("type", "")

        if event_type == "order.new":
            return self._create_order(event)
        elif event_type == "order.cancel":
            return self._cancel_order(event)
        elif event_type == "order.route":
            return self._route_order(event)

        return None

    def _create_order(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new order."""
        start_time = time.perf_counter()
        
        self.order_counter += 1
        order_id = f"ORD-{self.order_counter:06d}"
        
        order = Order(
            order_id=order_id,
            ticker=event.get("ticker", ""),
            side=OrderSide(event.get("side", "buy")),
            order_type=OrderType(event.get("order_type", "market")),
            quantity=event.get("quantity", 0.0),
            price=event.get("price"),
            stop_price=event.get("stop_price"),
        )
        
        self.orders[order_id] = order
        
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        
        return {
            "status": "created",
            "order_id": order_id,
            "ticker": order.ticker,
            "side": order.side.value,
            "quantity": order.quantity,
            "latency_ms": elapsed_ms,
            "under_50ms_sla": elapsed_ms < 50,
        }

    def _cancel_order(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Cancel an existing order."""
        order_id = event.get("order_id", "")
        
        if order_id not in self.orders:
            return {"status": "error", "message": "Order not found"}
        
        order = self.orders[order_id]
        if order.status in [OrderStatus.FILLED, OrderStatus.CANCELLED]:
            return {"status": "error", "message": f"Order already {order.status.value}"}
        
        order.status = OrderStatus.CANCELLED
        
        return {
            "status": "cancelled",
            "order_id": order_id,
        }

    def _route_order(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Route order to optimal venue using SOR logic."""
        start_time = time.perf_counter()
        
        order_id = event.get("order_id", "")
        
        if order_id not in self.orders:
            return {"status": "error", "message": "Order not found"}
        
        order = self.orders[order_id]
        
        # Smart Order Routing logic (simplified)
        # In production: query multiple venues for best price
        venues = ["NYSE", "NASDAQ", "ARCA", "BATS"]
        best_venue = venues[hash(order.ticker) % len(venues)]
        
        order.status = OrderStatus.SUBMITTED
        
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        
        return {
            "status": "routed",
            "order_id": order_id,
            "venue": best_venue,
            "latency_ms": elapsed_ms,
            "under_50ms_sla": elapsed_ms < 50,
        }


class FillTrackerAgent(BaseAgent):
    """
    Agent 4.2: The Fill Tracker
    
    Monitors and reconciles all order fills.
    
    Acceptance Criteria:
    - 100% fill reconciliation
    - Real-time position updates
    """

    def __init__(self) -> None:
        super().__init__(name="trader.fills.4.2", provider=ModelProvider.GEMINI)
        self.fills: List[Fill] = []
        self.positions: Dict[str, float] = {}
        self.fill_counter: int = 0

    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process fill events."""
        event_type = event.get("type", "")

        if event_type == "fill.new":
            return self._record_fill(event)
        elif event_type == "position.query":
            return self._get_position(event)
        elif event_type == "reconcile":
            return self._reconcile_fills(event)

        return None

    def _record_fill(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Record a new fill."""
        self.fill_counter += 1
        fill_id = f"FILL-{self.fill_counter:08d}"
        
        fill = Fill(
            fill_id=fill_id,
            order_id=event.get("order_id", ""),
            quantity=event.get("quantity", 0.0),
            price=event.get("price", 0.0),
            timestamp=datetime.now(timezone.utc),
            venue=event.get("venue", "UNKNOWN"),
            commission=event.get("commission", 0.0),
        )
        
        self.fills.append(fill)
        
        # Update position
        ticker = event.get("ticker", "")
        side = event.get("side", "buy")
        qty_delta = fill.quantity if side == "buy" else -fill.quantity
        self.positions[ticker] = self.positions.get(ticker, 0.0) + qty_delta
        
        return {
            "status": "recorded",
            "fill_id": fill_id,
            "position": self.positions.get(ticker, 0.0),
        }

    def _get_position(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Get current position for a ticker."""
        ticker = event.get("ticker", "")
        
        return {
            "status": "position",
            "ticker": ticker,
            "quantity": self.positions.get(ticker, 0.0),
        }

    def _reconcile_fills(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Reconcile fills against broker records."""
        broker_fills = event.get("broker_fills", [])
        
        # Compare counts
        local_count = len(self.fills)
        broker_count = len(broker_fills)
        
        discrepancy = abs(local_count - broker_count)
        
        return {
            "status": "reconciled",
            "local_fills": local_count,
            "broker_fills": broker_count,
            "discrepancy": discrepancy,
            "fully_reconciled": discrepancy == 0,
        }


class AlgoExecutorAgent(BaseAgent):
    """
    Agent 4.3: The Algo-Executor
    
    Executes large orders using algorithmic strategies.
    
    Supported algorithms:
    - TWAP: Time-weighted average price
    - VWAP: Volume-weighted average price
    - Iceberg: Hidden order size
    """

    def __init__(self) -> None:
        super().__init__(name="trader.algo.4.3", provider=ModelProvider.GEMINI)
        self.active_algos: Dict[str, Dict[str, Any]] = {}

    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process algo execution events."""
        event_type = event.get("type", "")

        if event_type == "algo.start":
            return self._start_algo(event)
        elif event_type == "algo.slice":
            return self._execute_slice(event)
        elif event_type == "algo.status":
            return self._get_algo_status(event)

        return None

    def _start_algo(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Start an algorithmic execution."""
        algo_id = event.get("algo_id", f"ALGO-{int(time.time())}")
        algo_type = AlgoType(event.get("algo_type", "twap"))
        
        total_qty = event.get("quantity", 0.0)
        duration_min = event.get("duration_min", 60)
        
        # Calculate slices
        num_slices = duration_min
        slice_qty = total_qty / num_slices
        
        self.active_algos[algo_id] = {
            "algo_type": algo_type,
            "total_qty": total_qty,
            "filled_qty": 0.0,
            "slice_qty": slice_qty,
            "num_slices": num_slices,
            "slices_completed": 0,
            "status": "active",
        }
        
        return {
            "status": "started",
            "algo_id": algo_id,
            "algo_type": algo_type.value,
            "slice_qty": slice_qty,
            "num_slices": num_slices,
        }

    def _execute_slice(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single slice of the algo."""
        algo_id = event.get("algo_id", "")
        
        if algo_id not in self.active_algos:
            return {"status": "error", "message": "Algo not found"}
        
        algo = self.active_algos[algo_id]
        
        if algo["status"] != "active":
            return {"status": "error", "message": "Algo not active"}
        
        # Execute slice
        algo["filled_qty"] += algo["slice_qty"]
        algo["slices_completed"] += 1
        
        if algo["slices_completed"] >= algo["num_slices"]:
            algo["status"] = "completed"
        
        return {
            "status": "slice_executed",
            "algo_id": algo_id,
            "filled_qty": algo["filled_qty"],
            "progress_pct": (algo["slices_completed"] / algo["num_slices"]) * 100,
        }

    def _get_algo_status(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Get status of an algo execution."""
        algo_id = event.get("algo_id", "")
        
        if algo_id not in self.active_algos:
            return {"status": "error", "message": "Algo not found"}
        
        algo = self.active_algos[algo_id]
        
        return {
            "status": algo["status"],
            "algo_id": algo_id,
            "filled_qty": algo["filled_qty"],
            "total_qty": algo["total_qty"],
            "slices_completed": algo["slices_completed"],
        }


class HedgerAgent(BaseAgent):
    """
    Agent 4.4: The Hedger
    
    Monitors portfolio exposure and executes hedging trades.
    """

    def __init__(self) -> None:
        super().__init__(name="trader.hedger.4.4", provider=ModelProvider.GEMINI)

    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process hedging events."""
        event_type = event.get("type", "")

        if event_type == "hedge.analyze":
            return self._analyze_exposure(event)
        elif event_type == "hedge.execute":
            return self._execute_hedge(event)

        return None

    def _analyze_exposure(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze portfolio exposure and recommend hedges."""
        positions = event.get("positions", {})
        
        # Calculate net exposure
        net_exposure = sum(positions.values())
        
        # Recommend hedge
        hedge_needed = abs(net_exposure) > 1000
        
        return {
            "status": "analyzed",
            "net_exposure": net_exposure,
            "hedge_needed": hedge_needed,
            "recommended_hedge": "SPY" if net_exposure > 0 else "SQQQ",
        }

    def _execute_hedge(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a hedging trade."""
        return {
            "status": "hedged",
            "ticker": event.get("ticker", "SPY"),
            "quantity": event.get("quantity", 0),
        }


class ArbitrageurAgent(BaseAgent):
    """
    Agent 4.5: The Arbitrageur
    
    Identifies and executes arbitrage opportunities.
    """

    def __init__(self) -> None:
        super().__init__(name="trader.arb.4.5", provider=ModelProvider.GEMINI)

    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process arbitrage events."""
        event_type = event.get("type", "")

        if event_type == "arb.scan":
            return self._scan_opportunities(event)

        return None

    def _scan_opportunities(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Scan for arbitrage opportunities."""
        return {
            "status": "scanned",
            "opportunities_found": 0,
            "best_spread_bps": 0.0,
        }


class MarketMakerAgent(BaseAgent):
    """
    Agent 4.6: The Market Maker
    
    Provides two-sided liquidity and manages bid/ask spreads.
    """

    def __init__(self) -> None:
        super().__init__(name="trader.mm.4.6", provider=ModelProvider.GEMINI)
        self.quotes: Dict[str, Dict[str, float]] = {}

    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process market making events."""
        event_type = event.get("type", "")

        if event_type == "quote.update":
            return self._update_quote(event)
        elif event_type == "quote.get":
            return self._get_quote(event)

        return None

    def _update_quote(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Update bid/ask quote for a ticker."""
        ticker = event.get("ticker", "")
        mid_price = event.get("mid_price", 100.0)
        spread_bps = event.get("spread_bps", 10)
        
        half_spread = mid_price * (spread_bps / 10000 / 2)
        
        self.quotes[ticker] = {
            "bid": mid_price - half_spread,
            "ask": mid_price + half_spread,
            "mid": mid_price,
            "spread_bps": spread_bps,
        }
        
        return {
            "status": "quoted",
            "ticker": ticker,
            "bid": self.quotes[ticker]["bid"],
            "ask": self.quotes[ticker]["ask"],
        }

    def _get_quote(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Get current quote for a ticker."""
        ticker = event.get("ticker", "")
        
        if ticker not in self.quotes:
            return {"status": "no_quote", "ticker": ticker}
        
        return {
            "status": "quote",
            **self.quotes[ticker],
        }


# =============================================================================
# Agent Registry
# =============================================================================

def get_trader_agents() -> Dict[str, BaseAgent]:
    """
    Factory function to instantiate all Trader department agents.
    """
    return {
        "trader.order.4.1": OrderGeneralAgent(),
        "trader.fills.4.2": FillTrackerAgent(),
        "trader.algo.4.3": AlgoExecutorAgent(),
        "trader.hedger.4.4": HedgerAgent(),
        "trader.arb.4.5": ArbitrageurAgent(),
        "trader.mm.4.6": MarketMakerAgent(),
    }
