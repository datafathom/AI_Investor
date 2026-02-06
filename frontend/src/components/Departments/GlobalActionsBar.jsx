import React from 'react';
import { ShieldAlert, Snowflake, Eraser, Zap, Info } from 'lucide-react';
import './GlobalActionsBar.css';

const ACTIONS = [
  {
    id: 'panic',
    label: 'PANIC MODE',
    icon: ShieldAlert,
    color: '#ff4757',
    description: 'Kill all execution and halt systems immediately.',
    auth: 'admin'
  },
  {
    id: 'cold-haven',
    label: 'COLD HAVEN',
    icon: Snowflake,
    color: '#00f2ff',
    description: 'Sweep all liquid assets to cold storage.',
    auth: 'admin'
  },
  {
    id: 'prune',
    label: 'MORNING SWEEP',
    icon: Eraser,
    color: '#2ed573',
    description: 'Auto-prune underperforming agent prompts.',
    auth: 'user'
  },
  {
    id: 'conserve',
    label: 'RESOURCE CONSERVE',
    icon: Zap,
    color: '#eccc68',
    description: 'Switch to local LLMs and minimize token usage.',
    auth: 'user'
  }
];

const GlobalActionsBar = ({ onAction }) => {
  return (
    <div className="global-actions-bar os-integrated">
      <div className="bar-header">
        <Info size={14} />
        <span>SYSTEM COMMAND OVERRIDE</span>
      </div>
      <div className="actions-list">
        {ACTIONS.map(action => (
          <button 
            key={action.id} 
            className="action-btn" 
            style={{ '--action-color': action.color }}
            onClick={() => onAction(action)}
            title={action.description}
          >
            <action.icon size={18} />
            <span className="btn-label">{action.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
};

export default GlobalActionsBar;
