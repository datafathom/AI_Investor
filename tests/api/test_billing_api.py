"""
Tests for Bill Payment API Endpoints
Phase 11: Bill Payment Automation
"""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from datetime import datetime, timezone
from web.api.billing_api import router, get_bill_payment_service, get_payment_reminder_service
from web.auth_utils import get_current_user


@pytest.fixture
def api_app(mock_bill_payment_service, mock_payment_reminder_service):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_bill_payment_service] = lambda: mock_bill_payment_service
    app.dependency_overrides[get_payment_reminder_service] = lambda: mock_payment_reminder_service
    app.dependency_overrides[get_current_user] = lambda: {"id": "user_1", "role": "user"}
    return app



@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_bill_payment_service():
    """Mock BillPaymentService."""
    service = AsyncMock()
    return service


@pytest.fixture
def mock_payment_reminder_service():
    """Mock PaymentReminderService."""
    service = AsyncMock()
    return service


def test_create_bill_success(client, mock_bill_payment_service):
    """Test successful bill creation."""
    from schemas.billing import Bill, RecurrenceType
    
    mock_bill = Bill(
        bill_id='bill_1',
        user_id='user_1',
        bill_name='Electric Bill',
        merchant='Utility Company',
        amount=150.0,
        due_date=datetime(2024, 12, 31),
        recurrence=RecurrenceType.MONTHLY,
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )
    mock_bill_payment_service.create_bill.return_value = mock_bill
    
    response = client.post('/api/v1/billing/bill/create',
                          json={
                               'user_id': 'user_1',
                               'bill_name': 'Electric Bill',
                               'merchant': 'Utility Company',
                               'amount': 150.0,
                               'due_date': '2024-12-31',
                               'recurrence': 'monthly'
                           })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['bill_name'] == 'Electric Bill'


def test_create_bill_missing_params(client):
    """Test bill creation with missing parameters."""
    response = client.post('/api/v1/billing/bill/create',
                          json={'user_id': 'user_1', 'bill_name': 'Test'})
    
    # FastAPI returns 422 Unprocessable Entity for Pydantic validation errors
    assert response.status_code in [400, 422]


def test_get_upcoming_bills_success(client, mock_bill_payment_service):
    """Test successful upcoming bills retrieval."""
    from schemas.billing import Bill, RecurrenceType
    
    mock_bills = [
        Bill(
            bill_id='bill_1',
            user_id='user_1',
            bill_name='Electric Bill',
            merchant='Utility Company',
            amount=150.0,
            due_date=datetime(2024, 12, 31),
            recurrence=RecurrenceType.MONTHLY,
            created_date=datetime.now(timezone.utc),
            updated_date=datetime.now(timezone.utc)
        )
    ]
    mock_bill_payment_service.get_upcoming_bills.return_value = mock_bills
    
    response = client.get('/api/v1/billing/upcoming?user_id=user_1')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 1


def test_create_reminder_success(client, mock_payment_reminder_service):
    """Test successful reminder creation."""
    from schemas.billing import PaymentReminder
    
    mock_reminder = PaymentReminder(
        reminder_id='reminder_1',
        bill_id='bill_1',
        reminder_date=datetime.now(timezone.utc),
        reminder_type='upcoming'
    )
    mock_payment_reminder_service.create_reminder.return_value = mock_reminder
    
    response = client.post('/api/v1/billing/reminder/create',
                          json={
                               'bill_id': 'bill_1',
                               'reminder_days_before': 3
                           })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
