import React, { useState } from 'react';
import useDepartmentStore from '../../stores/departmentStore';
import './AgentPanel.css';

const AgentPanel = ({ agents, deptId }) => {
  const invokeAgent = useDepartmentStore((state) => state.invokeAgent);
  const [invoking, setInvoking] = useState({});

  const handleInvoke = async (agentSlug) => {
    setInvoking(prev => ({ ...prev, [agentSlug]: true }));
    try {
      await invokeAgent(deptId, agentSlug, { action: 'status_check', data: {} });
    } catch (err) {
      console.error('Failed to invoke agent:', err);
    } finally {
      setInvoking(prev => ({ ...prev, [agentSlug]: false }));
    }
  };

  return (
    <div className="agent-panel">
      <div className="panel-header">
        <i className="fas fa-users-cog"></i>
        <h3>AGENT FLEET</h3>
        <span className="agent-count">{agents?.length || 0}/6 ONLINE</span>
      </div>
      
      <div className="agent-list">
        {agents?.map((agent, index) => {
          // Handle both string slugs (legacy) and object inputs (API)
           const agentId = typeof agent === 'string' ? agent : agent.agent_id;
           const agentRole = typeof agent === 'string' ? '' : agent.role;
           const agentStatus = typeof agent === 'string' ? 'idle' : agent.status;
           
           return (
          <div key={`${deptId}-${agentId}`} className={`agent-card ${invoking[agentId] ? 'invoking' : ''}`}>
            <div className="agent-id">#{index + 1}</div>
            <div className="agent-info">
              <div className="agent-name">{agentId.replace(/_/g, ' ').toUpperCase()}</div>
              {agentRole && <div className="agent-role">{agentRole}</div>}
              <div className="agent-status-row">
                <span className={`status-indicator ${agentStatus}`}></span>
                <span className="status-text">
                  {invoking[agentId] ? 'PROCESSING' : agentStatus.toUpperCase()}
                </span>
              </div>
            </div>
            <button 
              className="agent-invoke-btn" 
              title="Invoke Agent"
              onClick={() => handleInvoke(agentId)}
              disabled={invoking[agentId]}
            >
              <i className={`fas ${invoking[agentId] ? 'fa-spinner fa-spin' : 'fa-play'}`}></i>
            </button>
          </div>
        );
        })}
        {(!agents || agents.length === 0) && (
          <div className="no-agents">Initializing neural links...</div>
        )}
      </div>

      <div className="agent-footer">
        <button className="fleet-action-btn">
          <i className="fas fa-sync-alt"></i> REFRESH CLUSTER
        </button>
      </div>
    </div>
  );
};

export default AgentPanel;
