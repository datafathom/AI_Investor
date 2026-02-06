import React, { useEffect, useRef } from 'react';
import useDepartmentStore from '../../stores/departmentStore';
import { Terminal, Info, AlertTriangle, CheckCircle, Zap } from 'lucide-react';
import './DepartmentActivityLog.css';

const EMPTY_LOGS = [];

/**
 * DepartmentActivityLog - Streaming activity feed for agent events
 */
const DepartmentActivityLog = ({ deptId, color }) => {
  const departmentLogs = useDepartmentStore((state) => state.departmentLogs[deptId] || EMPTY_LOGS);
  const viewportRef = useRef(null);

  // Auto-scroll to bottom on new logs
  useEffect(() => {
    if (viewportRef.current) {
      const scrollContainer = viewportRef.current;
      const isAtBottom = scrollContainer.scrollHeight - scrollContainer.scrollTop <= scrollContainer.clientHeight + 100;
      
      if (isAtBottom) {
        scrollContainer.scrollTo({
          top: scrollContainer.scrollHeight,
          behavior: 'smooth'
        });
      }
    }
  }, [departmentLogs]);

  const getLogIcon = (type) => {
    switch (type) {
      case 'critical': return <AlertTriangle size={14} className="log-icon critical" />;
      case 'warning': return <Zap size={14} className="log-icon warning" />;
      case 'success': return <CheckCircle size={14} className="log-icon success" />;
      default: return <Info size={14} className="log-icon info" />;
    }
  };

  return (
    <div className="dept-activity-log">
      <div className="log-header">
        <div className="log-title">
          <Terminal size={16} style={{ color }} />
          <span>REAL-TIME AGENT ACTIVITY</span>
        </div>
        <div className="log-status">
          <span className="pulse-dot" style={{ backgroundColor: color }}></span>
          STREAMING DATA
        </div>
      </div>

      <div className="log-viewport custom-scrollbar" ref={viewportRef}>
        {departmentLogs.length === 0 ? (
          <div className="log-empty">
            <p>Initializing neural bridge...</p>
            <p className="sub">Waiting for agent events from Kafka cluster</p>
          </div>
        ) : (
          departmentLogs.map((log) => (
            <div key={log.id} className={`log-entry ${log.type || 'info'}`}>
              <div className="log-meta">
                <span className="log-time">[{log.timestamp}]</span>
                {getLogIcon(log.type)}
                <span className="log-agent">{log.agent || 'SYSTEM'}:</span>
              </div>
              <div className="log-message">{log.message}</div>
            </div>
          ))
        )}
      </div>
      
      <div className="log-footer">
        <span className="log-count">{departmentLogs.length} EVENTS LOADED</span>
        <span className="log-encryption">256-BIT ENCRYPTED TUNNEL</span>
      </div>
    </div>
  );
};

export default DepartmentActivityLog;
