"""
Verification script for Phase 10.
Simulates trade journaling lifecycle.
"""
import sys
import uuid
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

# Create a mock session to avoid real DB connection in verification script if DB not ready
mock_session = MagicMock()

def run_verification():
    print("=== Starting Phase 10 Verification ===")
    
    # Mocking services because we might not have a live DB yet in this environment
    with patch('utils.db_sqlalchemy.sqlalchemy_manager.session_scope') as mock_scope:
        mock_scope.return_value.__enter__.return_value = mock_session
        
        from services.trade_journal_service import trade_journal_service
        from services.r_multiple_calculator import RMultipleCalculator
        from services.trade_hash_generator import TradeHashGenerator
        
        print("\n[1/3] Verifying R-Multiple Math...")
        # (covered by unit tests, but sanity check here)
        r = RMultipleCalculator.calculate(1.1000, 1.1100, 1.0950, "LONG")
        if r == 2.0:
            print("✅ R-Multiple Math Verified (1.10 -> 1.11 with 1.095 SL = 2.0R)")
        else:
            print("❌ R-Multiple Math Failed")
            return False

        print("\n[2/3] Verifying Integrity Hash...")
        trade_id = uuid.uuid4()
        trade_data = {
            'trade_id': trade_id,
            'symbol': 'EUR/USD',
            'direction': 'LONG',
            'entry_price': 1.1000,
            'stop_loss': 1.0950,
            'position_size': 100000,
            'entry_time': datetime.utcnow(),
            'agent_id': 'searcher-001',
            'trade_thesis': 'Bullish BOS'
        }
        hash1 = TradeHashGenerator.generate_hash(trade_data)
        hash2 = TradeHashGenerator.generate_hash(trade_data)
        
        if hash1 == hash2 and len(hash1) == 64:
            print(f"✅ SHA-256 Hashing verified: {hash1[:10]}...")
        else:
            print("❌ Hashing failure")
            return False

        print("\n[3/3] Simulating Trade Lifecycle...")
        print("Opening trade...")
        trade_journal_service.open_trade(trade_data)
        
        print("Closing trade at 1.1150...")
        # Mocking the query result for close_trade
        mock_entry = MagicMock()
        mock_entry.entry_price = 1.1000
        mock_entry.stop_loss = 1.0950
        mock_entry.direction = 'LONG'
        mock_entry.trade_id = trade_id
        mock_session.query.return_value.filter_by.return_value.first.return_value = mock_entry
        
        closed = trade_journal_service.close_trade(trade_id, 1.1150)
        
        if closed and mock_entry.r_multiple == 3.0:
            print(f"✅ Trade lifecycle verified. Final R-Multiple: {mock_entry.r_multiple}")
        else:
            print(f"❌ Lifecycle verification failed. R={getattr(mock_entry, 'r_multiple', 'N/A')}")
            return False

        print("\n=== Phase 10 Verification SUCCESS ===")
        return True

if __name__ == "__main__":
    success = run_verification()
    if not success:
        sys.exit(1)
