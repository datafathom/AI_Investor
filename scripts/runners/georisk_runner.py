import logging
import json
from services.risk.geopolitical_risk_svc import GeopoliticalRiskService
from services.risk.commodity_tracker import CommodityExposureTracker

logger = logging.getLogger(__name__)

def sim_war():
    """
    CLI Handler for Total War portfolio simulation.
    """
    # Mock allocation
    allocation = {
        "Equities": 0.60,
        "Bonds": 0.20,
        "Gold": 0.10,
        "Commodities": 0.10
    }
    
    svc = GeopoliticalRiskService()
    res = svc.simulate_total_war(allocation)
    
    print("\n" + "="*50)
    print("        GEOPOLITICAL 'TOTAL WAR' SIMULATOR")
    print("="*50)
    print(f"Scenario:            {res['scenario']}")
    print(f"Risk Tier:           {res['risk_tier']}")
    print("-" * 50)
    print(f"PROJECTED IMPACT:    {res['total_portfolio_impact']:.2%}")
    print("-" * 50)
    print("Asset Breakdown:")
    for asset, impact in res['asset_breakdown'].items():
        print(f" - {asset:12}: {impact:+.2%}")
    print("="*50 + "\n")

def fear_score():
    """
    CLI Handler for geopolitical fear scoring.
    """
    # Mock market data
    vix = 35.0
    pc_ratio = 1.4
    sentiment = 0.2
    
    svc = GeopoliticalRiskService()
    res = svc.calculate_geopolitical_fear_score(vix, pc_ratio, sentiment)
    
    print("\n" + "="*50)
    print("        GEOPOLITICAL FEAR & EFFICIENCY")
    print("="*50)
    print(f"Fear Score:          {res['fear_score']:.2f} / 1.00")
    print(f"Market Efficiency:   {res['market_efficiency']}")
    print("-" * 50)
    print(f"RECOMMENDATION:      {res['recommendation']}")
    print("="*50 + "\n")
