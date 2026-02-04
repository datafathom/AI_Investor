/**
 * MenuBar Component
 *
 * Traditional desktop application-style menu bar with dropdown menus.
 * Fixed at the top of the application.
 */

import React, { useState, useRef, useEffect } from "react";
import useEducationStore from "../../stores/educationStore";
import { Settings } from "lucide-react";
import "./MenuBar.css";

const MENU_ITEMS = [
  {
    label: "File",
    items: [
      { label: "Market Dashboard", action: "show-dashboard" },
      { label: "Mission Control", action: "show-mission-control" },
      { label: "Political Alpha", action: "show-political-alpha" },
      { label: "Strategy Distillery", action: "show-strategy-distillery" },
      { label: "Debate Chamber", action: "show-debate-chamber" },
      { label: "Auto-Coder", action: "show-auto-coder" },
      { label: "VR Cockpit", action: "show-vr-cockpit" },
      { type: "divider" },
      { label: "Options Analytics", action: "show-options" },
      { label: "Backtest Portfolio", action: "show-backtest" },
      { label: "Virtual Brokerage", action: "show-brokerage" },
      { label: "Global Scanner", action: "show-scanner" },
      { type: "divider" },
      { label: "New Dashboard", action: "new-dashboard", shortcut: "Ctrl+N" },
      { label: "Open Dashboard", action: "open-dashboard", shortcut: "Ctrl+O" },
      { label: "Save Layout", action: "save-layout", shortcut: "Ctrl+S" },
      { type: "divider" },
      { label: "Export Layout", action: "export-layout" },
      { label: "Import Layout", action: "import-layout" },
      { type: "divider" },
      { label: "Exit", action: "exit" },
    ],
  },
  {
    label: "Edit",
    items: [
      { label: "Undo", action: "undo", shortcut: "Ctrl+Z", disabled: true },
      { label: "Redo", action: "redo", shortcut: "Ctrl+Y", disabled: true },
      { type: "divider" },
      { label: "Cut", action: "cut", shortcut: "Ctrl+X", disabled: true },
      { label: "Copy", action: "copy", shortcut: "Ctrl+C", disabled: true },
      { label: "Paste", action: "paste", shortcut: "Ctrl+V", disabled: true },
      { type: "divider" },
      { label: "Select All", action: "select-all", shortcut: "Ctrl+A" },
    ],
  },
  {
    label: "View",
    items: [
      { label: "Zoom In", action: "zoom-in", shortcut: "Ctrl++" },
      { label: "Zoom Out", action: "zoom-out", shortcut: "Ctrl+-" },
      { label: "Reset Zoom", action: "reset-zoom", shortcut: "Ctrl+0" },
      { type: "divider" },
      { label: "Toggle Dark Mode", action: "toggle-theme", shortcut: "Ctrl+T" },
      {
        label: "Toggle Fullscreen",
        action: "toggle-fullscreen",
        shortcut: "F11",
      },
      { type: "divider" },
      { label: "Debug States", action: "debug-states", shortcut: "" },
      {
        label: "Force Loading",
        action: "force-loading",
        shortcut: "",
        checked: false,
      },
      {
        label: "Force Error",
        action: "force-error",
        shortcut: "",
        checked: false,
      },
    ],
  },
  {
    label: "Roles",
    items: [
      {
        label: "The Architect",
        action: "nav-overview-architect",
        submenu: [
          { label: "System Health", action: "role-architect" },
          { label: "API & Integrations", action: "role-api" },
        ],
      },
      {
        label: "The Orchestrator",
        action: "nav-overview-workspace",
        submenu: [
          { label: "Master Graph", action: "role-orchestrator" },
          { label: "System Reflexivity", action: "role-orchestrator" },
        ],
      },
      {
        label: "The Strategist",
        action: "nav-overview-strategist",
        submenu: [
          { label: "Social Class Maintenance", action: "role-scm" },
          { label: "Currency & Cash", action: "role-strategist" },
          { label: "Estate Planning", action: "role-estate" },
          { label: "Philanthropy & Impact", action: "role-impact" },
          { label: "Corporate & Earnings", action: "role-corporate" },
          { label: "Zen Homeostasis", action: "show-zen" },
        ],
      },
      {
        label: "The Guardian",
        action: "nav-overview-guardian",
        submenu: [
          { label: "Compliance & KYC", action: "role-guardian" },
          { label: "Margin & Liquidity", action: "role-margin" },
          { label: "Regulatory Audit", action: "role-audit" },
          { label: "Mobile Warden", action: "role-warden" },
        ],
      },
      {
        label: "The Analyst",
        action: "nav-overview-analyst",
        submenu: [
          { label: "Debate Chamber", action: "role-analyst" },
          { label: "Macro Observer", action: "role-observer" },
          { label: "Stress Scenarios", action: "role-scenarios" },
        ],
      },
      { type: "divider" },
      {
        label: "Asset Classes",
        submenu: [
          { label: "Crypto & Web3", action: "show-crypto" },
          { label: "Fixed Income", action: "show-fixed-income" },
          { label: "Real Estate & Illiquid", action: "show-assets" }, // Upcoming 
        ],
      },
      { type: "divider" },
      { label: "Tax Optimisation", action: "show-tax" },
      { label: "Portfolio Attribution", action: "show-attribution" },
      { label: "Global Scanner", action: "show-scanner" },
      { label: "Backtest Explorer", action: "show-backtest" },
    ],
  },
  {
    label: "Routes",
    items: [
      {
        label: "Module Overviews",
        action: "nav-overview-workspace", // Primary landing
        submenu: [
          { label: "Orchestrator Overview", action: "nav-overview-orchestrator" },
          { label: "Architect Overview", action: "nav-overview-architect" },
          { label: "Analyst Overview", action: "nav-overview-analyst" },
          { label: "Trader Overview", action: "nav-overview-trader" },
          { label: "Strategist Overview", action: "nav-overview-strategist" },
          { label: "Data Scientist Overview", action: "nav-overview-data-scientist" },
          { label: "Marketing Overview", action: "nav-overview-marketing" },
          { label: "Legal Overview", action: "nav-overview-legal" },
          { label: "Guardian Overview", action: "nav-overview-guardian" },
          { label: "Data Scientist Overview", action: "nav-overview-pioneer" },
        ],
      },
      { type: "divider" },
      {
        label: "Orchestrator",
        action: "nav-overview-orchestrator",
        submenu: [
          { label: "Terminal Workspace", action: "show-dashboard" },
          { label: "Mission Control", action: "show-mission-control" },
          { label: "Master Graph Control", action: "role-orchestrator" },
          { label: "Global Chat", action: "show-chat" },
          { label: "Zen Mode", action: "show-zen" },
          { type: "divider" },
          { label: "Market Monitor", action: "toggle-widget-monitor-view" },
          { label: "Trade Tape", action: "toggle-widget-trade-tape-view" },
          { label: "Options Chain", action: "toggle-widget-options-chain-view" },
          { label: "Market Depth", action: "toggle-widget-market-depth-view" },
          { label: "System Log", action: "toggle-widget-system-log-view" },
        ],
      },
      {
        label: "Architect",
        action: "nav-overview-architect",
        submenu: [
          { label: "Cloud Admin Center", action: "nav-admin" },
          { label: "System Health", action: "role-architect" },
          { label: "API Dashboard", action: "role-api" },
          { label: "Third-Party Integrations", action: "nav-integrations" },
          { label: "Developer Platform", action: "nav-developer-platform" },
        ],
      },
       {
         label: "Data Scientist",
         action: "nav-overview-data-scientist",
         submenu: [
           { label: "AI Predictions", action: "nav-ai-predictions" },
           { label: "ML Pipeline", action: "nav-ml-training" },
           { label: "AI Colleague", action: "nav-ai-assistant" },
           { label: "Auto-Coder", action: "nav-autocoder" },
           { label: "Debate Chamber", action: "show-debate" },
           { label: "VR Cockpit", action: "show-vr" },
         ],
       },
      {
        label: "Trader",
        action: "nav-overview-trader",
        submenu: [
          { label: "Global Scanner", action: "show-scanner" },
          { label: "Options Strategy Builder", action: "nav-options-strategy" },
          { label: "Advanced Orders", action: "nav-advanced-orders" },
          { label: "Algorithmic Trading", action: "nav-algorithmic-trading" },
          { label: "Paper Trading", action: "nav-paper-trading" },
          { label: "Advanced Charting", action: "nav-advanced-charting" },
          { label: "Options Analytics", action: "show-options" },
        ],
      },
      {
        label: "Strategist",
        action: "nav-overview-strategist",
        submenu: [
          { label: "Portfolio Net Worth", action: "nav-portfolio-management" },
          { label: "Advanced Analytics", action: "nav-advanced-analytics" },
          { label: "Portfolio Optimization", action: "nav-portfolio-optimization" },
          { label: "Portfolio Attribution", action: "show-attribution" },
          { label: "Backtest Explorer", action: "show-backtest" },
          { label: "Virtual Brokerage", action: "show-brokerage" },
          { type: "divider" },
          { label: "Crypto & Web3 Assets", action: "show-crypto" },
          { label: "Fixed Income", action: "show-fixed-income" },
          { label: "Assets & Illiquids", action: "show-assets" },
          { type: "divider" },
          { label: "Corporate Actions", action: "role-corporate" },
          { label: "Philanthropy & Impact", action: "role-impact" },
          { label: "Social Class Maintenance", action: "role-scm" },
          { type: "divider" },
          { label: "Estate Planning", action: "nav-estate-planning" },
          { label: "Retirement Planning", action: "nav-retirement-planning" },
          { label: "Budgeting & Planning", action: "nav-budgeting" },
          { label: "Financial Planning", action: "nav-financial-planning" },
        ],
      },
      {
        label: "Marketing",
        action: "nav-overview-marketing",
        submenu: [
          { label: "News & Sentiment Analysis", action: "nav-news-sentiment" },
          { label: "Social Trading", action: "nav-social-trading" },
          { label: "Community Forums", action: "nav-community-forums" },
          { label: "Education Platform", action: "nav-education" },
          { label: "Extension Marketplace", action: "nav-marketplace" },
          { label: "Research Reports", action: "nav-research-reports" },
          { label: "Watchlists & Alerts", action: "nav-watchlists-alerts" },
        ],
      },
      {
        label: "Lawyer",
        action: "nav-overview-legal",
        submenu: [
          { label: "Compliance & KYC", action: "role-guardian" },
          { label: "Regulatory Audit", action: "role-audit" },
          { label: "Stress Scenarios", action: "role-scenarios" },
          { label: "Margin Management", action: "role-margin" },
          { label: "Tax Optimization", action: "show-tax" },
          { label: "Legal Terms", action: "nav-legal-terms" },
          { label: "Privacy Policy", action: "nav-legal-privacy" },
        ],
      },
      {
        label: "Guardian",
        action: "nav-overview-guardian",
        submenu: [
          { label: "Advanced Risk Management", action: "nav-advanced-risk" },
          { label: "Credit Monitoring", action: "nav-credit-monitoring" },
          { label: "Institutional Tools", action: "nav-institutional" },
          { label: "Enterprise Features", action: "nav-enterprise" },
          { label: "Bill Payments", action: "nav-bill-payment" },
          { label: "Cash Flow Tracking", action: "show-cash-flow" },
          { label: "Family Office", action: "show-tenant" },
          { label: "Mobile Companion", action: "role-warden" },
        ],
      },
      {
        label: "Data Scientist",
        action: "nav-overview-pioneer",
        submenu: [
          { label: "Auto-Coder Dashboard", action: "show-auto-coder" },
          { label: "Auto-Coder Sandbox", action: "show-sandbox" },
          { label: "VR Cockpit", action: "show-vr-cockpit" },
          { label: "Debate Chamber", action: "show-debate-chamber" },
        ],
      },
      { type: "divider" },
      { label: "Mobile Dashboard", action: "role-warden" },
    ],
  },
  {
    label: "Widgets",
    items: [], // Will be populated dynamically
  },
  {
    label: "Selection",
    items: [
      {
        label: "Select All Widgets",
        action: "select-all-widgets",
        shortcut: "Ctrl+Shift+A",
      },
      { label: "Deselect All", action: "deselect-all" },
      { type: "divider" },
      // Lock toggle will be dynamically injected
      { type: "divider" },
      { label: "Reset Layout", action: "reset-layout" },
    ],
  },
  {
    label: "Tools",
    items: [
      { label: "Widget Settings", action: "widget-settings" },
      { label: "Layout Manager", action: "layout-manager" },
      { type: "divider" },
      { label: "Developer Tools", action: "dev-tools", shortcut: "F12" },
      { label: "Console", action: "console" },
    ],
  },
  {
    label: "Help",
    items: [
      { label: "Documentation", action: "docs" },
      { label: "Keyboard Shortcuts", action: "shortcuts", shortcut: "?" },
      { type: "divider" },
      { label: "About", action: "about" },
      { type: "divider" },
      {
        label: "Legal",
        submenu: [
          { label: "Terms of Service", action: "nav-legal-terms" },
          { label: "Privacy Policy", action: "nav-legal-privacy" },
        ],
      },
    ],
  },
];

