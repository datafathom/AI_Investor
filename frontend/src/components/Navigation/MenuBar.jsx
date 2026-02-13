/**
 * MenuBar Component
 *
 * Traditional desktop application-style menu bar with dropdown menus.
 * Fixed at the top of the application.
 */

import React, { useState, useRef, useEffect, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import useEducationStore from "../../stores/educationStore";
import { 
  Settings, Search, Brain, Cpu, Target, TrendingUp, Shield, Grid, 
  Home, ShieldCheck, Scale, Users, Briefcase, Clock, Zap, Landmark, Layout, Atom,
  Crosshair, Activity, Terminal, Database, BookOpen, ShoppingBag, Bell
} from "lucide-react";
import CommandPalette from "../Layout/CommandPalette";
import EnvVarsModal from "../admin/EnvVarsModal";
import { DEPT_REGISTRY } from "../../config/departmentRegistry";
import { getIcon } from "../../config/iconRegistry";
import "./MenuBar.css";

// Remove local ICON_MAP, now handled by iconRegistry.js

const STATIC_MENU_BEFORE = [
  {
    label: "File",
    items: [
      { label: "Market Dashboard", action: "nav-path:/special/terminal" },
      { label: "Mission Control", action: "nav-path:/special/mission-control" },
      { label: "Political Alpha", action: "nav-path:/special/political" },
      { label: "Strategy Distillery", action: "nav-path:/special/strategy" },
      { label: "Debate Chamber", action: "nav-path:/special/debate" },
      { label: "Auto-Coder", action: "nav-path:/data-scientist/autocoder" },
      { label: "VR Cockpit", action: "nav-path:/special/vr" },
      { type: "divider" },
      { label: "Options Analytics", action: "nav-path:/trader/options-analytics" },
      { label: "Backtest Portfolio", action: "nav-path:/strategist/backtest" },
      { label: "Virtual Brokerage", action: "nav-path:/strategist/brokerage" },
      { label: "Global Scanner", action: "nav-path:/trader/scanner" },
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
];

const STATIC_MENU_AFTER = [
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
      { label: "Deployment Controller", action: "nav-path:/admin/deployments" },
      { label: "Operations Dashboard", action: "nav-path:/admin/ops" },
      { label: "Workspace Manager", action: "nav-path:/admin/workspaces" },
      { label: "Environment Variables", action: "open-env-vars" },
      { label: "Feature Flags", action: "nav-path:/admin/features" },
      { label: "Forced Seller Monitor", action: "nav-path:/data-scientist/forced-sellers" },
      { label: "Whale Flow Terminal", action: "nav-path:/data-scientist/whale-flow" },
      { label: "Technical Indicators", action: "nav-path:/data-scientist/indicators" },
      { label: "Rule 144A Compliance", action: "nav-path:/legal/144a-compliance" },
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
          { label: "Terms of Service", action: "nav-path:/legal/terms" },
          { label: "Privacy Policy", action: "nav-path:/legal/privacy" },
        ],
      },
    ],
  },
];

