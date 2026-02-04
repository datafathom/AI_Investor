"""
Billing API - FastAPI Router
REST endpoints for bill payment tracking and reminders.
"""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel

from web.auth_utils import get_current_user
from services.billing.bill_payment_service import get_bill_payment_service
from services.billing.payment_reminder_service import get_payment_reminder_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/billing", tags=["Billing"])

class BillCreateRequest(BaseModel):
    user_id: str
    bill_name: str
    merchant: str
    amount: float
    due_date: str
    recurrence: str = 'one_time'
    account_id: Optional[str] = None

class PaymentScheduleRequest(BaseModel):
    bill_id: str
    payment_date: str
    payment_method: str = 'bank_transfer'

class ReminderCreateRequest(BaseModel):
    bill_id: str
    reminder_days_before: int = 7

@router.post('/bill/create')
async def create_bill(
    request_data: BillCreateRequest,
    current_user: dict = Depends(get_current_user),
    service = Depends(get_bill_payment_service)
):
    """Create a new bill."""
    try:
        due_date = datetime.strptime(request_data.due_date, '%Y-%m-%d')
        bill = await service.create_bill(
            user_id=request_data.user_id,
            bill_name=request_data.bill_name,
            merchant=request_data.merchant,
            amount=request_data.amount,
            due_date=due_date,
            recurrence=request_data.recurrence,
            account_id=request_data.account_id
        )
        return {'success': True, 'data': bill.model_dump()}
    except Exception as e:
        logger.exception(f"Error creating bill: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

@router.get('/bills')
async def get_all_bills(
    user_id: str = Query(...),
    current_user: dict = Depends(get_current_user),
    service = Depends(get_bill_payment_service)
):
    """Get all bills for user."""
    try:
        bills = await service.get_upcoming_bills(user_id, 365) 
        return {'success': True, 'data': [b.model_dump() for b in bills]}
    except Exception as e:
        logger.exception(f"Error getting bills: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

@router.get('/upcoming')
async def get_upcoming_bills(
    user_id: str = Query(...),
    days_ahead: int = Query(30),
    current_user: dict = Depends(get_current_user),
    service = Depends(get_bill_payment_service)
):
    """Get upcoming bills for user."""
    try:
        bills = await service.get_upcoming_bills(user_id, days_ahead)
        return {'success': True, 'data': [b.model_dump() for b in bills]}
    except Exception as e:
        logger.exception(f"Error getting upcoming bills: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

@router.get('/history')
async def get_payment_history(
    user_id: str = Query(...),
    limit: int = Query(50),
    current_user: dict = Depends(get_current_user)
):
    """Get payment history for user."""
    try:
        service = get_bill_payment_service()
        history = await service.get_payment_history(user_id, limit)
        return {'success': True, 'data': [h.model_dump() for h in history]}
    except Exception as e:
        logger.exception(f"Error getting payment history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/upcoming/{user_id}')
async def get_upcoming_bills_path(
    user_id: str,
    days_ahead: int = 30,
    current_user: dict = Depends(get_current_user),
    service = Depends(get_bill_payment_service)
):
    return await get_upcoming_bills(user_id, days_ahead, current_user, service)

@router.get('/history/{user_id}')
async def get_payment_history_path(
    user_id: str,
    limit: int = 50,
    current_user: dict = Depends(get_current_user),
    service = Depends(get_bill_payment_service)
):
    return await get_payment_history(user_id, limit, current_user, service)

@router.post('/payment/schedule')
async def schedule_payment(
    request_data: PaymentScheduleRequest,
    current_user: dict = Depends(get_current_user)
):
    """Schedule bill payment."""
    try:
        payment_date = datetime.strptime(request_data.payment_date, '%Y-%m-%d')
        service = get_bill_payment_service()
        payment = await service.schedule_payment(
            bill_id=request_data.bill_id,
            payment_date=payment_date,
            payment_method=request_data.payment_method
        )
        return {'success': True, 'data': payment.model_dump()}
    except Exception as e:
        logger.exception(f"Error scheduling payment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/reminder/create')
async def create_reminder(
    request_data: ReminderCreateRequest,
    current_user: dict = Depends(get_current_user),
    service = Depends(get_payment_reminder_service)
):
    """Create payment reminder."""
    try:
        reminder = await service.create_reminder(
            bill_id=request_data.bill_id,
            reminder_days_before=request_data.reminder_days_before
        )
        return {'success': True, 'data': reminder.model_dump()}
    except Exception as e:
        logger.exception(f"Error creating reminder: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

@router.post('/reminder/send')
async def send_reminders(
    user_id: str = Query(...),
    current_user: dict = Depends(get_current_user)
):
    """Send reminders for upcoming bills."""
    try:
        service = get_payment_reminder_service()
        reminders = await service.send_reminders(user_id)
        return {'success': True, 'data': [r.model_dump() for r in reminders]}
    except Exception as e:
        logger.exception(f"Error sending reminders: {e}")
        raise HTTPException(status_code=500, detail=str(e))
