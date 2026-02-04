import React, { useState } from 'react';
import { Plus, X, Zap, TrendingUp, DollarSign, Bell, Settings } from 'lucide-react';
import './QuickActions.css';

const DEFAULT_ACTIONS = [
  { id: 'trade', icon: TrendingUp, label: 'Quick Trade', color: 'var(--neon-green)' },
  { id: 'deposit', icon: DollarSign, label: 'Deposit', color: 'var(--neon-cyan)' },
  { id: 'alert', icon: Bell, label: 'Set Alert', color: 'var(--neon-yellow)' },
  { id: 'settings', icon: Settings, label: 'Settings', color: 'var(--neon-purple)' },
];

/**
 * Floating action button with expandable quick actions.
 * 
 * @param {Array} actions - Custom actions { id, icon, label, color, onClick }
 * @param {string} position - 'bottom-right' | 'bottom-left'
 */
const QuickActions = ({
  actions = DEFAULT_ACTIONS,
  position = 'bottom-right',
  onAction
}) => {
  const [isOpen, setIsOpen] = useState(false);

  const handleAction = (action) => {
    onAction?.(action.id);
    setIsOpen(false);
  };

  return (
    <div className={`quick-actions quick-actions--${position}`}>
      {/* Action buttons */}
      <div className={`quick-actions__menu ${isOpen ? 'quick-actions__menu--open' : ''}`}>
        {actions.map((action, idx) => {
          const Icon = action.icon;
          return (
            <button
              key={action.id}
              className="quick-actions__item"
              style={{ 
                '--action-color': action.color,
                '--delay': `${idx * 0.05}s`
              }}
              onClick={() => handleAction(action)}
              aria-label={action.label}
            >
              <Icon size={18} />
              <span className="quick-actions__label">{action.label}</span>
            </button>
          );
        })}
      </div>

      {/* Main FAB */}
      <button
        className={`quick-actions__fab ${isOpen ? 'quick-actions__fab--open' : ''}`}
        onClick={() => setIsOpen(!isOpen)}
        aria-label={isOpen ? 'Close menu' : 'Open quick actions'}
        aria-expanded={isOpen}
      >
        {isOpen ? <X size={24} /> : <Plus size={24} />}
      </button>
    </div>
  );
};

export default QuickActions;
