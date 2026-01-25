/**
 * ==============================================================================
 * FILE: frontend2/src/pages/ComplianceDashboard.jsx
 * ROLE: Compliance & Reporting Dashboard
 * PURPOSE: Phase 32 - Advanced Compliance & Reporting
 *          Displays compliance status, violations, and regulatory reports.
 * 
 * INTEGRATION POINTS:
 *    - ComplianceAPI: /api/v1/compliance endpoints
 * 
 * FEATURES:
 *    - Compliance rule checking
 *    - Violation detection
 *    - Regulatory report generation
 *    - Compliance monitoring
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ComplianceDashboard.css';

const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
const API_BASE = `http://localhost:${BACKEND_PORT}`;

const ComplianceDashboard = () => {
  const [complianceStatus, setComplianceStatus] = useState(null);
  const [violations, setViolations] = useState([]);
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(false);
  const [userId] = useState('user_1');
  const [selectedRule, setSelectedRule] = useState('all');

  useEffect(() => {
    checkCompliance();
    loadViolations();
    loadReports();
  }, []);

  const checkCompliance = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/api/v1/compliance/check`, {
        user_id: userId
      });
      setComplianceStatus(res.data.data);
    } catch (error) {
      console.error('Error checking compliance:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadViolations = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/compliance/violations`, {
        params: { user_id: userId }
      });
      setViolations(res.data.data || []);
    } catch (error) {
      console.error('Error loading violations:', error);
    }
  };

  const loadReports = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/compliance/reports`, {
        params: { user_id: userId }
      });
      setReports(res.data.data || []);
    } catch (error) {
      console.error('Error loading reports:', error);
    }
  };

  const generateReport = async (reportType) => {
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/v1/compliance/report/generate`, {
        user_id: userId,
        report_type: reportType
      });
      loadReports();
      alert('Report generated successfully!');
    } catch (error) {
      console.error('Error generating report:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="compliance-dashboard">
      <div className="dashboard-header">
        <h1>Compliance & Reporting</h1>
        <p className="subtitle">Phase 32: Advanced Compliance & Reporting</p>
      </div>

      <div className="dashboard-content">
        {/* Compliance Status */}
        {complianceStatus && (
          <div className="status-panel">
            <h2>Compliance Status</h2>
            <div className="status-overview">
              <div className="status-card">
                <div className="status-label">Overall Status</div>
                <div className={`status-value ${complianceStatus.overall_status}`}>
                  {complianceStatus.overall_status?.toUpperCase()}
                </div>
              </div>
              <div className="status-card">
                <div className="status-label">Rules Checked</div>
                <div className="status-value">{complianceStatus.rules_checked || 0}</div>
              </div>
              <div className="status-card">
                <div className="status-label">Violations Found</div>
                <div className="status-value" style={{ color: violations.length > 0 ? '#ff4444' : '#00ff88' }}>
                  {violations.length}
                </div>
              </div>
              <div className="status-card">
                <div className="status-label">Last Checked</div>
                <div className="status-value">
                  {new Date(complianceStatus.last_checked).toLocaleDateString()}
                </div>
              </div>
            </div>
            <button onClick={checkCompliance} disabled={loading} className="check-button">
              Re-check Compliance
            </button>
          </div>
        )}

        {/* Violations */}
        <div className="violations-panel">
          <h2>Compliance Violations</h2>
          {violations.length > 0 ? (
            <div className="violations-list">
              {violations.map((violation) => (
                <div key={violation.violation_id} className="violation-card">
                  <div className="violation-header">
                    <h3>{violation.rule_name}</h3>
                    <span className={`severity ${violation.severity}`}>
                      {violation.severity}
                    </span>
                  </div>
                  <p className="violation-description">{violation.description}</p>
                  <div className="violation-details">
                    <span>Detected: {new Date(violation.detected_date).toLocaleDateString()}</span>
                    {violation.resolution_date && (
                      <span>Resolved: {new Date(violation.resolution_date).toLocaleDateString()}</span>
                    )}
                  </div>
                  {!violation.resolution_date && (
                    <div className="violation-actions">
                      <button className="resolve-button">Mark as Resolved</button>
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">No violations found</div>
          )}
        </div>

        {/* Reports */}
        <div className="reports-panel">
          <h2>Regulatory Reports</h2>
          <div className="report-actions">
            <button
              onClick={() => generateReport('monthly')}
              disabled={loading}
              className="generate-button"
            >
              Generate Monthly Report
            </button>
            <button
              onClick={() => generateReport('quarterly')}
              disabled={loading}
              className="generate-button"
            >
              Generate Quarterly Report
            </button>
            <button
              onClick={() => generateReport('annual')}
              disabled={loading}
              className="generate-button"
            >
              Generate Annual Report
            </button>
          </div>
          {reports.length > 0 ? (
            <div className="reports-list">
              {reports.map((report) => (
                <div key={report.report_id} className="report-card">
                  <div className="report-header">
                    <h3>{report.report_type} Report</h3>
                    <span className="report-status">{report.status}</span>
                  </div>
                  <div className="report-meta">
                    <span>Generated: {new Date(report.generated_date).toLocaleDateString()}</span>
                    <span>Period: {report.period}</span>
                  </div>
                  <div className="report-actions">
                    <button className="download-button">Download</button>
                    <button className="view-button">View</button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">No reports generated yet</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ComplianceDashboard;