export default function MenuBar({
  onMenuAction,
  isDarkMode,
  widgetVisibility,
  onToggleWidget,
  onTriggerModal,
  onResetLayout,
  toggleTheme,
  onAutoSort,
  onSaveLayout,
  onLoadLayout,
  onToggleLogCenter,
  showLogCenter,
  debugStates,
  widgetTitles = {},
  currentUser,
  onLogout,
  onSignin,
  // Widget lock
  globalLock = false,
  // Workspaces
  activeWorkspace,
  workspaces = [],
  onLoadWorkspace,
  onSaveWorkspacePrompt,
}) {
  const [activeMenu, setActiveMenu] = useState(null);
  const menuRefs = useRef({});
  const menuBarRef = useRef(null);

  const [localUser, setLocalUser] = useState(currentUser);

  useEffect(() => {
    setLocalUser(currentUser);
  }, [currentUser]);

  useEffect(() => {
    const handleProfileUpdate = () => {
      setLocalUser(authService.getCurrentUser());
    };
    window.addEventListener('user-profile-update', handleProfileUpdate);
    return () => window.removeEventListener('user-profile-update', handleProfileUpdate);
  }, []);

  const AI_INVESTOR_IDS = [
    "monitor-view",
    "command-view",
    "research-view",
    "portfolio-view",
    "homeostasis-view",
    "options-chain-view",
    "market-depth-view",
    "trade-tape-view",
  ];

  // Build widgets menu dynamically
  const menuItemsWithWidgets = MENU_ITEMS.map((menu) => {
    if (menu.label === "Routes") {
      return {
        ...menu,
        items: menu.items.map((routeItem) => {
          if (routeItem.label === "Orchestrator") {
            const investorWidgets = Object.entries(widgetTitles)
              .filter(([id]) => AI_INVESTOR_IDS.includes(id))
              .map(([id, name]) => ({ id, name }))
              .sort((a, b) => a.name.localeCompare(b.name));

            return {
              ...routeItem,
              submenu: [
                ...routeItem.submenu,
                { type: "divider" },
                ...investorWidgets.map(({ id, name }) => ({
                  label: name,
                  action: `toggle-widget-${id}`,
                  checked: widgetVisibility?.[id] !== false,
                })),
              ],
            };
          }
          return routeItem;
        }),
      };
    }
    if (menu.label === "Widgets") {
      // Sort widgets alphabetically by their display name
      const otherWidgets = Object.entries(widgetTitles)
        .filter(([id]) => !AI_INVESTOR_IDS.includes(id))
        .map(([id, name]) => ({ id, name }))
        .sort((a, b) => a.name.localeCompare(b.name));

      return {
        ...menu,
        items: [
          // "Open All Widgets" action at the top
          { label: "Open All Widgets", action: "open-all-widgets" },
          // "Close All Widgets" action
          { label: "Close All Widgets", action: "close-all-widgets" },
          // Separator
          { type: "divider" },
          // Individual widget toggles (alphabetically sorted)
          ...otherWidgets.map(({ id, name }) => ({
            label: name,
            action: `toggle-widget-${id}`,
            checked: widgetVisibility?.[id] !== false,
          })),
        ],
      };
    }
    if (menu.label === "View") {
      return {
        ...menu,
        items: menu.items.map((item) => {
          if (item.action === "force-loading") {
            return { ...item, checked: debugStates?.forceLoading || false };
          }
          if (item.action === "force-error") {
            return { ...item, checked: debugStates?.forceError || false };
          }
          return item;
        }),
      };
    }
    if (menu.label === "Workspaces") {
      return {
        ...menu,
        items: [
          ...menu.items,
          ...workspaces.map((name) => ({
            label: name,
            action: `load-workspace-${name}`,
            checked: name === activeWorkspace,
          })),
        ],
      };
    }
    if (menu.label === "Selection") {
      // Inject dynamic lock toggle
      return {
        ...menu,
        items: [
          {
            label: "Select All Widgets",
            action: "select-all-widgets",
            shortcut: "Ctrl+Shift+A",
          },
          { label: "Deselect All", action: "deselect-all" },
          { type: "divider" },
          {
            label: globalLock ? "🔒 Unlock Widgets" : "🔓 Lock Widgets",
            action: "toggle-lock",
            icon: globalLock ? "lock" : "unlock",
          },
          { type: "divider" },
          { label: "Reset Layout", action: "reset-layout" },
        ],
      };
    }
    return menu;
  });

  // Add Account menu at the end
  const finalMenuItems = [
    ...menuItemsWithWidgets,
    {
      label: "Account",
      items: localUser
        ? [
            { 
              type: "account-profile", 
              label: localUser?.username || "Account", 
              action: "nav-account" 
            },
            { type: "divider" },
            {
              label: (
                <span className="menu-label-with-icon">
                  <Settings size={14} className="menu-icon" /> Settings
                </span>
              ),
              action: "nav-account-settings",
              submenu: [
                {
                  label: "Layout",
                  submenu: [
                    { label: "Save Layout", action: "save-layout" },
                    { label: "Load Layout", action: "load-layout" },
                    { label: "Reset Layout", action: "reset-layout" },
                    { label: "AutoSort Current Page", action: "auto-sort" },
                    { label: "Sync Cloud Layout", action: "save-layout" },
                    { type: "divider" },
                    {
                      label: "Workspaces",
                      action: "workspace-save-prompt",
                      shortcut: "Ctrl+Shift+S",
                    },
                    { label: "Import Layout", action: "import-layout" },
                    { label: "Export Layout", action: "export-layout" },
                    { type: "divider" },
                    ...workspaces.map((name) => ({
                      label: name,
                      action: `load-workspace-${name}`,
                      checked: name === activeWorkspace,
                    })),
                  ],
                },
              ],
            },
            { type: "divider" },
            { label: "Logout", action: "logout" },
          ]
        : [{ label: "Sign In / Register", action: "signin" }],
    },
  ];

  const userForDisplay = localUser || currentUser;

  const renderMenuItems = (items) => {
    return items.map((item, index) => {
      if (item.type === "divider") {
        return <div key={`divider-${index}`} className="menu-divider" />;
      }

      if (item.type === "account-profile") {
        return (
          <div 
            key={`profile-${index}`} 
            className="menu-account-profile-item"
            onClick={(e) => handleMenuItemClick(item.action, e)}
          >
            <div className="profile-avatar-circle">
              {userForDisplay?.avatar ? (
                <img src={userForDisplay.avatar} alt="Avatar" className="w-full h-full object-cover" />
              ) : (
                <span className="profile-initials">{userForDisplay?.username?.charAt(0).toUpperCase() || 'A'}</span>
              )}
            </div>
            <div className="profile-info">
              <span className="profile-label">{userForDisplay?.username || "Account"}</span>
              <span className="profile-subtitle">Signed in as {userForDisplay?.email || userForDisplay?.username || 'Admin'}</span>
            </div>
          </div>
        );
      }

      const isChecked = item.checked !== undefined && item.checked;
      const hasSubmenu = item.submenu && item.submenu.length > 0;

      return (
        <div
          key={`menu-item-${index}`}
          className={`menu-dropdown-item ${item.disabled ? "disabled" : ""} ${isChecked ? "checked" : ""} ${hasSubmenu ? "has-submenu" : ""}`}
          onClick={(e) => {
            if (!item.disabled) {
              if (hasSubmenu && item.action) {
                // Submenu headers are now clickable if they have an action
                handleMenuItemClick(item.action, e);
              } else if (!hasSubmenu) {
                if (typeof item.action === "string" && item.action.startsWith("toggle-widget-")) {
                  const widgetId = item.action.replace("toggle-widget-", "");
                  if (onToggleWidget) {
                    onToggleWidget(widgetId);
                  }
                  e.stopPropagation();
                } else {
                  handleMenuItemClick(item.action, e);
                }
              }
            }
          }}
          tabIndex={item.disabled ? -1 : 0}
          role="menuitem"
          aria-disabled={item.disabled}
          aria-checked={isChecked}
          aria-haspopup={hasSubmenu}
          aria-expanded={false}
        >
          {item.checked !== undefined && (
            <span className="menu-checkmark">{isChecked ? "" : ""}</span>
          )}

          {hasSubmenu ? (
            <div className="menu-submenu-trigger">
              <span className="menu-item-label">{item.label}</span>
              <span className="menu-submenu-arrow">▶</span>
            </div>
          ) : (
            <span className="menu-item-label">{item.label}</span>
          )}

          {item.shortcut && (
            <span className="menu-item-shortcut">{item.shortcut}</span>
          )}

          {/* Recursive Sub-menu Rendering */}
          {hasSubmenu && (
            <div className="menu-submenu">
              {renderMenuItems(item.submenu)}
            </div>
          )}
        </div>
      );
    });
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuBarRef.current && !menuBarRef.current.contains(event.target)) {
        setActiveMenu(null);
      }
    };

    const handleEscape = (event) => {
      if (event.key === "Escape") {
        setActiveMenu(null);
      }
    };

    if (activeMenu !== null) {
      document.addEventListener("mousedown", handleClickOutside);
      document.addEventListener("keydown", handleEscape);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("keydown", handleEscape);
    };
  }, [activeMenu]);

  const handleMenuClick = (menuLabel) => {
    setActiveMenu(activeMenu === menuLabel ? null : menuLabel);
  };

  const handleMenuItemClick = (action, event) => {
    event.stopPropagation();
    setActiveMenu(null);

    if (action === "workspace-save-prompt") {
      onSaveWorkspacePrompt();
      return;
    }
    if (action?.startsWith("load-workspace-")) {
      const name = action.replace("load-workspace-", "");
      onLoadWorkspace(name);
      return;
    }

    if (action === "logout" && onLogout) {
      onLogout();
    }
    if (action === "signin" && onSignin) {
      onSignin();
    }

    if (action === "auto-sort") {
      onAutoSort();
      return;
    }

    if (onMenuAction) {
      onMenuAction(action);
    }
  };

  const handleKeyDown = (event, menuLabel) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      handleMenuClick(menuLabel);
    } else if (event.key === "ArrowRight" && activeMenu === menuLabel) {
      event.preventDefault();
      const currentIndex = MENU_ITEMS.findIndex((m) => m.label === menuLabel);
      const nextIndex = (currentIndex + 1) % MENU_ITEMS.length;
      setActiveMenu(MENU_ITEMS[nextIndex].label);
    } else if (event.key === "ArrowLeft" && activeMenu === menuLabel) {
      event.preventDefault();
      const currentIndex = MENU_ITEMS.findIndex((m) => m.label === menuLabel);
      const prevIndex =
        (currentIndex - 1 + MENU_ITEMS.length) % MENU_ITEMS.length;
      setActiveMenu(MENU_ITEMS[prevIndex].label);
    }
  };

  return (
    <div
      className={`menu-bar ${isDarkMode ? "dark" : "light"}`}
      ref={menuBarRef}
    >
      <div className="menu-bar-left">
        {finalMenuItems.map((menu) => (
          <div
            key={menu.label}
            className={`menu-item ${activeMenu === menu.label ? "active" : ""}`}
            onClick={() => handleMenuClick(menu.label)}
            onKeyDown={(e) => handleKeyDown(e, menu.label)}
            tabIndex={0}
            role="menuitem"
            aria-haspopup="true"
            aria-expanded={activeMenu === menu.label}
          >
            {menu.label}
            {activeMenu === menu.label && (
              <div
                className="menu-dropdown"
                ref={(el) => (menuRefs.current[menu.label] = el)}
              >
                {renderMenuItems(menu.items)}
              </div>
            )}
          </div>
        ))}
      </div>
      <div className="menu-bar-right">
        <button
          className="menu-bar-button menu-bar-zoom-button"
          onClick={() => {}}
          title="Zoom out all widgets"
          aria-label="Zoom out all widgets"
          disabled
        >
          <span className="zoom-icon"></span>
          <span className="zoom-symbol"></span>
        </button>
        <button
          className="menu-bar-button menu-bar-zoom-button"
          onClick={() => {}}
          title="Zoom in all widgets"
          aria-label="Zoom in all widgets"
          disabled
        >
          <span className="zoom-icon"></span>
          <span className="zoom-symbol">+</span>
        </button>

        <button
          className="menu-bar-button"
          onClick={onToggleLogCenter}
          title="Toggle log center"
        >
          {showLogCenter ? "Hide" : "Show"} Logs
        </button>
        {/* Education Mode Toggle */}
        <div className="menu-bar-theme-toggle" role="group" aria-label="Education mode toggle" style={{ marginRight: '1rem' }}>
            <span style={{ fontSize: '0.8rem' }}>🎓 Edu Mode</span>
            <label className="switch">
                <input
                    type="checkbox"
                    checked={useEducationStore((state) => state.isEducationMode)}
                    onChange={useEducationStore((state) => state.toggleEducationMode)}
                    aria-label="Toggle education mode"
                />
                <span className="slider" style={{ backgroundColor: useEducationStore.getState().isEducationMode ? '#06b6d4' : '#ccc' }} />
            </label>
        </div>

        <div
          className="menu-bar-theme-toggle"
          role="group"
          aria-label="Theme toggle"
        >
          <span>Light</span>
          <label className="switch">
            <input
              type="checkbox"
              checked={isDarkMode}
              onChange={toggleTheme}
              aria-label="Toggle dark mode"
            />
            <span className="slider" />
          </label>
          <span>Dark</span>
        </div>
      </div>
    </div>
  );
}
