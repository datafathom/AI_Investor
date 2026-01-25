"""
Tests for Public API Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from models.public_api import (
    APITier,
    APIKey,
    APIUsage
)


class TestAPITierEnum:
    """Tests for APITier enum."""
    
    def test_api_tier_enum(self):
        """Test API tier enum values."""
        assert APITier.FREE == "free"
        assert APITier.PRO == "pro"
        assert APITier.ENTERPRISE == "enterprise"


class TestAPIKey:
    """Tests for APIKey model."""
    
    def test_valid_api_key(self):
        """Test valid API key creation."""
        api_key = APIKey(
            api_key_id='key_1',
            user_id='user_1',
            api_key='test_key_12345',
            tier=APITier.PRO,
            rate_limit=1000,
            usage_count=500,
            created_date=datetime.now(),
            last_used_date=datetime.now(),
            is_active=True
        )
        assert api_key.api_key_id == 'key_1'
        assert api_key.tier == APITier.PRO
        assert api_key.rate_limit == 1000
    
    def test_api_key_defaults(self):
        """Test API key with default values."""
        api_key = APIKey(
            api_key_id='key_1',
            user_id='user_1',
            api_key='test_key',
            created_date=datetime.now()
        )
        assert api_key.tier == APITier.FREE
        assert api_key.rate_limit == 100
        assert api_key.usage_count == 0
        assert api_key.is_active is True


class TestAPIUsage:
    """Tests for APIUsage model."""
    
    def test_valid_api_usage(self):
        """Test valid API usage creation."""
        usage = APIUsage(
            usage_id='usage_1',
            api_key_id='key_1',
            endpoint='/api/v1/market/quote',
            timestamp=datetime.now(),
            response_time_ms=150.5,
            status_code=200
        )
        assert usage.usage_id == 'usage_1'
        assert usage.endpoint == '/api/v1/market/quote'
        assert usage.response_time_ms == 150.5
        assert usage.status_code == 200
