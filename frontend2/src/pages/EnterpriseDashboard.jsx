/**
 * ==============================================================================
 * FILE: frontend2/src/pages/EnterpriseDashboard.jsx
 * ROLE: Enterprise Features Dashboard
 * PURPOSE: Phase 31 - Enterprise Features & Multi-User Support
 *          Displays team management, organizational structure, and shared portfolios.
 * 
 * INTEGRATION POINTS:
 *    - EnterpriseAPI: /api/v1/enterprise endpoints
 * 
 * FEATURES:
 *    - Team management
 *    - Organizational structure
 *    - Role assignments
 *    - Shared portfolios
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './EnterpriseDashboard.css';

const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
const API_BASE = `http://localhost:${BACKEND_PORT}`;

const EnterpriseDashboard = () => {
  const [teams, setTeams] = useState([]);
  const [organizations, setOrganizations] = useState([]);
  const [sharedPortfolios, setSharedPortfolios] = useState([]);
  const [loading, setLoading] = useState(false);
  const [userId] = useState('user_1');
  const [newTeam, setNewTeam] = useState({ name: '', description: '' });

  useEffect(() => {
    loadTeams();
    loadOrganizations();
    loadSharedPortfolios();
  }, []);

  const loadTeams = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/enterprise/teams`, {
        params: { user_id: userId }
      });
      setTeams(res.data.data || []);
    } catch (error) {
      console.error('Error loading teams:', error);
    }
  };

  const loadOrganizations = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/enterprise/organizations`, {
        params: { user_id: userId }
      });
      setOrganizations(res.data.data || []);
    } catch (error) {
      console.error('Error loading organizations:', error);
    }
  };

  const loadSharedPortfolios = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/enterprise/shared-portfolios`, {
        params: { user_id: userId }
      });
      setSharedPortfolios(res.data.data || []);
    } catch (error) {
      console.error('Error loading shared portfolios:', error);
    }
  };

  const createTeam = async () => {
    if (!newTeam.name) return;
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/v1/enterprise/team/create`, {
        user_id: userId,
        team_name: newTeam.name,
        description: newTeam.description
      });
      setNewTeam({ name: '', description: '' });
      loadTeams();
    } catch (error) {
      console.error('Error creating team:', error);
    } finally {
      setLoading(false);
    }
  };

  const sharePortfolio = async (portfolioId, teamId) => {
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/v1/enterprise/portfolio/share`, {
        portfolio_id: portfolioId,
        team_id: teamId
      });
      loadSharedPortfolios();
    } catch (error) {
      console.error('Error sharing portfolio:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="enterprise-dashboard">
      <div className="dashboard-header">
        <h1>Enterprise Features</h1>
        <p className="subtitle">Phase 31: Enterprise Features & Multi-User Support</p>
      </div>

      <div className="dashboard-content">
        {/* Create Team */}
        <div className="create-team-panel">
          <h2>Create Team</h2>
          <div className="team-form">
            <input
              type="text"
              placeholder="Team Name"
              value={newTeam.name}
              onChange={(e) => setNewTeam({ ...newTeam, name: e.target.value })}
              className="form-input"
            />
            <input
              type="text"
              placeholder="Description"
              value={newTeam.description}
              onChange={(e) => setNewTeam({ ...newTeam, description: e.target.value })}
              className="form-input"
            />
            <button onClick={createTeam} disabled={loading} className="create-button">
              Create Team
            </button>
          </div>
        </div>

        {/* Teams */}
        <div className="teams-panel">
          <h2>Your Teams</h2>
          {teams.length > 0 ? (
            <div className="teams-list">
              {teams.map((team) => (
                <div key={team.team_id} className="team-card">
                  <div className="team-header">
                    <h3>{team.team_name}</h3>
                    <span className="member-count">{team.member_count || 0} members</span>
                  </div>
                  <p className="team-description">{team.description || 'No description'}</p>
                  <div className="team-roles">
                    {team.roles && team.roles.map((role, idx) => (
                      <span key={idx} className="role-badge">{role}</span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">No teams created yet</div>
          )}
        </div>

        {/* Organizations */}
        <div className="organizations-panel">
          <h2>Organizations</h2>
          {organizations.length > 0 ? (
            <div className="organizations-list">
              {organizations.map((org) => (
                <div key={org.organization_id} className="org-card">
                  <h3>{org.organization_name}</h3>
                  <div className="org-stats">
                    <span>Teams: {org.team_count || 0}</span>
                    <span>Users: {org.user_count || 0}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">No organizations</div>
          )}
        </div>

        {/* Shared Portfolios */}
        <div className="shared-portfolios-panel">
          <h2>Shared Portfolios</h2>
          {sharedPortfolios.length > 0 ? (
            <div className="portfolios-list">
              {sharedPortfolios.map((portfolio) => (
                <div key={portfolio.portfolio_id} className="portfolio-card">
                  <div className="portfolio-header">
                    <h3>{portfolio.portfolio_name}</h3>
                    <span className="shared-badge">Shared</span>
                  </div>
                  <div className="portfolio-meta">
                    <span>Team: {portfolio.team_name}</span>
                    <span>Value: ${portfolio.total_value?.toLocaleString()}</span>
                  </div>
                  <div className="portfolio-permissions">
                    <span>Permissions: {portfolio.permissions?.join(', ') || 'View'}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">No shared portfolios</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default EnterpriseDashboard;
