import logging
import uuid
from decimal import Decimal
from datetime import date
from services.risk.valuation_gap_analyzer import ValuationGapAnalyzer
from services.risk.advanced_risk_metrics_service import get_risk_metrics_service
from services.risk.risk_monitor import get_risk_monitor

logger = logging.getLogger(__name__)

def calc_gap(asset_name: str, nav: float, ticker: str):
    """
    CLI Handler for valuation gap analysis.
    """
    vga = ValuationGapAnalyzer()
    res = vga.calculate_gap(asset_name, Decimal(str(nav)), date.today(), ticker) # Wait, date is not imported
    
    print("\n" + "="*50)
    print("          VALUATION GAP ANALYSIS")
    print("="*50)
    print(f"Asset:            {res['asset']}")
    print(f"Reported NAV:     ${res['reported_nav']:,.2f}")
    print(f"Proxy Ticker:     {res['proxy_ticker']}")
    print(f"Proxy Return:     {res['proxy_performance']:.1%}")
    print("-" * 50)
    print(f"Implied Value:    ${res['implied_true_value']:,.2f}")
    print(f"Valuation Gap:    ${res['valuation_gap']:,.2f} ({res['gap_percentage']:.1%})")
    print(f"Risk Verdict:     {res['risk_flag']}")
    print("="*50 + "\n")

def true_vol(vol: float, gap: float, lockup: int):
    """
    CLI Handler for hidden volatility scoring.
    """
    arms = get_risk_metrics_service()
    res = arms.calculate_hidden_volatility_score(vol, gap, lockup)
    
    print("\n" + "="*50)
    print("          TRUE VOLATILITY (HIDDEN RISK)")
    print("="*50)
    print(f"Reported Vol:     {res['reported_volatility']:.1%}")
    print(f"Valuation Gap:    {res['valuation_gap_pct']:.1%}")
    print(f"Lockup Period:    {res['liquidity_lockup_years']} Years")
    print("-" * 50)
    print(f"True Volatility:  {res['true_volatility']:.1%}")
    print(f"Risk Score:       {res['hidden_vol_score']}/100")
    print(f"Status:           {res['status']}")
    print("="*50 + "\n")

if __name__ == "__main__":
    from datetime import date # Added import
    calc_gap("SpaceX PE", 25000000.0, "QQQ")
