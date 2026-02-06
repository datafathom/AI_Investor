import React from 'react';
import PropTypes from 'prop-types';
import { getIcon } from '../../config/iconRegistry';
import './DepartmentMetricPanel.css';

const DepartmentMetricPanel = ({ metrics, primaryMetric, primaryLabel, unit, pulse, workflows, onWorkflowExecute }) => {
  return (
    <div className="metric-panel">
      {/* Primary Department Metric */}
      <div className="primary-metric-card">
        <div className="metric-label">{primaryLabel?.toUpperCase()}</div>
        <div className="metric-value-row">
          <span className="value">{metrics?.[primaryMetric] || 0}</span>
          <span className="unit">{unit}</span>
        </div>
        <div className="metric-trend positive">
          <i className="fas fa-caret-up"></i> 2.4% vs Previous
        </div>
      </div>

      <div className="panel-divider">DEPT ACTIVITY STREAM</div>

      {/* Secondary Metrics */}
      <div className="secondary-metrics-grid">
        {Object.entries(metrics || {}).map(([key, value]) => (
          key !== primaryMetric && (
            <div key={key} className="secondary-metric-item">
              <span className="sm-label">{key.replace(/([A-Z])/g, ' $1').toUpperCase()}</span>
              <span className="sm-value">{typeof value === 'object' ? '...' : value}</span>
            </div>
          )
        ))}
      </div>

      <div className="panel-divider">GLOBAL PULSE</div>

      {/* Global Pulse Sync */}
      <div className="pulse-grid">
        <div className="pulse-item">
          <span className="p-label">SYSTEM HEALTH</span>
          <div className="p-status">
            <span className={`p-dot ${pulse?.systemHealth}`}></span>
            {pulse?.systemHealth?.toUpperCase() || 'STABLE'}
          </div>
        </div>
        <div className="pulse-item">
          <span className="p-label">THREAT LEVEL</span>
          <span className={`p-value threat-${pulse?.threatLevel?.toLowerCase()}`}>
            {pulse?.threatLevel?.toUpperCase() || 'LOW'}
          </span>
        </div>
        <div className="pulse-item">
          <span className="p-label">NET WORTH</span>
          <span className="p-value highlight">${(pulse?.netWorth || 0).toLocaleString()}</span>
        </div>
        <div className="pulse-item">
          <span className="p-label">LIQUIDITY</span>
          <span className="p-value">{pulse?.liquidityDays || 0} DAYS</span>
        </div>
      </div>
      
      <div className="workflow-actions">
        {workflows?.map(wf => {
          const WfIcon = getIcon(wf.icon);
          return (
            <button 
              key={wf.id}
              className={`workflow-btn ${wf.variant || 'primary'}`}
              onClick={() => onWorkflowExecute?.(wf)}
            >
              <WfIcon size={16} />
              {wf.label.toUpperCase()}
            </button>
          );
        })}
        {!workflows && (
          <>
            <button className="workflow-btn primary">
              EXECUTE DEPT PROTOCOL
            </button>
            <button className="workflow-btn secondary">
              EXPORT AUDIT LOG
            </button>
          </>
        )}
      </div>
    </div>
  );
};

DepartmentMetricPanel.propTypes = {
  metrics: PropTypes.object,
  primaryMetric: PropTypes.string,
  primaryLabel: PropTypes.string,
  unit: PropTypes.string,
  pulse: PropTypes.shape({
    systemHealth: PropTypes.string,
    threatLevel: PropTypes.string,
    netWorth: PropTypes.number,
    liquidityDays: PropTypes.number
  }),
  workflows: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired,
    icon: PropTypes.string,
    action: PropTypes.string,
    agentId: PropTypes.string,
    variant: PropTypes.string
  })),
  onWorkflowExecute: PropTypes.func
};

export default DepartmentMetricPanel;
