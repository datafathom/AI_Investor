"""
==============================================================================
FILE: web/api/billing_api.py
ROLE: Bill Payment API Endpoints
PURPOSE: REST endpoints for bill payment tracking and reminders.

INTEGRATION POINTS:
    - BillPaymentService: Bill management
    - PaymentReminderService: Reminder system
    - FrontendBilling: Bill payment dashboard

ENDPOINTS:
    - POST /api/billing/bill/create
    - GET /api/billing/bill/upcoming/:user_id
    - POST /api/billing/payment/schedule
    - GET /api/billing/payment/history/:user_id
    - POST /api/billing/reminder/create
    - POST /api/billing/reminder/send/:user_id

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
from datetime import datetime
import logging
from services.billing.bill_payment_service import get_bill_payment_service
from services.billing.payment_reminder_service import get_payment_reminder_service

logger = logging.getLogger(__name__)

billing_bp = Blueprint('billing', __name__, url_prefix='/api/billing')


@billing_bp.route('/bill/create', methods=['POST'])
async def create_bill():
    """
    Create a new bill.
    
    Request body:
        user_id: User identifier
        bill_name: Name of bill
        merchant: Merchant name
        amount: Bill amount
        due_date: Due date (YYYY-MM-DD)
        recurrence: Recurrence type (default: one_time)
        account_id: Optional account for payment
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        bill_name = data.get('bill_name')
        merchant = data.get('merchant')
        amount = float(data.get('amount', 0))
        due_date_str = data.get('due_date')
        recurrence = data.get('recurrence', 'one_time')
        account_id = data.get('account_id')
        
        if not user_id or not bill_name or not merchant or not amount or not due_date_str:
            return jsonify({
                'success': False,
                'error': 'user_id, bill_name, merchant, amount, and due_date are required'
            }), 400
        
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        
        service = get_bill_payment_service()
        bill = await service.create_bill(
            user_id=user_id,
            bill_name=bill_name,
            merchant=merchant,
            amount=amount,
            due_date=due_date,
            recurrence=recurrence,
            account_id=account_id
        )
        
        return jsonify({
            'success': True,
            'data': bill.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error creating bill: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@billing_bp.route('/bill/upcoming/<user_id>', methods=['GET'])
async def get_upcoming_bills(user_id: str):
    """
    Get upcoming bills for user.
    
    Query params:
        days_ahead: Number of days to look ahead (default: 30)
    """
    try:
        days_ahead = int(request.args.get('days_ahead', 30))
        
        service = get_bill_payment_service()
        bills = await service.get_upcoming_bills(user_id, days_ahead)
        
        return jsonify({
            'success': True,
            'data': [b.model_dump() for b in bills]
        })
        
    except Exception as e:
        logger.error(f"Error getting upcoming bills: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@billing_bp.route('/payment/schedule', methods=['POST'])
async def schedule_payment():
    """
    Schedule bill payment.
    
    Request body:
        bill_id: Bill identifier
        payment_date: Payment date (YYYY-MM-DD)
        payment_method: Payment method (default: bank_transfer)
    """
    try:
        data = request.get_json() or {}
        bill_id = data.get('bill_id')
        payment_date_str = data.get('payment_date')
        payment_method = data.get('payment_method', 'bank_transfer')
        
        if not bill_id or not payment_date_str:
            return jsonify({
                'success': False,
                'error': 'bill_id and payment_date are required'
            }), 400
        
        payment_date = datetime.strptime(payment_date_str, '%Y-%m-%d')
        
        service = get_bill_payment_service()
        payment = await service.schedule_payment(
            bill_id=bill_id,
            payment_date=payment_date,
            payment_method=payment_method
        )
        
        return jsonify({
            'success': True,
            'data': payment.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error scheduling payment: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@billing_bp.route('/payment/history/<user_id>', methods=['GET'])
async def get_payment_history(user_id: str):
    """
    Get payment history for user.
    
    Query params:
        limit: Maximum number of records (default: 50)
    """
    try:
        limit = int(request.args.get('limit', 50))
        
        service = get_bill_payment_service()
        history = await service.get_payment_history(user_id, limit)
        
        return jsonify({
            'success': True,
            'data': [h.model_dump() for h in history]
        })
        
    except Exception as e:
        logger.error(f"Error getting payment history: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@billing_bp.route('/reminder/create', methods=['POST'])
async def create_reminder():
    """
    Create payment reminder.
    
    Request body:
        bill_id: Bill identifier
        reminder_days_before: Days before due date (default: 7)
    """
    try:
        data = request.get_json() or {}
        bill_id = data.get('bill_id')
        reminder_days_before = int(data.get('reminder_days_before', 7))
        
        if not bill_id:
            return jsonify({
                'success': False,
                'error': 'bill_id is required'
            }), 400
        
        service = get_payment_reminder_service()
        reminder = await service.create_reminder(
            bill_id=bill_id,
            reminder_days_before=reminder_days_before
        )
        
        return jsonify({
            'success': True,
            'data': reminder.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error creating reminder: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@billing_bp.route('/reminder/send/<user_id>', methods=['POST'])
async def send_reminders(user_id: str):
    """
    Send reminders for upcoming bills.
    """
    try:
        service = get_payment_reminder_service()
        reminders = await service.send_reminders(user_id)
        
        return jsonify({
            'success': True,
            'data': [r.model_dump() for r in reminders]
        })
        
    except Exception as e:
        logger.error(f"Error sending reminders: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
