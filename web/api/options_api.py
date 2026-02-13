"""
==============================================================================
FILE: web/api/options_api.py
ROLE: Options API Endpoints (FastAPI)
PURPOSE: REST endpoints for options strategy building and analytics.
==============================================================================
"""

from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional, List
from pydantic import BaseModel
import logging

from web.auth_utils import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/options", tags=["Options"])


class LegModel(BaseModel):
    option_type: str  # 'call' or 'put'
    strike: float
    expiration: str
    quantity: int
    action: str  # 'buy' or 'sell'


class StrategyRequest(BaseModel):
    strategy_name: str
    underlying_symbol: str
    legs: List[LegModel] = []
    strategy_type: str = "custom"


class TemplateRequest(BaseModel):
    template_name: str
    underlying_symbol: str
    current_price: float
    expiration: str


class AnalysisRequest(BaseModel):
    underlying_price: float
    days_to_expiration: int
    volatility: float = 0.20


# Mock options chain data
def generate_mock_chain(symbol: str):
    """Generate mock options chain."""
    return {
        "symbol": symbol,
        "underlying_price": 175.50,
        "expirations": ["2026-02-21", "2026-03-21", "2026-04-18"],
        "chains": {
            "2026-02-21": {
                "calls": [
                    {"strike": 170, "bid": 6.50, "ask": 6.70, "iv": 0.22, "delta": 0.65, "volume": 1250},
                    {"strike": 175, "bid": 3.80, "ask": 4.00, "iv": 0.21, "delta": 0.50, "volume": 2100},
                    {"strike": 180, "bid": 1.90, "ask": 2.10, "iv": 0.20, "delta": 0.35, "volume": 1800}
                ],
                "puts": [
                    {"strike": 170, "bid": 1.20, "ask": 1.40, "iv": 0.23, "delta": -0.35, "volume": 980},
                    {"strike": 175, "bid": 3.30, "ask": 3.50, "iv": 0.22, "delta": -0.50, "volume": 1500},
                    {"strike": 180, "bid": 6.20, "ask": 6.40, "iv": 0.21, "delta": -0.65, "volume": 750}
                ]
            }
        }
    }


@router.get("/chain")
async def get_options_chain(
    symbol: str = Query("AAPL"),
    expiration: Optional[str] = Query(None)
):
    """Get options chain for symbol."""
    chain = generate_mock_chain(symbol)
    return {
        "success": True,
        "data": chain
    }


@router.post("/strategy/create")
async def create_strategy(request: StrategyRequest):
    """Create a new options strategy."""
    return {
        "success": True,
        "data": {
            "strategy_id": f"strat_{request.underlying_symbol.lower()}_001",
            "strategy_name": request.strategy_name,
            "underlying_symbol": request.underlying_symbol,
            "legs": [leg.model_dump() for leg in request.legs],
            "strategy_type": request.strategy_type,
            "created_at": "2026-02-03T10:00:00Z"
        }
    }


@router.post("/strategy/template")
async def create_from_template(request: TemplateRequest):
    """Create strategy from template."""
    # Generate legs based on template
    templates = {
        "iron_condor": [
            {"option_type": "put", "strike": request.current_price * 0.95, "action": "sell"},
            {"option_type": "put", "strike": request.current_price * 0.90, "action": "buy"},
            {"option_type": "call", "strike": request.current_price * 1.05, "action": "sell"},
            {"option_type": "call", "strike": request.current_price * 1.10, "action": "buy"}
        ],
        "covered_call": [
            {"option_type": "call", "strike": request.current_price * 1.05, "action": "sell"}
        ],
        "protective_put": [
            {"option_type": "put", "strike": request.current_price * 0.95, "action": "buy"}
        ]
    }
    
    legs = templates.get(request.template_name.lower(), [])
    
    return {
        "success": True,
        "data": {
            "strategy_id": f"strat_{request.underlying_symbol.lower()}_tpl",
            "template_name": request.template_name,
            "underlying_symbol": request.underlying_symbol,
            "current_price": request.current_price,
            "expiration": request.expiration,
            "legs": legs
        }
    }


@router.get("/strategy/{strategy_id}/greeks")
async def get_greeks(
    strategy_id: str,
    underlying_price: float = Query(175.0),
    days_to_expiration: int = Query(30),
    volatility: float = Query(0.20)
):
    """Calculate Greeks for strategy."""
    return {
        "success": True,
        "data": {
            "strategy_id": strategy_id,
            "greeks": {
                "delta": 0.15,
                "gamma": 0.02,
                "theta": -0.08,
                "vega": 0.25,
                "rho": 0.01
            },
            "underlying_price": underlying_price,
            "days_to_expiration": days_to_expiration,
            "volatility": volatility
        }
    }


