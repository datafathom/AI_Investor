/**
 * ==============================================================================
 * FILE: frontend2/src/pages/ResearchReportsDashboard.jsx
 * ROLE: Research Reports Dashboard
 * PURPOSE: Phase 18 - Research Reports & Analysis
 *          Displays research reports, report generation, and templates.
 * 
 * INTEGRATION POINTS:
 *    - ResearchStore: Centralized state management
 *    - ResearchAPI: /api/v1/research endpoints (via Service)
 * 
 * FEATURES:
 *    - Research report listing
 *    - Report generation
 *    - Report templates
 *    - PDF/HTML/Excel export
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-28
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import { StorageService } from '../utils/storageService';
import useResearchStore from '../stores/researchStore';
import { Responsive, WidthProvider } from 'react-grid-layout';
import './ResearchReportsDashboard.css';

const ResponsiveGridLayout = WidthProvider(Responsive);

const ResearchReportsDashboard = () => {
  // Store State
  const { 
    reports, 
    templates, 
    isLoading, 
    fetchReports, 
    fetchTemplates, 
    generateReport: generateReportAction
  } = useResearchStore();

  const [userId] = useState('user_1');
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [reportParams, setReportParams] = useState({ title: '', format: 'pdf' });

  const DEFAULT_LAYOUT = {
    lg: [
      { i: 'generate', x: 0, y: 0, w: 12, h: 2 },
      { i: 'reports', x: 0, y: 2, w: 8, h: 8 },
      { i: 'templates', x: 8, y: 2, w: 4, h: 8 }
    ]
  };
  const STORAGE_KEY = 'layout_research_reports';

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
    StorageService.set(STORAGE_KEY, allLayouts);
  };

  // Load Data on Mount
  useEffect(() => {
    fetchReports(userId);
    fetchTemplates();
  }, [userId, fetchReports, fetchTemplates]);

  const handleGenerateReport = async () => {
    if (!selectedTemplate || !reportParams.title) return;
    
    const success = await generateReportAction(
      userId, 
      selectedTemplate, 
      reportParams.title, 
      reportParams.format
    );

    if (success) {
      setReportParams({ title: '', format: 'pdf' });
      setSelectedTemplate(null);
    }
  };

  return (
    <div className="full-bleed-page research-reports-dashboard">
      <div className="dashboard-header">
        <h1>Research Reports & Analysis</h1>
        <p className="subtitle">Phase 18: Research Reports & Analysis</p>
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
          {/* Generate Report */}
          <div key="generate" className="generate-panel">
            <h2>Generate New Research Report</h2>
            <div className="generate-form">
              <div className="form-group">
                <span className="form-label">Template</span>
                <select
                  value={selectedTemplate || ''}
                  onChange={(e) => setSelectedTemplate(e.target.value)}
                  className="form-input"
                >
                  <option value="">Select Template</option>
                  {templates.map((template) => (
                    <option key={template.template_id} value={template.template_id}>
                      {template.template_name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <span className="form-label">Report Title</span>
                <input
                  type="text"
                  placeholder="e.g. Q1 Tech Outlook"
                  value={reportParams.title}
                  onChange={(e) => setReportParams({ ...reportParams, title: e.target.value })}
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <span className="form-label">Output Format</span>
                <select
                  value={reportParams.format}
                  onChange={(e) => setReportParams({ ...reportParams, format: e.target.value })}
                  className="form-input"
                >
                  <option value="pdf">PDF Document</option>
                  <option value="html">Interactive HTML</option>
                  <option value="excel">Data Export (Excel)</option>
                </select>
              </div>
              <div className="form-group" style={{ flex: '0 0 auto', justifyContent: 'flex-end' }}>
                <button 
                  onClick={handleGenerateReport} 
                  disabled={isLoading || !selectedTemplate} 
                  className="generate-button"
                >
                  {isLoading ? 'Generating...' : 'Generate Report'}
                </button>
              </div>
            </div>
          </div>

          {/* Reports List */}
          <div key="reports" className="reports-panel h-full">
            <h2>Your Generated Reports</h2>
            {reports.length > 0 ? (
              <div className="reports-list">
                {reports.map((report) => (
                  <div key={report.report_id} className="report-card">
                    <div className="report-header">
                      <h3>{report.report_title}</h3>
                      <span className="report-format">{report.format?.toUpperCase()}</span>
                    </div>
                    <div className="report-meta">
                      <span>Created: {new Date(report.created_date).toLocaleDateString()}</span>
                      <span>Pages: {report.page_count || 'N/A'}</span>
                    </div>
                    <div className="report-actions">
                      <button className="download-button">Download</button>
                      <button className="view-button">View</button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
                <div className="no-data">No reports found. Generate one above to begin.</div>
            )}
          </div>

          {/* Templates */}
          <div key="templates" className="templates-panel h-full">
            <h2>Library Templates</h2>
            {templates.length > 0 ? (
              <div className="templates-list">
                {templates.map((template) => (
                  <div key={template.template_id} className="template-card">
                    <h3>{template.template_name}</h3>
                    <p className="template-description">{template.description}</p>
                    <div className="template-meta">
                      <span className="category">{template.category}</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-data">No templates available</div>
            )}
          </div>
        </ResponsiveGridLayout>
        
        {/* Bottom Buffer */}
        <div className="scroll-buffer-100" />
      </div>
    </div>
  );
};

export default ResearchReportsDashboard;

