import logging
from decimal import Decimal
from services.lending.stock_lending_svc import StockLendingService

logger = logging.getLogger(__name__)

def calc_capacity(symbol: str, value: str, vol: float = 20.0):
    """
    CLI Handler for borrowing capacity check.
    """
    service = StockLendingService()
    val = Decimal(value.replace(',', ''))
    res = service.calculate_borrowing_power(symbol, val, vol)
    
    print("\n" + "="*50)
    print(f"          STOCK-BASED LENDING CAPACITY")
    print("="*50)
    print(f"Asset Symbol:    {symbol}")
    print(f"Position Value:  ${val:,.2f}")
    print(f"Implied Vol:     {vol}%")
    print("-" * 50)
    print(f"Max LTV:         {res['max_ltv']*100}%")
    print(f"Borrow Limit:    ${res['available_liquidity']:,.2f}")
    print(f"Risk Bucket:     {res['vol_risk_bucket']}")
    print("="*50 + "\n")

def analyze_spread(value: str, basis: str):
    """
    CLI Handler for Borrow vs Sell analysis.
    """
    service = StockLendingService()
    val = Decimal(value.replace(',', ''))
    bs = Decimal(basis.replace(',', ''))
    
    res = service.analyze_borrow_vs_sell(
        position_value=val,
        cost_basis=bs,
        cap_gains_rate=Decimal('0.20'),
        loan_interest_rate=Decimal('0.06')
    )
    
    print("\n" + "="*50)
    print("          BORROW VS SELL ANALYSIS")
    print("="*50)
    print(f"One-Time Tax (Sell):  ${res['one_time_tax_cost']:,.2f}")
    print(f"Annual Interest:      ${res['annual_loan_interest']:,.2f}")
    print(f"Break-Even Time:      {res['breakeven_years']} years")
    print("-" * 50)
    print(f"RECOMMENDATION:       {res['recommendation']}")
    print("="*50 + "\n")
