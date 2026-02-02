import logging
from decimal import Decimal
from services.trading.option_hedge_service import OptionHedgeService
from services.market_data.forced_seller_svc import ForcedSellerService

logger = logging.getLogger(__name__)

def recommend():
    """
    CLI Handler for hedging recommendations.
    """
    svc = OptionHedgeService()
    # Mock input
    res = svc.recommend_hedge("SPY", 550.0, 18.0, Decimal("150000.00"))
    
    print("\n" + "="*50)
    print("        HEDGING STRATEGY RECOMMENDATION")
    print("="*50)
    print(f"Ticker:         {res['ticker']}")
    print(f"Vol Regime:     {res['regime']}")
    print(f"Recommended:    {res['strategy'].replace('_', ' ')}")
    print("-" * 50)
    print(f"Justification:  {res['justification']}")
    print("-" * 50)
    print(f"Target Put:     ${res['strikes']['put']}")
    if res['strikes']['call']:
        print(f"Target Call:    ${res['strikes']['call']}")
    print("="*50 + "\n")

def forced_seller_status():
    """
    CLI Handler for forced seller liquidity status.
    """
    svc = ForcedSellerService()
    # Mock input
    res = svc.monitor_passive_flow("TSLA", 75.0)
    
    print("\n" + "="*50)
    print("        FORCED SELLER FRAGILITY REPORT")
    print("="*50)
    print(f"Ticker:         {res['ticker']}")
    print(f"Passive Ownership: {res['passive_concentration']}%")
    print(f"Fragility Score:   {res['fragility_score']:.2f} / 1.00")
    print("-" * 50)
    print(f"RISK LEVEL:     {res['risk_level']}")
    print(f"Impact:         {res['notes']}")
    print("="*50 + "\n")
