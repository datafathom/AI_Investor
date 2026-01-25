"""
Tests for Compliance Engine
Comprehensive test coverage for compliance checking and violation detection
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.compliance.compliance_engine import ComplianceEngine
from models.compliance import ComplianceRule, ComplianceViolation, ViolationSeverity


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.compliance.compliance_engine.get_cache_service'):
        return ComplianceEngine()


@pytest.fixture
def mock_transaction():
    """Mock transaction."""
    return {
        'symbol': 'AAPL',
        'quantity': 1000,
        'price': 150.0,
        'transaction_type': 'buy',
        'user_id': 'user_123'
    }


@pytest.mark.asyncio
async def test_check_compliance(service, mock_transaction):
    """Test compliance checking."""
    rule = ComplianceRule(
        rule_id="rule_1",
        rule_name="Position Limit",
        regulation="SEC",
        rule_logic="quantity <= 10000"
    )
    service.rules["rule_1"] = rule
    service._evaluate_rule = AsyncMock(return_value=False)  # No violation
    service._save_violation = AsyncMock()
    
    result = await service.check_compliance(
        user_id="user_123",
        transaction=mock_transaction
    )
    
    assert result is not None
    assert isinstance(result, list)
    assert len(result) == 0  # No violations


@pytest.mark.asyncio
async def test_check_compliance_with_violation(service, mock_transaction):
    """Test compliance checking with violation."""
    rule = ComplianceRule(
        rule_id="rule_1",
        rule_name="Position Limit",
        regulation="SEC",
        rule_logic="quantity <= 100"
    )
    service.rules["rule_1"] = rule
    service._evaluate_rule = AsyncMock(return_value=True)  # Violation detected
    service._save_violation = AsyncMock()
    
    result = await service.check_compliance(
        user_id="user_123",
        transaction=mock_transaction
    )
    
    assert result is not None
    assert len(result) == 1
    assert isinstance(result[0], ComplianceViolation)


@pytest.mark.asyncio
async def test_get_violations(service):
    """Test getting user violations."""
    service._get_violations_from_db = AsyncMock(return_value=[
        ComplianceViolation(
            violation_id="violation_1",
            rule_id="rule_1",
            user_id="user_123",
            severity=ViolationSeverity.MEDIUM,
            description="Position limit exceeded",
            detected_date=datetime.utcnow(),
            status="open"
        )
    ])
    
    result = await service.get_violations("user_123")
    
    assert result is not None
    assert len(result) == 1
