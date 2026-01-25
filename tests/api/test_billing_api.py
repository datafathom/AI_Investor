"""
Tests for Bill Payment API Endpoints
Phase 11: Bill Payment Automation
"""

import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from datetime import datetime
from web.api.billing_api import billing_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(billing_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_bill_payment_service():
    """Mock BillPaymentService."""
    with patch('web.api.billing_api.get_bill_payment_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.fixture
def mock_payment_reminder_service():
    """Mock PaymentReminderService."""
    with patch('web.api.billing_api.get_payment_reminder_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.mark.asyncio
async def test_create_bill_success(client, mock_bill_payment_service):
    """Test successful bill creation."""
    from models.billing import Bill
    
    mock_bill = Bill(
        bill_id='bill_1',
        user_id='user_1',
        bill_name='Electric Bill',
        merchant='Utility Company',
        amount=150.0,
        due_date=datetime(2024, 12, 31),
        recurrence='monthly'
    )
    mock_bill_payment_service.create_bill.return_value = mock_bill
    
    response = client.post('/api/billing/bill/create',
                          json={
                              'user_id': 'user_1',
                              'bill_name': 'Electric Bill',
                              'merchant': 'Utility Company',
                              'amount': 150.0,
                              'due_date': '2024-12-31',
                              'recurrence': 'monthly'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['bill_name'] == 'Electric Bill'


@pytest.mark.asyncio
async def test_create_bill_missing_params(client):
    """Test bill creation with missing parameters."""
    response = client.post('/api/billing/bill/create',
                          json={'user_id': 'user_1', 'bill_name': 'Test'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


@pytest.mark.asyncio
async def test_get_upcoming_bills_success(client, mock_bill_payment_service):
    """Test successful upcoming bills retrieval."""
    from models.billing import Bill
    
    mock_bills = [
        Bill(
            bill_id='bill_1',
            user_id='user_1',
            bill_name='Electric Bill',
            merchant='Utility Company',
            amount=150.0,
            due_date=datetime(2024, 12, 31),
            recurrence='monthly'
        )
    ]
    mock_bill_payment_service.get_upcoming_bills.return_value = mock_bills
    
    response = client.get('/api/billing/bill/upcoming/user_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) == 1


@pytest.mark.asyncio
async def test_create_reminder_success(client, mock_payment_reminder_service):
    """Test successful reminder creation."""
    from models.billing import PaymentReminder
    
    mock_reminder = PaymentReminder(
        reminder_id='reminder_1',
        user_id='user_1',
        bill_id='bill_1',
        reminder_days_before=3
    )
    mock_payment_reminder_service.create_reminder.return_value = mock_reminder
    
    response = client.post('/api/billing/reminder/create',
                          json={
                              'user_id': 'user_1',
                              'bill_id': 'bill_1',
                              'reminder_days_before': 3
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
