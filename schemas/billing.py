"""
==============================================================================
FILE: models/billing.py
ROLE: Bill Payment Data Models
PURPOSE: Pydantic models for bill payment tracking, reminders, and scheduling.

INTEGRATION POINTS:
    - BillPaymentService: Bill tracking and payment
    - PaymentReminderService: Reminder system
    - BillingAPI: API response models
    - FrontendBilling: Bill payment dashboard

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class BillStatus(str, Enum):
    """Bill payment status."""
    PENDING = "pending"
    SCHEDULED = "scheduled"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class RecurrenceType(str, Enum):
    """Bill recurrence types."""
    ONE_TIME = "one_time"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    CUSTOM = "custom"


class Bill(BaseModel):
    """Bill definition."""
    bill_id: str
    user_id: str
    bill_name: str
    merchant: str
    amount: float
    due_date: datetime
    status: BillStatus = BillStatus.PENDING
    recurrence: RecurrenceType = RecurrenceType.ONE_TIME
    account_id: Optional[str] = None
    category: Optional[str] = None
    notes: Optional[str] = None
    created_date: datetime
    updated_date: datetime


class PaymentReminder(BaseModel):
    """Payment reminder."""
    reminder_id: str
    bill_id: str
    reminder_date: datetime
    reminder_type: str  # "upcoming", "due_soon", "overdue"
    sent: bool = False
    sent_date: Optional[datetime] = None


class PaymentHistory(BaseModel):
    """Payment history record."""
    payment_id: str
    bill_id: str
    amount: float
    payment_date: datetime
    payment_method: str
    confirmation_number: Optional[str] = None
    status: str  # "completed", "pending", "failed"
