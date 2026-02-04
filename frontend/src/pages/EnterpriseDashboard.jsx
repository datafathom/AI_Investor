/**
 * ==============================================================================
 * FILE: frontend2/src/pages/EnterpriseDashboard.jsx
 * ROLE: Enterprise Features Dashboard
 * PURPOSE:  - Enterprise Features & Multi-User Support
 *          Displays team management, organizational structure, and shared portfolios.
 * 
 * INTEGRATION POINTS:
 *    - EnterpriseStore: Centralized state management
 *    - EnterpriseAPI: /api/v1/enterprise endpoints (via Service)
 * 
 * FEATURES:
 *    - Team management
 *    - Organizational structure
 *    - Role assignments
 *    - Shared portfolios
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-28
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import { StorageService } from '../utils/storageService';
import useEnterpriseStore from '../stores/enterpriseStore';
import './EnterpriseDashboard.css';

const EnterpriseDashboard = () => {
  // Store State
  const { 
    teams, 
    organizations, 
    sharedPortfolios, 
    isLoading, 
    fetchTeams, 
    fetchOrganizations, 
    fetchSharedPortfolios,
    createTeam: createTeamAction,
    sharePortfolio: sharePortfolioAction
  } = useEnterpriseStore();

  const [userId] = useState('user_1');
  const [newTeam, setNewTeam] = useState({ name: '', description: '' });

  // Load Data on Mount
  useEffect(() => {
    fetchTeams(userId);
    fetchOrganizations(userId);
    fetchSharedPortfolios(userId);
  }, [userId, fetchTeams, fetchOrganizations, fetchSharedPortfolios]);

  const handleCreateTeam = async () => {
    if (!newTeam.name) return;
    
    const success = await createTeamAction(userId, newTeam.name, newTeam.description);
    if (success) {
      setNewTeam({ name: '', description: '' });
    }
  };

  // NOTE: This function is currently unused in the UI but preserved for future wiring
  const handleSharePortfolio = async (portfolioId, teamId) => {
    await sharePortfolioAction(userId, portfolioId, teamId);
  };

  return (
    <div className="enterprise-dashboard">
      <div className="dashboard-header">
        <h1>Enterprise Features</h1>
        <p className="subtitle">: Enterprise Features & Multi-User Support</p>
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
            <button onClick={handleCreateTeam} disabled={isLoading} className="create-button">
              {isLoading ? 'Creating...' : 'Create Team'}
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

