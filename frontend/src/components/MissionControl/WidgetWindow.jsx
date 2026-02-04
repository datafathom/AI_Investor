import React, { useState } from 'react';
import { ChevronUp, ChevronDown, Maximize2, Minimize2 } from 'lucide-react';
import './WidgetWindow.css';

/**
 * WidgetWindow
 * 
 * An OS-style window wrapper for dashboard widgets.
 * Handles:
 * - Title Bar with controls
 * - Roll-up/Down (Shading) logic
 * - Internal scroll vault (flex-grow: 1, overflow: auto)
 * - Container query context for children
 */
const WidgetWindow = ({ 
  title, 
  children, 
  icon: Icon,
  onToggleMaximize,
  isMaximized = false,
  className = ""
}) => {
  const [isRolledUp, setIsRolledUp] = useState(false);

  const toggleRollup = (e) => {
    e.stopPropagation();
    setIsRolledUp(!isRolledUp);
  };

  return (
    <div className={`os-window ${isRolledUp ? 'is-rolled-up' : ''} ${className} flex flex-col h-full bg-slate-900/40 border border-slate-800 rounded-xl overflow-hidden glass-panel`}>
      {/* OS Title Bar */}
      <div className="window-title-bar flex items-center justify-between px-3 py-1.5 bg-slate-800/50 cursor-grab border-b border-white/5 active:bg-slate-700/50 transition-colors">
        <div className="flex items-center gap-2 overflow-hidden">
          {Icon && <Icon size={12} className="text-cyan-400 flex-shrink-0" />}
          <span className="font-mono text-[10px] uppercase font-bold text-slate-300 truncate tracking-wider">
            {title}
          </span>
        </div>
        
        <div className="window-controls flex items-center gap-1.5">
          <button 
            onClick={toggleRollup}
            className="window-control-btn hover:bg-white/10 p-1 rounded transition-colors"
            title={isRolledUp ? "Roll Down" : "Roll Up"}
          >
            {isRolledUp ? <ChevronDown size={14} /> : <ChevronUp size={14} />}
          </button>
          {onToggleMaximize && (
            <button 
              onClick={(e) => { e.stopPropagation(); onToggleMaximize(); }}
              className="window-control-btn hover:bg-white/10 p-1 rounded transition-colors"
              title={isMaximized ? "Restore" : "Maximize"}
            >
              {isMaximized ? <Minimize2 size={12} /> : <Maximize2 size={12} />}
            </button>
          )}
        </div>
      </div>

      {/* Internal Content (Scroll Vault) */}
      {!isRolledUp && (
        <div className="window-content flex-grow overflow-auto scroll-vault relative p-4 custom-scrollbar">
          {children}
        </div>
      )}
      
      {/* Decorative footer line if not rolled up */}
      {!isRolledUp && (
        <div className="window-status-bar h-1 bg-white/5 w-full mt-auto" />
      )}
    </div>
  );
};

export default WidgetWindow;
