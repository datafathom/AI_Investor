"""
Tests for Billing Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from schemas.billing import (
    BillStatus,
    RecurrenceType,
    Bill,
    PaymentReminder,
    PaymentHistory
)


class TestBillEnums:
    """Tests for bill enums."""
    
    def test_bill_status_enum(self):
        """Test bill status enum values."""
        assert BillStatus.PENDING == "pending"
        assert BillStatus.PAID == "paid"
        assert BillStatus.OVERDUE == "overdue"
    
    def test_recurrence_type_enum(self):
        """Test recurrence type enum values."""
        assert RecurrenceType.ONE_TIME == "one_time"
        assert RecurrenceType.MONTHLY == "monthly"
        assert RecurrenceType.YEARLY == "yearly"


class TestBill:
    """Tests for Bill model."""
    
    def test_valid_bill(self):
        """Test valid bill creation."""
        bill = Bill(
            bill_id='bill_1',
            user_id='user_1',
            bill_name='Electric Bill',
            merchant='Utility Company',
            amount=150.0,
            due_date=datetime(2024, 12, 31),
            status=BillStatus.PENDING,
            recurrence=RecurrenceType.MONTHLY,
            account_id='account_1',
            category='utilities',
            notes=None,
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert bill.bill_id == 'bill_1'
        assert bill.amount == 150.0
        assert bill.status == BillStatus.PENDING
    
    def test_bill_defaults(self):
        """Test bill with default values."""
        bill = Bill(
            bill_id='bill_1',
            user_id='user_1',
            bill_name='Test Bill',
            merchant='Test Merchant',
            amount=100.0,
            due_date=datetime(2024, 12, 31),
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert bill.status == BillStatus.PENDING
        assert bill.recurrence == RecurrenceType.ONE_TIME


class TestPaymentReminder:
    """Tests for PaymentReminder model."""
    
    def test_valid_payment_reminder(self):
        """Test valid payment reminder creation."""
        reminder = PaymentReminder(
            reminder_id='reminder_1',
            bill_id='bill_1',
            reminder_date=datetime(2024, 12, 28),
            reminder_type='due_soon',
            sent=False,
            sent_date=None
        )
        assert reminder.reminder_id == 'reminder_1'
        assert reminder.reminder_type == 'due_soon'
        assert reminder.sent is False


class TestPaymentHistory:
    """Tests for PaymentHistory model."""
    
    def test_valid_payment_history(self):
        """Test valid payment history creation."""
        history = PaymentHistory(
            payment_id='payment_1',
            bill_id='bill_1',
            amount=150.0,
            payment_date=datetime.now(),
            payment_method='credit_card',
            confirmation_number='CONF123',
            status='completed'
        )
        assert history.payment_id == 'payment_1'
        assert history.amount == 150.0
        assert history.status == 'completed'
