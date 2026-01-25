"""
Tests for Budgeting API Endpoints
Phase 10: Budgeting & Expense Tracking
"""

import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from web.api.budgeting_api import budgeting_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(budgeting_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_budgeting_service():
    """Mock BudgetingService."""
    with patch('web.api.budgeting_api.get_budgeting_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.fixture
def mock_expense_tracking_service():
    """Mock ExpenseTrackingService."""
    with patch('web.api.budgeting_api.get_expense_tracking_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.mark.asyncio
async def test_create_budget_success(client, mock_budgeting_service):
    """Test successful budget creation."""
    from models.budgeting import Budget
    
    mock_budget = Budget(
        budget_id='budget_1',
        user_id='user_1',
        budget_name='Monthly Budget',
        period='monthly',
        categories={'food': 500.0, 'transportation': 300.0}
    )
    mock_budgeting_service.create_budget.return_value = mock_budget
    
    response = client.post('/api/budgeting/budget/create',
                          json={
                              'user_id': 'user_1',
                              'budget_name': 'Monthly Budget',
                              'period': 'monthly',
                              'categories': {'food': 500.0, 'transportation': 300.0}
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['budget_name'] == 'Monthly Budget'


@pytest.mark.asyncio
async def test_create_budget_missing_params(client):
    """Test budget creation with missing parameters."""
    response = client.post('/api/budgeting/budget/create',
                          json={'user_id': 'user_1', 'budget_name': 'Test'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


@pytest.mark.asyncio
async def test_add_expense_success(client, mock_expense_tracking_service):
    """Test successful expense addition."""
    from models.budgeting import Expense
    
    mock_expense = Expense(
        expense_id='expense_1',
        user_id='user_1',
        amount=50.0,
        category='food',
        description='Groceries'
    )
    mock_expense_tracking_service.add_expense.return_value = mock_expense
    
    response = client.post('/api/budgeting/expense/add',
                          json={
                              'user_id': 'user_1',
                              'amount': 50.0,
                              'category': 'food',
                              'description': 'Groceries'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['amount'] == 50.0


@pytest.mark.asyncio
async def test_get_user_expenses_success(client, mock_expense_tracking_service):
    """Test successful user expenses retrieval."""
    from models.budgeting import Expense
    
    mock_expenses = [
        Expense(
            expense_id='expense_1',
            user_id='user_1',
            amount=50.0,
            category='food'
        )
    ]
    mock_expense_tracking_service.get_user_expenses.return_value = mock_expenses
    
    response = client.get('/api/budgeting/expense/user_1?limit=20')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) == 1
