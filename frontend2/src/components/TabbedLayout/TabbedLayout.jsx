/**
 * Tabbed Layout Component
 * 
 * Tab-based layout for organizing content.
 * Supports multiple tabs with close functionality.
 */

import React, { useState } from 'react';
import './TabbedLayout.css';

export default function TabbedLayout({
  tabs,
  defaultTab,
  onTabChange,
  onTabClose,
  closable = true,
}) {
  const [activeTab, setActiveTab] = useState(defaultTab || tabs[0]?.id);

  const handleTabClick = (tabId) => {
    setActiveTab(tabId);
    if (onTabChange) {
      onTabChange(tabId);
    }
  };

  const handleTabClose = (e, tabId) => {
    e.stopPropagation();
    
    if (onTabClose) {
      onTabClose(tabId);
    }

    // If closing active tab, switch to another
    if (tabId === activeTab) {
      const remainingTabs = tabs.filter(t => t.id !== tabId);
      if (remainingTabs.length > 0) {
        const newActiveTab = remainingTabs[0].id;
        setActiveTab(newActiveTab);
        if (onTabChange) {
          onTabChange(newActiveTab);
        }
      }
    }
  };

  const activeTabContent = tabs.find(t => t.id === activeTab);

  return (
    <div className="tabbed-layout">
      <div className="tabbed-layout-tabs">
        {tabs.map((tab) => (
          <div
            key={tab.id}
            className={`tabbed-layout-tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => handleTabClick(tab.id)}
          >
            {tab.icon && (
              <span className="tabbed-layout-tab-icon">{tab.icon}</span>
            )}
            <span className="tabbed-layout-tab-label">{tab.label}</span>
            {closable && tab.closable !== false && (
              <button
                className="tabbed-layout-tab-close"
                onClick={(e) => handleTabClose(e, tab.id)}
                title="Close tab"
              >
                ×
              </button>
            )}
          </div>
        ))}
      </div>
      <div className="tabbed-layout-content">
        {activeTabContent && activeTabContent.content}
      </div>
    </div>
  );
}

