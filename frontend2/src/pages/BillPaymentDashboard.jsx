/**
 * ==============================================================================
 * FILE: frontend2/src/pages/BillPaymentDashboard.jsx
 * ROLE: Bill Payment & Reminders Dashboard
 * PURPOSE: Phase 11 - Bill Payment Automation & Reminders
 *          Displays bills, payment scheduling, and reminders.
 * 
 * INTEGRATION POINTS:
 *    - BillingAPI: /api/v1/billing endpoints
 * 
 * FEATURES:
 *    - Bill tracking
 *    - Payment scheduling
 *    - Recurring payments
 *    - Payment reminders
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import useBillingStore from '../stores/billingStore';
import './BillPaymentDashboard.css';

const BillPaymentDashboard = () => {
  const { 
    bills, 
    upcomingBills, 
    paymentHistory, 
    fetchBills, 
    addBill, 
    schedulePayment, 
    loading 
  } = useBillingStore();

  const [userId] = useState('user_1');
  const [newBill, setNewBill] = useState({ payee: '', amount: '', due_date: '', is_recurring: false });

  useEffect(() => {
    fetchBills(userId);
  }, [fetchBills, userId]);

  const handleAddBill = async () => {
    if (!newBill.payee || !newBill.amount || !newBill.due_date) return;
    await addBill({
      user_id: userId,
      payee: newBill.payee,
      amount: parseFloat(newBill.amount),
      due_date: newBill.due_date,
      is_recurring: newBill.is_recurring
    });
    setNewBill({ payee: '', amount: '', due_date: '', is_recurring: false });
  };

  const handleSchedulePayment = async (billId) => {
    await schedulePayment(billId, userId);
  };

  const getDaysUntilDue = (dueDate) => {
    const today = new Date();
    const due = new Date(dueDate);
    const diff = Math.ceil((due - today) / (1000 * 60 * 60 * 24));
    return diff;
  };

  return (
    <div className="full-bleed-page bill-payment-dashboard">
      <div className="dashboard-header">
        <h1>Bill Payment & Reminders</h1>
        <p className="subtitle">Phase 11: Bill Payment Automation & Reminders</p>
      </div>

      <div className="scrollable-content-wrapper">
        <div className="dashboard-content">
          {/* Add Bill */}
          <div className="add-bill-panel">
            <h2>Add Bill</h2>
            <div className="bill-form">
              <div className="form-group">
                <span className="form-label">Payee</span>
                <input
                  type="text"
                  placeholder="e.g. Electric Company"
                  value={newBill.payee}
                  onChange={(e) => setNewBill({ ...newBill, payee: e.target.value })}
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <span className="form-label">Amount ($)</span>
                <input
                  type="number"
                  placeholder="0.00"
                  value={newBill.amount}
                  onChange={(e) => setNewBill({ ...newBill, amount: e.target.value })}
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <span className="form-label">Due Date</span>
                <input
                  type="date"
                  value={newBill.due_date}
                  onChange={(e) => setNewBill({ ...newBill, due_date: e.target.value })}
                  className="form-input"
                />
              </div>
              <div className="form-group" style={{ flex: '0 0 auto', justifyContent: 'center' }}>
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={newBill.is_recurring}
                    onChange={(e) => setNewBill({ ...newBill, is_recurring: e.target.checked })}
                  />
                  Recurring
                </label>
              </div>
              <div className="form-group" style={{ justifyContent: 'flex-end', flex: '0 0 auto' }}>
                <button onClick={handleAddBill} disabled={loading} className="add-button">
                  {loading ? 'Adding...' : 'Add Bill'}
                </button>
              </div>
            </div>
          </div>

          {/* Upcoming Bills */}
          <div className="upcoming-bills-panel">
            <h2>Upcoming Bills</h2>
            {upcomingBills.length > 0 ? (
              <div className="bills-list">
                {upcomingBills.map((bill) => {
                  const daysUntil = getDaysUntilDue(bill.due_date);
                  const isOverdue = daysUntil < 0;
                  const isDueSoon = daysUntil <= 7 && daysUntil >= 0;
                  return (
                    <div key={bill.bill_id} className={`bill-card ${isOverdue ? 'overdue' : isDueSoon ? 'due-soon' : ''}`}>
                      <div className="bill-header">
                        <h3>{bill.payee}</h3>
                        {bill.is_recurring && <span className="recurring-badge">Recurring</span>}
                      </div>
                      <div className="bill-details">
                        <div className="bill-amount">${bill.amount?.toFixed(2)}</div>
                        <div className="bill-due">
                          Due: {new Date(bill.due_date).toLocaleDateString()}
                          {isOverdue && <span className="overdue-label">OVERDUE</span>}
                          {isDueSoon && !isOverdue && <span className="due-soon-label">Due Soon</span>}
                        </div>
                      </div>
                      <button
                        onClick={() => handleSchedulePayment(bill.bill_id)}
                        disabled={loading}
                        className="pay-button"
                      >
                        {loading ? 'Processing...' : 'Schedule Payment'}
                      </button>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="no-data">No upcoming bills</div>
            )}
          </div>

          {/* All Bills */}
          <div className="all-bills-panel">
            <h2>All Bills</h2>
            {bills.length > 0 ? (
              <div className="bills-list">
                {bills.map((bill) => (
                  <div key={bill.bill_id} className="bill-item">
                    <div className="bill-info">
                      <span className="payee">{bill.payee}</span>
                      <span className="amount">${bill.amount?.toFixed(2)}</span>
                    </div>
                    <div className="bill-meta">
                      <span>Due: {new Date(bill.due_date).toLocaleDateString()}</span>
                      <span className={`status ${bill.status}`}>{bill.status}</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-data">No bills added yet</div>
            )}
          </div>

          {/* Payment History */}
          <div className="history-panel">
            <h2>Payment History</h2>
            {paymentHistory.length > 0 ? (
              <div className="history-list">
                {paymentHistory.map((payment) => (
                  <div key={payment.payment_id} className="history-item">
                    <div className="payment-info">
                      <span className="payee">{payment.payee}</span>
                      <span className="amount">${payment.amount?.toFixed(2)}</span>
                    </div>
                    <div className="payment-date">
                      {new Date(payment.payment_date).toLocaleDateString()}
                    </div>
                    <div className={`payment-status ${payment.status}`}>
                      {payment.status}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-data">No payment history</div>
            )}
          </div>
        </div>
        
        {/* Bottom Buffer */}
        <div className="scroll-buffer-100" />
      </div>
    </div>
  );
};

export default BillPaymentDashboard;
