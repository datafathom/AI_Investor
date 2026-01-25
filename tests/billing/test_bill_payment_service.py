"""
Tests for Bill Payment Service
Comprehensive test coverage for bill tracking, payment scheduling, and history
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
from services.billing.bill_payment_service import BillPaymentService
from models.billing import Bill, BillStatus, RecurrenceType


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.billing.bill_payment_service.get_cache_service'):
        return BillPaymentService()


@pytest.mark.asyncio
async def test_create_bill(service):
    """Test bill creation."""
    service._save_bill = AsyncMock()
    
    result = await service.create_bill(
        user_id="user_123",
        bill_name="Electric Bill",
        merchant="Electric Company",
        amount=150.0,
        due_date=datetime(2024, 2, 1),
        recurrence="monthly"
    )
    
    assert result is not None
    assert isinstance(result, Bill)
    assert result.user_id == "user_123"
    assert result.amount == 150.0
    assert result.status == BillStatus.PENDING


@pytest.mark.asyncio
async def test_schedule_payment(service):
    """Test payment scheduling."""
    bill = Bill(
        bill_id="bill_123",
        user_id="user_123",
        bill_name="Test Bill",
        merchant="Test Merchant",
        amount=100.0,
        due_date=datetime(2024, 2, 1),
        status=BillStatus.PENDING,
        recurrence=RecurrenceType.ONE_TIME,
        created_date=datetime.utcnow()
    )
    
    service._get_bill = AsyncMock(return_value=bill)
    service._execute_payment = AsyncMock(return_value={'status': 'scheduled', 'payment_id': 'pay_123'})
    service._update_bill = AsyncMock()
    
    result = await service.schedule_payment(
        bill_id="bill_123",
        payment_date=datetime(2024, 1, 28)
    )
    
    assert result is not None
    assert 'payment_id' in result or hasattr(result, 'payment_id')


@pytest.mark.asyncio
async def test_get_upcoming_bills(service):
    """Test getting upcoming bills."""
    service._get_bills_from_db = AsyncMock(return_value=[
        Bill(
            bill_id="bill_1",
            user_id="user_123",
            bill_name="Bill 1",
            merchant="Merchant 1",
            amount=100.0,
            due_date=datetime.utcnow() + timedelta(days=5),
            status=BillStatus.PENDING,
            recurrence=RecurrenceType.ONE_TIME,
            created_date=datetime.utcnow()
        )
    ])
    
    result = await service.get_upcoming_bills(
        user_id="user_123",
        days_ahead=30
    )
    
    assert result is not None
    assert len(result) == 1


@pytest.mark.asyncio
async def test_create_bill_error_handling(service):
    """Test error handling in bill creation."""
    service._save_bill = AsyncMock(side_effect=Exception("Database error"))
    
    with pytest.raises(Exception):
        await service.create_bill(
            user_id="user_123",
            bill_name="Error Bill",
            merchant="Error Merchant",
            amount=100.0,
            due_date=datetime.utcnow()
        )
