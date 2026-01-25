/**
 * ==============================================================================
 * FILE: frontend2/src/pages/BudgetingDashboard.jsx
 * ROLE: Budgeting & Expense Tracking Dashboard
 * PURPOSE: Phase 10 - Budgeting & Expense Tracking
 *          Displays budgets, expense tracking, and spending insights.
 * 
 * INTEGRATION POINTS:
 *    - BudgetingAPI: /api/v1/budgeting endpoints
 * 
 * FEATURES:
 *    - Budget creation and management
 *    - Expense tracking
 *    - Spending insights
 *    - Category-based budgets
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './BudgetingDashboard.css';

const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
const API_BASE = `http://localhost:${BACKEND_PORT}`;

import { Responsive, WidthProvider } from 'react-grid-layout';

const ResponsiveGridLayout = WidthProvider(Responsive);

const BudgetingDashboard = () => {
  const [budgets, setBudgets] = useState([]);
  const [expenses, setExpenses] = useState([]);
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(false);
  const [userId] = useState('user_1');
  const [newExpense, setNewExpense] = useState({ amount: '', category: '', description: '' });

  const DEFAULT_LAYOUT = {
    lg: [
      { i: 'add-expense', x: 0, y: 0, w: 12, h: 2 },
      { i: 'insights', x: 0, y: 2, w: 12, h: 2 },
      { i: 'budgets', x: 0, y: 4, w: 7, h: 8 },
      { i: 'recent-expenses', x: 7, y: 4, w: 5, h: 8 }
    ]
  };
  const STORAGE_KEY = 'layout_budgeting_dashboard';

  const [layouts, setLayouts] = useState(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      return saved ? JSON.parse(saved) : DEFAULT_LAYOUT;
    } catch (e) {
      return DEFAULT_LAYOUT;
    }
  });

  const onLayoutChange = (currentLayout, allLayouts) => {
    setLayouts(allLayouts);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(allLayouts));
  };

  useEffect(() => {
    loadBudgets();
    loadExpenses();
    loadInsights();
  }, []);

  const loadBudgets = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/budgeting/budgets`, {
        params: { user_id: userId }
      });
      setBudgets(res.data.data || []);
    } catch (error) {
      console.error('Error loading budgets:', error);
    }
  };

  const loadExpenses = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/budgeting/expenses`, {
        params: { user_id: userId, limit: 20 }
      });
      setExpenses(res.data.data || []);
    } catch (error) {
      console.error('Error loading expenses:', error);
    }
  };

  const loadInsights = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/budgeting/insights`, {
        params: { user_id: userId }
      });
      setInsights(res.data.data);
    } catch (error) {
      console.error('Error loading insights:', error);
    }
  };

  const addExpense = async () => {
    if (!newExpense.amount || !newExpense.category) return;
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/v1/budgeting/expenses/add`, {
        user_id: userId,
        amount: parseFloat(newExpense.amount),
        category: newExpense.category,
        description: newExpense.description
      });
      setNewExpense({ amount: '', category: '', description: '' });
      loadExpenses();
      loadInsights();
    } catch (error) {
      console.error('Error adding expense:', error);
    } finally {
      setLoading(false);
    }
  };

  const getBudgetProgress = (budget) => {
    if (!budget.spent || !budget.limit) return 0;
    return Math.min((budget.spent / budget.limit) * 100, 100);
  };

  return (
    <div className="full-bleed-page budgeting-dashboard">
      <div className="dashboard-header">
        <h1>Budgeting & Expense Tracking</h1>
        <p className="subtitle">Phase 10: Budgeting & Expense Tracking</p>
      </div>

      <div className="scrollable-content-wrapper">
        <ResponsiveGridLayout
          className="layout"
          layouts={layouts}
          onLayoutChange={onLayoutChange}
          breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
          cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
          rowHeight={80}
          isDraggable={true}
          isResizable={true}
          draggableHandle="h2"
          margin={[16, 16]}
        >
          {/* Add Expense */}
          <div key="add-expense" className="add-expense-panel">
            <h2>Add Expense</h2>
            <div className="expense-form">
              <div className="form-group">
                <span className="form-label">Amount ($)</span>
                <input
                  type="number"
                  placeholder="0.00"
                  value={newExpense.amount}
                  onChange={(e) => setNewExpense({ ...newExpense, amount: e.target.value })}
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <span className="form-label">Category</span>
                <select
                  value={newExpense.category}
                  onChange={(e) => setNewExpense({ ...newExpense, category: e.target.value })}
                  className="form-input"
                >
                  <option value="">Select Category</option>
                  <option value="food">Food & Dining</option>
                  <option value="transportation">Transportation</option>
                  <option value="housing">Housing</option>
                  <option value="entertainment">Entertainment</option>
                  <option value="shopping">Shopping</option>
                  <option value="utilities">Utilities</option>
                  <option value="healthcare">Healthcare</option>
                  <option value="other">Other</option>
                </select>
              </div>
              <div className="form-group">
                <span className="form-label">Description</span>
                <input
                  type="text"
                  placeholder="e.g. Lunch with client"
                  value={newExpense.description}
                  onChange={(e) => setNewExpense({ ...newExpense, description: e.target.value })}
                  className="form-input"
                />
              </div>
              <div className="form-group" style={{ justifyContent: 'flex-end', flex: '0 0 auto' }}>
                <button onClick={addExpense} disabled={loading} className="add-button">
                  Add Expense
                </button>
              </div>
            </div>
          </div>

          {/* Insights */}
          <div key="insights">
            {insights && (
              <div className="insights-panel h-full">
                <h2>Spending Insights</h2>
                <div className="insights-grid">
                  <div className="insight-card">
                    <div className="insight-label">Total Spent This Month</div>
                    <div className="insight-value">${insights.total_spent?.toFixed(2)}</div>
                  </div>
                  <div className="insight-card">
                    <div className="insight-label">Top Category</div>
                    <div className="insight-value">{insights.top_category}</div>
                  </div>
                  <div className="insight-card">
                    <div className="insight-label">Average Daily Spending</div>
                    <div className="insight-value">${insights.avg_daily_spending?.toFixed(2)}</div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Budgets */}
          <div key="budgets" className="budgets-panel">
            <h2>Budgets</h2>
            {budgets.length > 0 ? (
              <div className="budgets-list">
                {budgets.map((budget) => {
                  const progress = getBudgetProgress(budget);
                  const isOver = budget.spent > budget.limit;
                  return (
                    <div key={budget.budget_id} className="budget-card">
                      <div className="budget-header">
                        <h3>{budget.category}</h3>
                        <span className={`budget-status ${isOver ? 'over' : 'under'}`}>
                          {isOver ? 'Over Budget' : 'Under Budget'}
                        </span>
                      </div>
                      <div className="budget-amounts">
                        <span className="spent">${budget.spent?.toFixed(2)}</span>
                        <span className="limit">of ${budget.limit?.toFixed(2)}</span>
                      </div>
                      <div className="progress-bar-container">
                        <div
                          className={`progress-bar ${isOver ? 'over' : ''}`}
                          style={{ width: `${Math.min(progress, 100)}%` }}
                        ></div>
                      </div>
                      <div className="progress-text">{progress.toFixed(1)}% Used</div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="no-data">No budgets created yet</div>
            )}
          </div>

          {/* Recent Expenses */}
          <div key="recent-expenses" className="expenses-panel">
            <h2>Recent Expenses</h2>
            {expenses.length > 0 ? (
              <div className="expenses-list">
                {expenses.map((expense) => (
                  <div key={expense.expense_id} className="expense-item">
                    <div className="expense-info">
                      <span className="expense-category">{expense.category}</span>
                      <span className="expense-description">{expense.description || 'No description'}</span>
                    </div>
                    <div className="expense-amount">${expense.amount?.toFixed(2)}</div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-data">No expenses recorded</div>
            )}
          </div>
        </ResponsiveGridLayout>
        
        {/* Bottom Buffer */}
        <div className="scroll-buffer-100" />
      </div>
    </div>
  );
};

export default BudgetingDashboard;
