/**
 * ==============================================================================
 * FILE: frontend2/src/pages/ComplianceDashboard.jsx
 * ROLE: Compliance & Reporting Dashboard
 * PURPOSE:  - Advanced Compliance & Reporting
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
import { StorageService } from '../utils/storageService';
import './ComplianceDashboard.css';
import { complianceService } from '../services/waveServices';

const ComplianceDashboard = () => {
  const [complianceStatus, setComplianceStatus] = useState(null);
  const [violations, setViolations] = useState([]);
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(false);
  const [userId] = useState('user_1');

  useEffect(() => {
    checkCompliance();
    loadViolations();
    loadReports();
  }, []);

  const checkCompliance = async () => {
    setLoading(true);
    try {
      const res = await complianceService.verifyCompliance();
      setComplianceStatus(res.data || res);
    } catch (error) {
      console.error('Error checking compliance:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadViolations = async () => {
    try {
      // Assuming getOverview or a specific endpoint provides violations
      const res = await complianceService.getAuditTrail(); 
      // For now, mapping audit trail to violations structure or using a specific endpoint if available
      // The service definition for getSARQueue might be more relevant for violations depending on API design
      // Falling back to empty array if no specific violation endpoint exists in waveServices yet
      setViolations(res.data?.violations || []);
    } catch (error) {
      console.error('Error loading violations:', error);
    }
  };

  const loadReports = async () => {
    try {
      const res = await complianceService.getOverview();
      setReports(res.data?.reports || []);
    } catch (error) {
      console.error('Error loading reports:', error);
    }
  };

  const generateReport = async (reportType) => {
    setLoading(true);
    try {
      await complianceService.getOverview(); // Placeholder for actual report generation endpoint
      // loadReports();
      alert('Report generation triggered!');
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
        <p className="subtitle">: Advanced Compliance & Reporting</p>
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