@router.get("/strategy/{strategy_id}/pnl")
async def get_pnl(
    strategy_id: str,
    underlying_price: float = Query(175.0),
    days_to_expiration: int = Query(30)
):
    """Calculate P&L for strategy."""
    return {
        "success": True,
        "data": {
            "strategy_id": strategy_id,
            "pnl_at_price": 250.00,
            "max_profit": 500.00,
            "max_loss": -300.00,
            "breakeven_prices": [168.50, 181.50],
            "probability_of_profit": 0.65
        }
    }


@router.post("/strategy/{strategy_id}/analyze")
async def analyze_strategy(strategy_id: str, request: AnalysisRequest):
    """Complete strategy analysis."""
    return {
        "success": True,
        "data": {
            "strategy_id": strategy_id,
            "underlying_price": request.underlying_price,
            "days_to_expiration": request.days_to_expiration,
            "volatility": request.volatility,
            "greeks": {
                "delta": 0.15, "gamma": 0.02, "theta": -0.08, "vega": 0.25
            },
            "pnl": {
                "current": 150.00,
                "max_profit": 500.00,
                "max_loss": -300.00
            },
            "risk_metrics": {
                "probability_of_profit": 0.65,
                "risk_reward_ratio": 1.67
            }
        }
    }


@router.get("/{ticker}/greeks/surface")
async def get_greeks_surface(ticker: str):
    """3D Greeks Surface Data."""
    strikes = [150, 160, 170, 180, 190, 200]
    expiries = ["2026-03-20", "2026-04-17", "2026-05-15", "2026-06-19"]
    data = []
    
    import math
    for exp in expiries:
        for strike in strikes:
            # Mock surface shape
            normalized = (strike - 175) / 50.0
            delta = 0.5 + (0.5 * math.tanh(normalized))
            gamma = 0.05 * math.exp(-0.5 * normalized**2)
            vega = 0.2 * math.exp(-0.2 * normalized**2)
            
            data.append({
                "expiry": exp,
                "strike": strike,
                "delta": delta,
                "gamma": gamma,
                "vega": vega
            })
    return {"success": True, "data": data}


@router.get("/portfolio/greeks")
async def get_portfolio_greeks():
    """Portfolio-level Greeks."""
    return {
        "success": True,
        "data": {
            "net_delta": 125.50,
            "net_gamma": 4.20,
            "net_theta": -15.75,
            "net_vega": 210.00,
            "positions": [
                {"symbol": "AAPL", "delta": 50.0, "gamma": 2.0, "theta": -5.0, "vega": 100.0},
                {"symbol": "TSLA", "delta": 75.5, "gamma": 2.2, "theta": -10.75, "vega": 110.0}
            ]
        }
    }


@router.post("/scenarios")
async def run_scenario(request: AnalysisRequest):
    """P&L Scenario Analysis."""
    scenarios = []
    # Generate -20% to +20% price moves
    base_price = request.underlying_price
    for i in range(-20, 21, 5):
        pct = i / 100.0
        price = base_price * (1 + pct)
        pnl = (price - base_price) * 100 * 0.5 # Mock PnL
        scenarios.append({
            "price_pct": i,
            "price": price,
            "pnl": pnl,
            "delta_proj": 0.5 + (pct * 2)
        })
    return {"success": True, "data": scenarios}


@router.get("/{ticker}/iv-rank")
async def get_iv_rank(ticker: str):
    """IV Rank and Percentile."""
    return {
        "success": True,
        "data": {
            "ticker": ticker,
            "current_iv": 0.24,
            "iv_rank": 35.0,
            "iv_percentile": 42.0,
            "high_52w": 0.45,
            "low_52w": 0.15,
            "term_structure": "contango"
        }
    }


@router.get("/flow")
async def get_unusual_flow(ticker: Optional[str] = None):
    """Options Flow Scanner."""
    flow = [
        {"time": "10:30:05", "ticker": "AAPL", "contract": "2026-03-20 C 180", "premium": 1500000, "type": "SWEEP", "sentiment": "BULLISH"},
        {"time": "10:32:12", "ticker": "NVDA", "contract": "2026-02-21 P 800", "premium": 450000, "type": "BLOCK", "sentiment": "BEARISH"},
        {"time": "10:45:00", "ticker": "TSLA", "contract": "2026-06-19 C 250", "premium": 800000, "type": "SPLIT", "sentiment": "BULLISH"}
    ]
    if ticker:
        flow = [f for f in flow if f["ticker"] == ticker]
    return {"success": True, "data": flow}
