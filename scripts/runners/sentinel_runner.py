import logging
from decimal import Decimal
from services.market_data.fund_flow_service import FundFlowService
from services.alternative.pe_secondary_service import PESecondaryService
from services.tax.tax_harvest_service import TaxHarvestService

logger = logging.getLogger(__name__)

def whale_watch(ticker: str):
    """
    CLI Handler for tracking institutional 'Whale' selling.
    """
    svc = FundFlowService()
    # Mock 13F data
    mock_data = [
        {"holder": "BlackRock", "change": -5000000},
        {"holder": "Vanguard", "change": -8000000},
        {"holder": "Renaissance", "change": -2000000}
    ]
    res = svc.track_whale_selling(ticker, mock_data)
    
    print("\n" + "="*50)
    print(f"        SENTINEL WHALE WATCH: {ticker}")
    print("="*50)
    print(f"Selling Pressure:    {res['total_whale_sold']:,.0f} shares")
    print(f"Risk Level:          {res['risk_level']}")
    print(f"Signal:              {res['signal']}")
    print("-" * 50)
    print("Major Sellers:")
    for seller in res['major_sellers']:
        print(f" - {seller}")
    print("="*50 + "\n")

def pe_status(fund_id: str):
    """
    CLI Handler for PE secondary market status.
    """
    svc = PESecondaryService()
    res = svc.calculate_nav_discount(Decimal("100.00"), Decimal("75.00"))
    win = svc.track_redemption_window(fund_id, "2026-12-31")
    
    print("\n" + "="*50)
    print(f"        PE SECONDARY STATUS: {fund_id}")
    print("="*50)
    print(f"Discount to NAV:     {res['discount_pct']}%")
    print(f"Opportunity:         {res['opportunity_rank']}")
    print("-" * 50)
    print(f"Redemption Window:   {'[OPEN]' if win['is_redemption_open'] else '[CLOSED]'}")
    print(f"Lockup Expiry:       {win['lockup_expiry']}")
    print(f"Days to Exit:        {win['days_until_exit']}")
    print("="*50 + "\n")

def harvest_scan():
    """
    CLI Handler for tax-loss harvesting scan.
    """
    svc = TaxHarvestService()
    # Mock portfolio
    portfolio = [
        {"ticker": "NVDA", "cost_basis": 150.0, "current_price": 120.0},
        {"ticker": "TSLA", "cost_basis": 250.0, "current_price": 180.0},
        {"ticker": "AAPL", "cost_basis": 180.0, "current_price": 190.0}
    ]
    opportunities = svc.hunt_harvest_opportunity(portfolio)
    
    print("\n" + "="*50)
    print("        TAX-LOSS HARVESTING SCAN")
    print("="*50)
    if not opportunities:
        print("No harvesting opportunities found above 10% threshold.")
    else:
        for opp in opportunities:
            print(f"Ticker:         {opp['ticker']}")
            print(f"Unrealized Loss: ${opp['unrealized_loss']:,.2f}")
            print(f"Loss %:         {opp['loss_pct']}%")
            print(f"Wash Sale Safe: {opp['wash_sale_safe_date']}")
            print("-" * 50)
    print("="*50 + "\n")