export default function MenuBar({
  onMenuAction,
  isDarkMode,
  widgetVisibility = {},
  onToggleWidget,
  onTriggerModal,
  onResetLayout,
  toggleTheme,
  onAutoSort,
  onSaveLayout,
  onLoadLayout,
  onToggleLogCenter,
  showLogCenter,
  debugStates = {},
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
  const navigate = useNavigate();
  const [activeMenu, setActiveMenu] = useState(null);
  const menuRefs = useRef({});
  const menuBarRef = useRef(null);

  const [localUser, setLocalUser] = useState(currentUser);
  const [commandOpen, setCommandOpen] = useState(false);

  useEffect(() => {
    setLocalUser(currentUser);
  }, [currentUser]);

  useEffect(() => {
    const handleProfileUpdate = () => {
      // In a real app, this would use authService
      // setLocalUser(authService.getCurrentUser());
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

  // Build the dynamic menu items for the entire bar
  const finalMenuItems = useMemo(() => {
    // 1. Build Departments grouped by quadrant
    const allMissionRoutes = [
      { label: "🎯 Global Mission Board", action: 'nav-special-missions', highlight: true },
      { label: "🚀 Active Mission Control", action: "nav-special-mission-control", highlight: true },
      { label: "📊 Fleet Analytics", action: "nav-path:/special/fleet" },
      { label: "⚡ Scrum of Scrums", action: "nav-special-scrum" },
      { label: "🖥️ Master Terminal", action: "nav-special-terminal" }
    ];

    const allSpecialTools = [
      { label: "💼 Brokerage Account", action: "nav-path:/strategist/brokerage" },
      { label: "📱 Mobile Dashboard", action: "nav-path:/special/mobile" },
      { label: "🥽 VR Cockpit", action: "nav-path:/special/vr" },
      { label: "🧘 Zen Mode", action: "nav-path:/special/zen" },
      { label: "🏛️ Political Alpha", action: "nav-path:/special/political" },
      { label: "⚗️ Strategy Distillery", action: "nav-path:/special/strategy" },
      { label: "⚖️ Debate Chamber", action: "nav-path:/special/debate" },
      { label: "📝 Paper Trading", action: "nav-path:/special/paper" }
    ];

    const allDeptRoutes = Object.values(DEPT_REGISTRY)
      .filter(dept => {
        // Exclude Admin from general list, we'll handle it separately for visibility
        if (dept.id === 19) return false;
        
        if (dept.minRole === 'admin') {
          return currentUser?.role === 'admin' && currentUser?.username?.toLowerCase() === 'admin';
        }
        return true;
      })
      .sort((a, b) => (a.name || "").localeCompare(b.name || ""))
      .map(dept => {
        const uniqueSubModules = (dept.subModules || []).filter(mod => mod.path !== dept.route);
        return {
          label: dept.name,
          icon: getIcon(dept.icon),
          action: `nav-dept-${dept.id}`,
          submenu: [
            { label: `${dept.shortName} Dashboard`, action: `nav-dept-${dept.id}` },
            ...uniqueSubModules.map(mod => ({
              label: mod.label,
              action: `nav-path:${mod.path}`
            }))
          ]
        };
      });

    // DEBUG: Log current user to debug admin visibility
    console.log('[MenuBar] Admin Check:', { 
        user: currentUser, 
        role: currentUser?.role, 
        username: currentUser?.username,
        isAdmin: currentUser?.role === 'admin'
    });

    const isAdminUser = currentUser?.role === 'admin'; // Relaxed check: Role only
    const adminDept = DEPT_REGISTRY[19];
    const adminMenuItems = isAdminUser && adminDept ? [
      {
        label: "🛡️ Admin Controls",
        icon: ShieldCheck,
        action: `nav-dept-19`,
        highlight: true,
        submenu: [
          { label: "Admin Dashboard", action: "nav-dept-19" },
          ...(adminDept.subModules || [])
            .filter(mod => mod.path !== adminDept.route)
            .map(mod => ({
              label: mod.label,
              action: `nav-path:${mod.path}`
            }))
        ]
      },
      { type: "divider" }
    ] : [];

    const allWorkstationRoutes = Object.values(DEPT_REGISTRY)
      .filter(dept => {
        if (dept.minRole === 'admin') {
          return currentUser?.role === 'admin' && currentUser?.username?.toLowerCase() === 'admin';
        }
        return true;
      })
      .flatMap(dept => 
        (dept.subModules || []).map(mod => ({
          label: `${dept.shortName}: ${mod.label}`,
          action: `nav-path:${mod.path}`
        }))
      );

    // 3. Combine dynamic Routes, STATIC_BEFORE, and STATIC_AFTER
    const baseMenuItems = [
      ...STATIC_MENU_BEFORE,
      {
        label: "Routes",
        items: [
          {
            label: "🎯 Missions & Fleet",
            submenu: allMissionRoutes,
            highlight: true
          },
          {
            label: "🚀 Special Operations",
            submenu: allSpecialTools
          },
          {
            label: "🏢 Department Dashboards",
            submenu: allDeptRoutes,
            highlight: true
          },
          {
            label: "🛠️ Agent Workstations",
            submenu: allWorkstationRoutes
          },
          { type: "divider" },
          ...adminMenuItems,
          { label: "🖥️ Master Terminal", action: "nav-special-terminal" },
          { label: "🎯 Mission Control", action: "nav-special-mission-control" },
          { label: "📊 Fleet Analytics", action: "nav-path:/special/fleet" },
          { type: "divider" },
          { label: "🔐 Account Profile", action: "nav-path:/account" }
        ]
      },
      ...STATIC_MENU_AFTER
    ];

    // 4. Inject Dynamic Widget Toggles (preserving legacy logic)
    const menuItemsWithWidgets = baseMenuItems.map((menu) => {
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
        const otherWidgets = Object.entries(widgetTitles)
          .filter(([id]) => !AI_INVESTOR_IDS.includes(id))
          .map(([id, name]) => ({ id, name }))
          .sort((a, b) => a.name.localeCompare(b.name));

        return {
          ...menu,
          items: [
            { label: "Open All Widgets", action: "open-all-widgets" },
            { label: "Close All Widgets", action: "close-all-widgets" },
            { type: "divider" },
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
              icon: globalLock ? Shield : ShieldCheck, // Changed to Lucide components
            },
            { type: "divider" },
            { label: "Reset Layout", action: "reset-layout" },
          ],
        };
      }
      return menu;
    });

    // 5. Add Account menu at the end
    return [
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
  }, [widgetVisibility, widgetTitles, localUser, workspaces, activeWorkspace, globalLock, debugStates, toggleTheme, onLogout, onSignin, onMenuAction]);

  // State for search
  const [searchQuery, setSearchQuery] = useState("");
  const [showEnvVars, setShowEnvVars] = useState(false);

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
          className={`menu-dropdown-item ${item.disabled ? "disabled" : ""} ${isChecked ? "checked" : ""} ${hasSubmenu ? "has-submenu" : ""} ${item.highlight ? "highlight" : ""}`}
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
              <span className="menu-item-label">
                {item.icon ? (
                  <span className="menu-label-with-icon">
                    {typeof item.icon === 'string' ? item.icon : <item.icon size={14} className="menu-icon" />}
                    {item.label}
                  </span>
                ) : (
                  item.label
                )}
              </span>
              <span className="menu-submenu-arrow">▶</span>
            </div>
          ) : (
            <span className="menu-item-label">
              {item.icon ? (
                <span className="menu-label-with-icon">
                  {typeof item.icon === 'string' ? item.icon : <item.icon size={14} className="menu-icon" />}
                  {item.label}
                </span>
              ) : (
                item.label
              )}
            </span>
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

    if (action === "open-env-vars") {
      setShowEnvVars(true);
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

    // Handle Admin/Department Navigation
    if (action?.startsWith("nav-dept-")) {
      const deptId = action.replace("nav-dept-", "");
      navigate(deptId === '19' ? '/dept/admin' : `/dept/${deptId}`);
      return;
    }

    if (action?.startsWith("nav-path:")) {
      const path = action.replace("nav-path:", "");
      navigate(path);
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
      const currentIndex = finalMenuItems.findIndex((m) => m.label === menuLabel);
      const nextIndex = (currentIndex + 1) % finalMenuItems.length;
      setActiveMenu(finalMenuItems[nextIndex].label);
    } else if (event.key === "ArrowLeft" && activeMenu === menuLabel) {
      event.preventDefault();
      const currentIndex = finalMenuItems.findIndex((m) => m.label === menuLabel);
      const prevIndex =
        (currentIndex - 1 + finalMenuItems.length) % finalMenuItems.length;
      setActiveMenu(finalMenuItems[prevIndex].label);
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
        <CommandPalette open={commandOpen} onOpenChange={setCommandOpen} />
        <EnvVarsModal open={showEnvVars} onOpenChange={setShowEnvVars} />
      </div>
    </div>
  );
}
