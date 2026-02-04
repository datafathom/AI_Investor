"""
==============================================================================
FILE: services/billing/payment_reminder_service.py
ROLE: Payment Reminder System
PURPOSE: Provides automated reminders, payment history tracking, and late
         payment alerts.

INTEGRATION POINTS:
    - BillPaymentService: Bill information
    - NotificationService: Reminder delivery
    - CalendarService: Reminder scheduling
    - PaymentReminderAPI: Reminder endpoints
    - FrontendBilling: Reminder dashboard

FEATURES:
    - Automated reminders
    - Payment history
    - Late payment alerts
    - Reminder customization

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
from schemas.billing import Bill, PaymentReminder, BillStatus
from services.billing.bill_payment_service import get_bill_payment_service
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class PaymentReminderService:
    """
    Service for payment reminders and alerts.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.bill_service = get_bill_payment_service()
        self.cache_service = get_cache_service()
        self.default_reminder_days = [7, 3, 1]  # 7 days, 3 days, 1 day before due
        
    async def create_reminder(
        self,
        bill_id: str,
        reminder_days_before: int = 7
    ) -> PaymentReminder:
        """
        Create payment reminder for bill.
        
        Args:
            bill_id: Bill identifier
            reminder_days_before: Days before due date to send reminder
            
        Returns:
            PaymentReminder object
        """
        logger.info(f"Creating reminder for bill {bill_id}")
        
        # Get bill
        bill = await self.bill_service._get_bill(bill_id)
        if not bill:
            raise ValueError(f"Bill {bill_id} not found")
        
        # Calculate reminder date
        reminder_date = bill.due_date - timedelta(days=reminder_days_before)
        
        # Determine reminder type
        days_until_due = (bill.due_date - datetime.now(timezone.utc)).days
        if days_until_due < 0:
            reminder_type = "overdue"
        elif days_until_due <= 1:
            reminder_type = "due_soon"
        else:
            reminder_type = "upcoming"
        
        reminder = PaymentReminder(
            reminder_id=f"reminder_{bill_id}_{datetime.now(timezone.utc).timestamp()}",
            bill_id=bill_id,
            reminder_date=reminder_date,
            reminder_type=reminder_type,
            sent=False
        )
        
        # Save reminder
        await self._save_reminder(reminder)
        
        return reminder
    
    async def check_due_bills(
        self,
        user_id: str
    ) -> List[Bill]:
        """
        Check for bills that are due or overdue.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of due/overdue bills
        """
        # Get upcoming bills
        bills = await self.bill_service.get_upcoming_bills(user_id, days_ahead=0)
        
        due_bills = []
        today = datetime.now(timezone.utc).date()
        
        for bill in bills:
            due_date = bill.due_date.date() if isinstance(bill.due_date, datetime) else bill.due_date
            
            if due_date <= today and bill.status == BillStatus.PENDING:
                bill.status = BillStatus.OVERDUE
                due_bills.append(bill)
        
        return due_bills
    
    async def send_reminders(
        self,
        user_id: str
    ) -> List[PaymentReminder]:
        """
        Send reminders for upcoming bills.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of reminders sent
        """
        logger.info(f"Sending reminders for user {user_id}")
        
        # Get upcoming bills
        bills = await self.bill_service.get_upcoming_bills(user_id, days_ahead=7)
        
        reminders_sent = []
        today = datetime.now(timezone.utc)
        
        for bill in bills:
            days_until_due = (bill.due_date - today).days
            
            # Check if reminder should be sent
            if days_until_due in self.default_reminder_days:
                reminder = await self.create_reminder(
                    bill.bill_id,
                    reminder_days_before=days_until_due
                )
                
                # Mark as sent (in production, actually send notification)
                reminder.sent = True
                reminder.sent_date = datetime.now(timezone.utc)
                await self._save_reminder(reminder)
                
                reminders_sent.append(reminder)
        
        return reminders_sent
    
    async def get_upcoming_reminders(
        self,
        user_id: str,
        days_ahead: int = 7
    ) -> List[PaymentReminder]:
        """
        Get upcoming reminders for user.
        
        Args:
            user_id: User identifier
            days_ahead: Number of days to look ahead
            
        Returns:
            List of PaymentReminder objects
        """
        return await self._get_reminders_from_db(user_id, days_ahead)

    async def _get_reminders_from_db(self, user_id: str, days_ahead: int) -> List[PaymentReminder]:
        """Fetch reminders from database placeholder."""
        # This would implementation database query
        return []
    
    async def _save_reminder(self, reminder: PaymentReminder):
        """Save reminder to cache."""
        cache_key = f"reminder:{reminder.bill_id}:{reminder.reminder_id}"
        self.cache_service.set(cache_key, reminder.model_dump(), ttl=86400 * 30)


# Singleton instance
_payment_reminder_service: Optional[PaymentReminderService] = None


def get_payment_reminder_service() -> PaymentReminderService:
    """Get singleton payment reminder service instance."""
    global _payment_reminder_service
    if _payment_reminder_service is None:
        _payment_reminder_service = PaymentReminderService()
    return _payment_reminder_service
