import React, { useMemo } from 'react';
import { ShieldCheck, Activity, Zap, Cpu, Terminal } from 'lucide-react';
import './PageContextPanel.css';

/**
 * PageContextPanel - Unified header and telemetry window for all OS pages
 */
const PageContextPanel = ({ 
  title, 
  pageTitle = "", // Specific page name (e.g., "Strategic Missions")
  status = "SYSTEM_ACTIVE", 
  color = "#00f2ff", 
  telemetry = [],
  isDashboard = false,
  subPages = [],
  onNavigate = () => {},
  icon: IconComponent = Terminal
}) => {
  const [isDropdownOpen, setIsDropdownOpen] = React.useState(false);
  const dropdownRef = React.useRef(null);
  const neuralLoad = useMemo(() => (Math.random() * 15 + 5).toFixed(1), []);
  const currentTime = useMemo(() => new Date().toLocaleTimeString(), []);

  // Close dropdown on outside click
  React.useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsDropdownOpen(false);
      }
    };

    if (isDropdownOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isDropdownOpen]);

  const handleHeaderClick = () => {
    if (subPages.length > 0 || isDashboard) {
      setIsDropdownOpen(!isDropdownOpen);
    }
  };

  return (
    <div className="page-context-panel" style={{ '--accent': color }}>
      <div className="context-header">
        <div 
          ref={dropdownRef}
          className={`title-section has-dropdown ${isDropdownOpen ? 'active' : ''}`}
          onClick={handleHeaderClick}
        >
          <div className="context-icon">
            <IconComponent size={60} />
          </div>
          <div className="context-text">
            <div className="context-brand">CONTEXT WEAVER // {status}</div>
            <div className="title-row">
              <h1 className="context-title">{title.toUpperCase()}</h1>
              <IconComponent size={20} className="title-icon-inline" />
              {pageTitle && <span className="page-title-inline">{pageTitle}</span>}
            </div>
          </div>
          <div className={`dropdown-indicator ${(subPages.length > 0) ? 'visible' : ''} ${isDropdownOpen ? 'open' : ''}`}>▼</div>

          {isDropdownOpen && (
            <div className="context-title-dropdown" onClick={(e) => e.stopPropagation()}>
              <div className="dropdown-header">NAVIGATION</div>
              
              {/* Primary Dashboard Link */}
              <button 
                className={`dropdown-item dashboard-link ${isDashboard ? 'active' : ''}`}
                onClick={() => {
                  onNavigate('dashboard');
                  setIsDropdownOpen(false);
                }}
              >
                <IconComponent size={16} className="dropdown-item-icon" />
                <span className="item-label">{title.toUpperCase()} DASHBOARD</span>
                <span className="item-arrow">→</span>
              </button>

              {subPages.length > 0 && <div className="dropdown-divider" />}

              {/* Sub-Modules */}
              {subPages.map((page, idx) => (
                <button 
                  key={idx} 
                  className="dropdown-item"
                  onClick={() => {
                    onNavigate(page.path);
                    setIsDropdownOpen(false);
                  }}
                >
                  <span className="item-label">{page.label.toUpperCase()}</span>
                  <span className="item-arrow">→</span>
                </button>
              ))}
            </div>
          )}
        </div>
        
        <div className="telemetry-grid">
          {telemetry.map((item, idx) => (
            <div key={idx} className={`telem-item ${item.className || ''}`}>
              <div className="telem-label">{item.label.toUpperCase()}</div>
              <div className={`telem-value ${item.variant || ''}`}>
                {item.value}
                {item.showBar && (
                  <div className="telem-mini-bar">
                    <div className="bar-fill" style={{ width: `${item.barValue || 0}%` }}></div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
      <div className="panel-edge-accents">
        <div className="edge-L" />
        <div className="edge-R" />
      </div>
    </div>
  );
};

export default PageContextPanel;
