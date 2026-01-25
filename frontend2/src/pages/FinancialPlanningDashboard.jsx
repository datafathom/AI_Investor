/**
 * ==============================================================================
 * FILE: frontend2/src/pages/FinancialPlanningDashboard.jsx
 * ROLE: Financial Planning & Goal Tracking Dashboard
 * PURPOSE: Phase 7 - Financial Planning & Goal Tracking
 *          Displays financial goals, progress tracking, and planning recommendations.
 * 
 * INTEGRATION POINTS:
 *    - FinancialPlanningAPI: /api/v1/financial-planning endpoints
 * 
 * FEATURES:
 *    - Goal creation and tracking
 *    - Progress visualization
 *    - Planning recommendations
 *    - Scenario analysis
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './FinancialPlanningDashboard.css';

const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
const API_BASE = `http://localhost:${BACKEND_PORT}`;

const FinancialPlanningDashboard = () => {
  const [goals, setGoals] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [userId] = useState('user_1');
  const [newGoal, setNewGoal] = useState({ name: '', target_amount: '', target_date: '', goal_type: 'retirement' });

  useEffect(() => {
    loadGoals();
    loadRecommendations();
  }, []);

  const loadGoals = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/financial-planning/goals`, {
        params: { user_id: userId }
      });
      setGoals(res.data.data || []);
    } catch (error) {
      console.error('Error loading goals:', error);
    }
  };

  const loadRecommendations = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/financial-planning/recommendations`, {
        params: { user_id: userId }
      });
      setRecommendations(res.data.data || []);
    } catch (error) {
      console.error('Error loading recommendations:', error);
    }
  };

  const createGoal = async () => {
    if (!newGoal.name || !newGoal.target_amount) return;
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/v1/financial-planning/goals/create`, {
        user_id: userId,
        goal_name: newGoal.name,
        target_amount: parseFloat(newGoal.target_amount),
        target_date: newGoal.target_date,
        goal_type: newGoal.goal_type
      });
      setNewGoal({ name: '', target_amount: '', target_date: '', goal_type: 'retirement' });
      loadGoals();
    } catch (error) {
      console.error('Error creating goal:', error);
    } finally {
      setLoading(false);
    }
  };

  const getProgressPercentage = (goal) => {
    if (!goal.current_amount || !goal.target_amount) return 0;
    return Math.min((goal.current_amount / goal.target_amount) * 100, 100);
  };

  return (
    <div className="full-bleed-page financial-planning-dashboard">
      <div className="dashboard-header">
        <h1>Financial Planning & Goal Tracking</h1>
        <p className="subtitle">Phase 7: Financial Planning & Goal Tracking</p>
      </div>

      <div className="scrollable-content-wrapper">
        <div className="dashboard-content">
          {/* Create Goal */}
          <div className="create-goal-panel">
            <h2>Create New Goal</h2>
            <div className="goal-form">
              <div className="form-group">
                <span className="form-label">Goal Name</span>
                <input
                  type="text"
                  placeholder="e.g. Dream House"
                  value={newGoal.name}
                  onChange={(e) => setNewGoal({ ...newGoal, name: e.target.value })}
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <span className="form-label">Target Amount ($)</span>
                <input
                  type="number"
                  placeholder="0.00"
                  value={newGoal.target_amount}
                  onChange={(e) => setNewGoal({ ...newGoal, target_amount: e.target.value })}
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <span className="form-label">Target Date</span>
                <input
                  type="date"
                  value={newGoal.target_date}
                  onChange={(e) => setNewGoal({ ...newGoal, target_date: e.target.value })}
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <span className="form-label">Goal Type</span>
                <select
                  value={newGoal.goal_type}
                  onChange={(e) => setNewGoal({ ...newGoal, goal_type: e.target.value })}
                  className="form-input"
                >
                  <option value="retirement">Retirement</option>
                  <option value="house">House Purchase</option>
                  <option value="education">Education</option>
                  <option value="vacation">Vacation</option>
                  <option value="emergency">Emergency Fund</option>
                  <option value="other">Other</option>
                </select>
              </div>
              <div className="form-group" style={{ justifyContent: 'flex-end' }}>
                <button onClick={createGoal} disabled={loading} className="create-button">
                  Create Goal
                </button>
              </div>
            </div>
          </div>

          {/* Goals List */}
          <div className="goals-panel">
            <h2>Your Goals</h2>
            {goals.length > 0 ? (
              <div className="goals-list">
                {goals.map((goal) => {
                  const progress = getProgressPercentage(goal);
                  return (
                    <div key={goal.goal_id} className="goal-card">
                      <div className="goal-header">
                        <h3>{goal.goal_name}</h3>
                        <span className="goal-type">{goal.goal_type}</span>
                      </div>
                      <div className="goal-amounts">
                        <span className="current">${goal.current_amount?.toFixed(2) || 0}</span>
                        <span className="target">of ${goal.target_amount?.toFixed(2)}</span>
                      </div>
                      <div className="progress-bar-container">
                        <div className="progress-bar" style={{ width: `${progress}%` }}></div>
                      </div>
                      <div className="progress-text">{progress.toFixed(1)}% Complete</div>
                      {goal.target_date && (
                        <div className="goal-date">
                          Target Date: {new Date(goal.target_date).toLocaleDateString()}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="no-data">No goals created yet</div>
            )}
          </div>

          {/* Recommendations */}
          <div className="recommendations-panel">
            <h2>Planning Recommendations</h2>
            {recommendations.length > 0 ? (
              <div className="recommendations-list">
                {recommendations.map((rec, idx) => (
                  <div key={idx} className="recommendation-card">
                    <h3>{rec.title}</h3>
                    <p>{rec.description}</p>
                    <div className="rec-priority">Priority: {rec.priority}</div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-data">No recommendations available</div>
            )}
          </div>
        </div>
        
        {/* Bottom Buffer */}
        <div className="scroll-buffer-100" />
      </div>
    </div>
  );
};

export default FinancialPlanningDashboard;
