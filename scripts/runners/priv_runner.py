import logging
from decimal import Decimal
from services.private_markets.premium_optimizer import PremiumOptimizer

logger = logging.getLogger(__name__)

def calc_premium():
    """
    CLI Handler for illiquidity premium calculation.
    """
    opt = PremiumOptimizer()
    res = opt.calculate_illiquidity_premium(Decimal('0.15'), Decimal('0.11'))
    
    print("\n" + "="*50)
    print("          ILLIQUIDITY PREMIUM ANALYSIS")
    print("="*50)
    print(f"Private IRR:      15.00%")
    print(f"Public Equiv:     11.00%")
    print("-" * 50)
    print(f"PREMIUM (BPS):    {res['premium_bps']} bps")
    print(f"Sufficiency:      {res['is_sufficient']}")
    print("="*50 + "\n")

def unsmooth():
    """
    CLI Handler for return unsmoothing.
    """
    opt = PremiumOptimizer()
    smoothed = [0.02, 0.022, 0.021, 0.023, 0.025]
    unsmoothed = opt.unsmooth_returns(smoothed)
    
    print("\n" + "="*50)
    print("          RETURN UNSMOOTHING (GELTNER)")
    print("="*50)
    print(f"Smoothed:   {smoothed}")
    print(f"Unsmoothed: {unsmoothed}")
    print("="*50 + "\n")
