/**
 * MenuBar Component
 *
 * Traditional desktop application-style menu bar with dropdown menus.
 * Fixed at the top of the application.
 */

import React, { useState, useRef, useEffect } from "react";
import useEducationStore from "../../stores/educationStore";
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
        submenu: [
          { label: "System Health", action: "role-architect" },
          { label: "API & Integrations", action: "role-api" },
        ],
      },
      {
        label: "The Strategist",
        submenu: [
          { label: "Currency & Cash", action: "role-strategist" },
          { label: "Estate Planning", action: "role-estate" },
          { label: "Philanthropy & Impact", action: "role-impact" },
          { label: "Corporate & Earnings", action: "role-corporate" },
          { label: "Zen Homeostasis", action: "show-zen" },
        ],
      },
      {
        label: "The Guardian",
        submenu: [
          { label: "Compliance & KYC", action: "role-guardian" },
          { label: "Margin & Liquidity", action: "role-margin" },
          { label: "Regulatory Audit", action: "role-audit" },
          { label: "Mobile Warden", action: "role-warden" },
        ],
      },
      {
        label: "The Analyst",
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
          { label: "Real Estate & Illiquid", action: "show-assets" }, // Upcoming Phase 24
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
        submenu: [
          { label: "Core Workspace Overview", action: "nav-overview-workspace" },
          { label: "Analytics Overview", action: "nav-overview-analytics" },
          { label: "Portfolio Overview", action: "nav-overview-portfolio" },
          { label: "Analyst Overview", action: "nav-overview-analyst" },
          { label: "Guardian Overview", action: "nav-overview-guardian" },
          { label: "Strategist Overview", action: "nav-overview-strategist" },
          { label: "Architect Overview", action: "nav-overview-architect" },
          { label: "Observer Overview", action: "nav-overview-observer" },
          { label: "Scanner Overview", action: "nav-overview-scanner" },
        ],
      },
      { type: "divider" },
      {
        label: "Core Workspaces",
        submenu: [
          { label: "Terminal Workspace", action: "show-dashboard" },
          { label: "Mission Control", action: "show-mission-control" },
          { label: "Auto-Coder Dashboard", action: "show-auto-coder" },
          { label: "Auto-Coder Sandbox", action: "show-sandbox" },
          { label: "VR Cockpit", action: "show-vr-cockpit" },
          { label: "Chat", action: "show-chat" },
        ],
      },
      {
        label: "Analysis & Logic",
        submenu: [
          { label: "Political Alpha", action: "show-political-alpha" },
          { label: "Strategy Distillery", action: "show-strategy-distillery" },
          { label: "Options Analytics", action: "show-options" },
          { label: "Backtest Explorer", action: "show-backtest" },
          { label: "Debate Chamber", action: "show-debate-chamber" },
        ],
      },
      {
        label: "Portfolio Management",
        submenu: [
          { label: "Virtual Brokerage", action: "show-brokerage" },
          { label: "Global Scanner", action: "show-scanner" },
          { label: "Portfolio Attribution", action: "show-attribution" },
          { label: "Fixed Income", action: "show-fixed-income" },
          { label: "Crypto & Web3", action: "show-crypto" },
          { label: "Tax Optimization", action: "show-tax" },
          { label: "Assets & Illiquid", action: "show-assets" },
          { label: "Cash Flow", action: "show-cash-flow" },
          { label: "Family Office (Tenants)", action: "show-tenant" },
          { type: "divider" },
          { label: "Advanced Portfolio Analytics", action: "nav-advanced-analytics" },
          { label: "Portfolio Optimization", action: "nav-portfolio-optimization" },
          { label: "Advanced Risk Management", action: "nav-advanced-risk" },
          { label: "Tax Optimization (Enhanced)", action: "nav-tax-optimization" },
        ],
      },
      {
        label: "Trading & Execution",
        submenu: [
          { label: "Options Strategy Builder", action: "nav-options-strategy" },
          { label: "Advanced Orders", action: "nav-advanced-orders" },
          { label: "Paper Trading", action: "nav-paper-trading" },
          { label: "Algorithmic Trading", action: "nav-algorithmic-trading" },
        ],
      },
      {
        label: "Financial Planning",
        submenu: [
          { label: "Financial Planning", action: "nav-financial-planning" },
          { label: "Retirement Planning", action: "nav-retirement-planning" },
          { label: "Estate Planning", action: "nav-estate-planning" },
          { label: "Budgeting", action: "nav-budgeting" },
          { label: "Bill Payment", action: "nav-bill-payment" },
          { label: "Credit Monitoring", action: "nav-credit-monitoring" },
        ],
      },
      {
        label: "Market Intelligence",
        submenu: [
          { label: "News & Sentiment Analysis", action: "nav-news-sentiment" },
          { label: "Watchlists & Alerts", action: "nav-watchlists-alerts" },
          { label: "Research Reports", action: "nav-research-reports" },
          { label: "Advanced Charting", action: "nav-advanced-charting" },
        ],
      },
      {
        label: "Social & Community",
        submenu: [
          { label: "Social Trading", action: "nav-social-trading" },
          { label: "Community Forums", action: "nav-community-forums" },
          { label: "Education Platform", action: "nav-education" },
        ],
      },
      {
        label: "AI & Machine Learning",
        submenu: [
          { label: "AI Predictions", action: "nav-ai-predictions" },
          { label: "AI Assistant", action: "nav-ai-assistant" },
          { label: "ML Training Pipeline", action: "nav-ml-training" },
        ],
      },
      {
        label: "Integrations & Platform",
        submenu: [
          { label: "Third-Party Integrations", action: "nav-integrations" },
          { label: "Developer Platform", action: "nav-developer-platform" },
          { label: "Extension Marketplace", action: "nav-marketplace" },
        ],
      },
      {
        label: "Enterprise & Compliance",
        submenu: [
          { label: "Enterprise Features", action: "nav-enterprise" },
          { label: "Compliance & Reporting", action: "nav-compliance" },
          { label: "Institutional Tools", action: "nav-institutional" },
        ],
      },

      {
        label: "Role: The Guardian",
        submenu: [
          { label: "Compliance & KYC", action: "role-guardian" },
          { label: "Regulatory Audit", action: "role-audit" },
          { label: "Stress Scenarios", action: "role-scenarios" },
          { label: "Margin Management", action: "role-margin" },
        ],
      },
      {
        label: "Role: The Strategist",
        submenu: [
          { label: "Estate Planning", action: "role-estate" },
          { label: "Philanthropy & Impact", action: "role-impact" },
          { label: "Corporate Actions", action: "role-corporate" },
          { label: "Currency & Cash", action: "role-strategist" },
        ],
      },
      {
        label: "Role: The Architect",
        submenu: [
          { label: "System Health", action: "role-architect" },
          { label: "API Dashboard", action: "role-api" },
        ],
      },
      {
        label: "Role: The Observer",
        submenu: [{ label: "Macro Observer", action: "role-observer" }],
      },
      { type: "divider" },
      {
        label: "Special Modes",
        submenu: [
          { label: "Mobile Dashboard", action: "role-warden" },
          { label: "Zen Mode", action: "show-zen" },
        ],
      },
    ],
  },
  {
    label: "AI Investor",
    items: [], // Will be populated dynamically
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
    label: "Workspaces",
    items: [
      {
        label: "Save As...",
        action: "workspace-save-prompt",
        shortcut: "Ctrl+Shift+S",
      },
      { label: "Import Layout", action: "import-layout" },
      { label: "Export Layout", action: "export-layout" },
      { type: "divider" },
      // Dynamic workspaces will be injected here
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
    if (menu.label === "AI Investor") {
      const investorWidgets = Object.entries(widgetTitles)
        .filter(([id]) => AI_INVESTOR_IDS.includes(id))
        .map(([id, name]) => ({ id, name }))
        .sort((a, b) => a.name.localeCompare(b.name));

      return {
        ...menu,
        items: [
          ...investorWidgets.map(({ id, name }) => ({
            label: name,
            action: `toggle-widget-${id}`,
            checked: widgetVisibility?.[id] !== false,
          })),
        ],
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
      items: currentUser
        ? [
            { label: `Signed in as ${currentUser.username}`, disabled: true },
            { type: "divider" },
            {
              label: "Profile Settings",
              action: "profile-settings",
              disabled: false,
            },
            { label: "Sync Cloud Layout", action: "save-layout" },
            { type: "divider" },
            { label: "Logout", action: "logout" },
          ]
        : [{ label: "Sign In / Register", action: "signin" }],
    },
  ];

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
                {menu.items.map((item, index) => {
                  if (item.type === "divider") {
                    return (
                      <div key={`divider-${index}`} className="menu-divider" />
                    );
                  }

                  const isChecked = item.checked !== undefined && item.checked;
                  const hasSubmenu = item.submenu && item.submenu.length > 0;

                  return (
                    <div
                      key={item.label}
                      className={`menu-dropdown-item ${item.disabled ? "disabled" : ""} ${isChecked ? "checked" : ""} ${hasSubmenu ? "has-submenu" : ""}`}
                      onClick={(e) => {
                        if (!hasSubmenu && !item.disabled) {
                          if (item.action?.startsWith("toggle-widget-")) {
                            const widgetId = item.action.replace(
                              "toggle-widget-",
                              "",
                            );
                            if (onToggleWidget) {
                              onToggleWidget(widgetId);
                            }
                            e.stopPropagation();
                          } else {
                            handleMenuItemClick(item.action, e);
                          }
                        }
                      }}
                      tabIndex={item.disabled ? -1 : 0}
                      role="menuitem"
                      aria-disabled={item.disabled}
                      aria-checked={isChecked}
                      aria-haspopup={hasSubmenu}
                      aria-expanded={false} // Submenus expand on hover
                    >
                      {item.checked !== undefined && (
                        <span className="menu-checkmark">
                          {isChecked ? "" : ""}
                        </span>
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
                        <span className="menu-item-shortcut">
                          {item.shortcut}
                        </span>
                      )}

                      {/* Recursive Sub-menu Rendering */}
                      {hasSubmenu && (
                        <div className="menu-submenu">
                          {item.submenu.map((subItem, subIndex) => (
                            <div
                              key={subItem.label || subIndex}
                              className={`menu-dropdown-item`}
                              onClick={(e) =>
                                handleMenuItemClick(subItem.action, e)
                              }
                            >
                              <span className="menu-item-label">
                                {subItem.label}
                              </span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  );
                })}
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
          onClick={onAutoSort}
          title="Auto-sort widgets to fit as many as possible"
        >
          Auto Sort
        </button>
        <button
          className="menu-bar-button"
          onClick={onSaveLayout}
          title="Save current layout"
        >
          Save Layout
        </button>
        <button
          className="menu-bar-button"
          onClick={onLoadLayout}
          title="Load saved layout"
        >
          Load Layout
        </button>
        <button
          className="menu-bar-button"
          onClick={onResetLayout}
          title="Reset widget layout to default"
        >
          Reset Layout
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
