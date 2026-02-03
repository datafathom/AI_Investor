"""
scripts/runners/test_broker.py
Purpose: Test Robinhood Broker Integration.
"""

from services.broker.robinhood_service import RobinhoodService

def run_test_broker(mock: bool = False, **kwargs):
    """
    Test the Robinhood Service.
    Attempts to fetch basic account info.
    """
    mode = "MOCK" if mock else "LIVE"
    print(f"--- Testing Robinhood Broker Integration ({mode} MODE) ---")
    
    service = RobinhoodService(mock=mock)
    
    if not mock and not service.username:
        print("Warning: ROBINHOOD_USERNAME not found in env. Test will likely fail.")
    
    # Check session
    if service.login():
        print("Login: SUCCESS")
        
        # Profile check
        profile = service.get_account_profile()
        print(f"Account: {profile.get('account_number', 'N/A')}")
        print(f"Buying Power: ${profile.get('buying_power', '0.00')}")
        
        # Positions check
        positions = service.get_portfolio_positions()
        print(f"\nPositions ({len(positions)}):")
        for pos in positions:
            print(f" - {pos['symbol']}: {pos['quantity']} shares")
            
        print("\nVerified: RobinhoodService functional.")
    else:
        print("Login: FAILED")
        
    return True
