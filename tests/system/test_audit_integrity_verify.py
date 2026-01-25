
import pytest
from unittest.mock import MagicMock, patch
from services.system.audit_integrity_service import get_audit_integrity_service

def test_verify_chain_integrity():
    # Helper to create mock records
    def mk_record(id, prev_hash, my_hash):
        # 0:id, 1:uid, 2:type, 3:details, 4:created_at, 5:prev_hash, 6:verification_hash
        return (id, "u1", "ACT", {}, "2023-01-01", prev_hash, my_hash)
    
    service = get_audit_integrity_service()
    
    with patch('services.system.audit_integrity_service.get_database_manager') as mock_db:
        mock_cursor = MagicMock()
        mock_db.return_value.pg_cursor.return_value.__enter__.return_value = mock_cursor
        
        # Scenario 1: Valid Chain
        # R1: Hash = H(R1_data, GENESIS)
        # R2: Prev=H(R1), Hash = H(R2_data, H(R1))
        # Note: Logic checks curr.previous_hash == prev.verification_hash
        # Records are fetched ORDER BY created_at DESC (Newest first)
        # So records = [R2, R1]
        
        # Let's mock the calculate_hash to just return "HASH(id, prev_hash)" to be simple
        with patch.object(service, 'calculate_hash', side_effect=lambda d, p: f"HASH({d['id']},{p})"):
            
            # R1
            r1_prev = "GENESIS"
            r1_hash = "HASH(1,GENESIS)"
            # R2
            r2_prev = r1_hash
            r2_hash = "HASH(2,HASH(1,GENESIS))"
            
            mock_cursor.fetchall.return_value = [
                mk_record(2, r2_prev, r2_hash),
                mk_record(1, r1_prev, r1_hash)
            ]
            
            assert service.verify_chain() is True
            
        # Scenario 2: Broken Link
        # R2.prev_hash != R1.hash
        mock_cursor.fetchall.return_value = [
            mk_record(2, "WRONG_HASH", r2_hash),
            mk_record(1, r1_prev, r1_hash)
        ]
        assert service.verify_chain() is False

