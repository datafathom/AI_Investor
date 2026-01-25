"""
Tests for Payment Reminder Service
Comprehensive test coverage for payment reminders and alerts
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
from services.billing.payment_reminder_service import PaymentReminderService
from models.billing import PaymentReminder, Bill


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.billing.payment_reminder_service.get_bill_payment_service'), \
         patch('services.billing.payment_reminder_service.get_cache_service'):
        return PaymentReminderService()


@pytest.mark.asyncio
async def test_create_reminder(service):
    """Test creating payment reminder."""
    bill = Bill(
        bill_id="bill_123",
        user_id="user_123",
        bill_name="Test Bill",
        merchant="Test Merchant",
        amount=100.0,
        due_date=datetime.utcnow() + timedelta(days=7),
        status="pending",
        recurrence="one_time",
        created_date=datetime.utcnow()
    )
    
    service.bill_service._get_bill = AsyncMock(return_value=bill)
    service._save_reminder = AsyncMock()
    
    result = await service.create_reminder(
        bill_id="bill_123",
        reminder_days_before=7
    )
    
    assert result is not None
    assert isinstance(result, PaymentReminder)
    assert result.bill_id == "bill_123"


@pytest.mark.asyncio
async def test_get_upcoming_reminders(service):
    """Test getting upcoming reminders."""
    service._get_reminders_from_db = AsyncMock(return_value=[
        PaymentReminder(
            reminder_id="reminder_1",
            bill_id="bill_1",
            reminder_date=datetime.utcnow() + timedelta(days=1),
            sent=False
        )
    ])
    
    result = await service.get_upcoming_reminders("user_123", days_ahead=7)
    
    assert result is not None
    assert len(result) == 1
