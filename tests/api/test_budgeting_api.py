"""
Tests for Budgeting API Endpoints
Phase 10: Budgeting & Expense Tracking
"""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.budgeting_api import router, get_budgeting_service, get_expense_tracking_service
from web.auth_utils import get_current_user


@pytest.fixture
def api_app(mock_budgeting_service, mock_expense_tracking_service):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_budgeting_service] = lambda: mock_budgeting_service
    app.dependency_overrides[get_expense_tracking_service] = lambda: mock_expense_tracking_service
    app.dependency_overrides[get_current_user] = lambda: {"id": "user_1", "role": "user"}
    return app



@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_budgeting_service():
    """Mock BudgetingService."""
    service = AsyncMock()
    return service


@pytest.fixture
def mock_expense_tracking_service():
    """Mock ExpenseTrackingService."""
    service = AsyncMock()
    return service


def test_create_budget_success(client, mock_budgeting_service):
    """Test successful budget creation."""
    from datetime import datetime, timezone
    from schemas.budgeting import Budget
    
    mock_budget = Budget(
        budget_id='budget_1',
        user_id='user_1',
        budget_name='Monthly Budget',
        period='monthly',
        categories={'food': 500.0, 'transportation': 300.0},
        total_budget=800.0,
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )
    mock_budgeting_service.create_budget.return_value = mock_budget
    
    response = client.post('/api/v1/budgeting/budget/create',
                          json={
                              'user_id': 'user_1',
                              'budget_name': 'Monthly Budget',
                              'period': 'monthly',
                              'categories': {'food': 500.0, 'transportation': 300.0}
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['budget_name'] == 'Monthly Budget'


def test_create_budget_missing_params(client):
    """Test budget creation with missing parameters."""
    response = client.post('/api/v1/budgeting/budget/create',
                          json={'user_id': 'user_1', 'budget_name': 'Test'})
    
    # Pydantic validation error or internal check
    assert response.status_code in [400, 422]


def test_add_expense_success(client, mock_expense_tracking_service):
    """Test successful expense addition."""
    from datetime import datetime, timezone
    from schemas.budgeting import Expense, ExpenseCategory
    
    mock_expense = Expense(
        expense_id='expense_1',
        user_id='user_1',
        amount=50.0,
        category=ExpenseCategory.FOOD,
        description='Groceries',
        date=datetime.now(timezone.utc)
    )
    mock_expense_tracking_service.add_expense.return_value = mock_expense
    
    response = client.post('/api/v1/budgeting/expense/add',
                          json={
                              'user_id': 'user_1',
                              'amount': 50.0,
                              'category': 'food',
                              'description': 'Groceries'
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['amount'] == 50.0


def test_get_user_expenses_success(client, mock_expense_tracking_service):
    """Test successful user expenses retrieval."""
    from datetime import datetime, timezone
    from schemas.budgeting import Expense, ExpenseCategory
    
    mock_expenses = [
        Expense(
            expense_id='expense_1',
            user_id='user_1',
            amount=50.0,
            category=ExpenseCategory.FOOD,
            description="Mock",
            date=datetime.now(timezone.utc)
        )
    ]
    mock_expense_tracking_service.get_expenses.return_value = mock_expenses
    
    response = client.get('/api/v1/budgeting/expense/user_1?limit=20')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 1
