import pytest
from unittest.mock import MagicMock
from services.system.identity_service import IdentityService

class TestIdentityService:
    @pytest.fixture
    def service(self):
        # Reset singleton logic if necessary or just use the instance
        return IdentityService()

    def test_singleton_pattern(self):
        s1 = IdentityService()
        s2 = IdentityService()
        assert s1 is s2

    def test_calculate_trust_score(self, service):
        # Case 1: Minimal data
        score1 = service.calculate_trust_score("user1", {}, {})
        assert score1 == 0

        # Case 2: Social Verified
        score2 = service.calculate_trust_score("user1", {}, {"email": "test@test.com", "verified": True})
        assert score2 == 30 # 20 (email) + 10 (verified)

        # Case 3: Full Profile
        plaid_data = {
            "names": ["John"],
            "addresses": ["123 St"],
            "confidence": 0.9
        }
        score3 = service.calculate_trust_score("user1", plaid_data, {"verified": True, "email": "x"})
        # 30 (social) + 30 (name) + 20 (addr) + 20 (conf) = 100
        assert score3 == 100

    def test_reconcile_identity_structure(self, service):
        # Test that the method returns the expected structure even with mock data
        result = service.reconcile_identity("test_user_123")
        
        assert "profile" in result
        assert "trust_score" in result
        assert "sources" in result
        
        profile = result["profile"]
        assert "legal_name" in profile
        assert "kyc_status" in profile
        assert profile["kyc_status"] in ["verified", "pending"]
