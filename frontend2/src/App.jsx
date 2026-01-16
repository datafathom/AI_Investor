/**
 * Main App Component
 * 
 * This is the root React component for the application.
 * It demonstrates:
 * - Color palette integration
 * - API calls to the backend
 * - Optional Socket.io connection
 * - Basic component structure
 * 
 * Replace this with your own application logic.
 */

import React, { useEffect, useMemo, useState, useRef, useCallback, Suspense, lazy } from 'react';
import GridLayout from 'react-grid-layout';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';
import { useColorPalette } from './hooks/useColorPalette';
import { useWidgetLayout } from './hooks/useWidgetLayout';
import MenuBar from './components/MenuBar';
import WindowHeader from './components/WindowHeader';
import ViewSource from './components/ViewSource';
import LogCenter from './components/LogCenter';
import VirtualizedChatMessages from './components/VirtualizedChatMessages';
import { SimpleBarChart, SimplePieChart, SimpleLineChart, SimpleAreaChart } from './components/Charts/SimpleCharts';
// Lazy load heavy chart components
const SimpleScatterPlot = lazy(() => import('./components/Charts/SimpleCharts').then(module => ({ default: module.SimpleScatterPlot })));
const MovingAverageChart = lazy(() => import('./components/Charts/SimpleCharts').then(module => ({ default: module.MovingAverageChart })));
const AudioWaveform = lazy(() => import('./components/Charts/SimpleCharts').then(module => ({ default: module.AudioWaveform })));

// AI Investor Widgets
import MonitorWidget from './components/AI_Investor/Views/MonitorWidget';
import CommandWidget from './components/AI_Investor/Views/CommandWidget';
import ResearchWidget from './components/AI_Investor/Views/ResearchWidget';
import PortfolioWidget from './components/AI_Investor/Views/PortfolioWidget';

import { COMPONENT_SOURCE_MAP } from './utils/componentSourceMap';
import io from 'socket.io-client';
import { authService } from './utils/authService';
import LoginModal from './components/LoginModal';
import AuthGuard from './components/AuthGuard';
import DockerWidget from './components/DockerWidget';
import WindowManagerWidget from './components/WindowManager/WindowManagerWidget';
import './App.css';

// Default layout configuration
// Using 48 columns for fine-grained resizing (4x the original 12 columns)
// All widths and positions are scaled by 4 to maintain visual appearance
const DEFAULT_LAYOUT = [
  { i: 'monitor-view', x: 0, y: 0, w: 24, h: 20, minW: 16, minH: 10, maxW: 48 }, // Main Monitor
  { i: 'command-view', x: 24, y: 0, w: 24, h: 10, minW: 16, minH: 8, maxW: 48 }, // Command Center
  { i: 'portfolio-view', x: 24, y: 10, w: 24, h: 10, minW: 16, minH: 8, maxW: 48 }, // Portfolio
  { i: 'research-view', x: 0, y: 20, w: 24, h: 12, minW: 16, minH: 8, maxW: 48 }, // Research

  { i: 'socketio', x: 0, y: 32, w: 24, h: 7, minW: 16, minH: 4, maxW: 48 },
];

const CHECKLIST_STEPS = [
  {
    title: 'Craft the UI System',
    description: 'Replace App.jsx with product UI + routes.',
    command: 'code ./src/App.jsx',
  },
  {
    title: 'Wire Backend APIs',
    description: 'Add new endpoints to server.js + proxy rules.',
    command: 'npm run dev',
  },
  {
    title: 'Enable Realtime',
    description: 'Uncomment the Socket.io block and emit events.',
    command: 'npm install socket.io socket.io-client',
  },
  {
    title: 'Deploy',
    description: 'Build once, ship anywhere. Deploy Node + static bundle.',
    command: 'npm run build',
  },
];

const TERMINAL_SNIPPETS = [
  { label: 'Install dependencies', command: 'npm install' },
  { label: 'Start both servers', command: 'npm run dev' },
  { label: 'Run lint & tests', command: 'npm run lint && npm test' },
];

const INITIAL_MEMORY_POINTS = [62, 65, 64, 70, 66, 72, 68, 73, 69];

const COLOR_TOKENS = [
  { label: 'Burgundy / Primary', path: ['burgundy', 'primary'] },
  { label: 'Burgundy / Accent', path: ['burgundy', 'accent'] },
  { label: 'Burgundy / Dark', path: ['burgundy', 'dark'] },
  { label: 'Cream / Primary', path: ['cream', 'primary'] },
  { label: 'Cream / Medium', path: ['cream', 'medium'] },
  { label: 'Text / On Burgundy', path: ['text', 'on_burgundy'] },
];

const SURFACE_SCALE = [
  { label: 'Surface 50', token: '--surface-50' },
  { label: 'Surface 100', token: '--surface-100' },
  { label: 'Surface 200', token: '--surface-200' },
];

// Socket.io Configuration
const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '3002';
const SOCKET_SERVER_URL = `http://localhost:${BACKEND_PORT}`;

// Room configuration
const ROOM_LIST = [
  { id: 'general', name: '#general', secure: false },
  { id: 'tech', name: '#tech', secure: false },
  { id: 'secure', name: '#secure 🔒', secure: true },
  { id: 'top-secret', name: '#top-secret 🔐', secure: true }
];

const formatJson = (data) => {
  const json = JSON.stringify(data, null, 2)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');

  return json.replace(
    /("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+\.\d+|-?\d+)/g,
    (match) => {
      let cls = 'json-number';
      if (/^"/.test(match)) {
        cls = /:$/.test(match) ? 'json-key' : 'json-string';
      } else if (/true|false/.test(match)) {
        cls = 'json-boolean';
      } else if (/null/.test(match)) {
        cls = 'json-null';
      }
      return `<span class="${cls}">${match}</span>`;
    }
  );
};

const MemoryChart = ({ data }) => {
  if (data.length < 2) return null;
  const points = data
    .map((value, index) => {
      const x = (index / (data.length - 1)) * 100;
      const normalized = Math.max(0, Math.min(1, (value - 48) / 42));
      const y = 90 - normalized * 70;
      return `${x},${y}`;
    })
    .join(' ');

  const fillPoints = `0,100 ${points} 100,100`;

  return (
    <svg className="telemetry-chart" viewBox="0 0 100 100" preserveAspectRatio="none" role="img" aria-label="Server memory usage line chart">
      <defs>
        <linearGradient id="chartStroke" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="rgba(255,255,255,0.8)" />
          <stop offset="100%" stopColor="rgba(255,255,255,0.4)" />
        </linearGradient>
        <linearGradient id="chartFill" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="rgba(255,255,255,0.25)" />
          <stop offset="100%" stopColor="rgba(255,255,255,0.02)" />
        </linearGradient>
      </defs>
      <polygon points={fillPoints} fill="url(#chartFill)" />
      <polyline points={points} fill="none" stroke="url(#chartStroke)" strokeWidth="2.5" strokeLinecap="round" />
    </svg>
  );
};

const WIDGET_TITLES = {
  'monitor-view': 'Market Monitor',
  'command-view': 'Command Center',
  'research-view': 'Data Research',
  'portfolio-view': 'Live Portfolio',
  'window-manager': 'Window Manager',
  api: 'API Integration',
  palette: 'Color System',
  docker: 'Docker Containers',
  checklist: 'Launch Checklist',
  telemetry: 'Server Telemetry',
  ux: 'Experience Controls',
  socketio: 'Socket.io Realtime',
  'ping-api': 'Ping API',
  'server-status': 'Server Status',
  'bar-chart': 'Bar Chart',
  'pie-chart': 'Pie Chart',
  'line-chart': 'Line Chart',
  'area-chart': 'Area Chart',
  'scatter-plot': 'Scatter Plot',
  'moving-average': 'Moving Average',
  'audio-waveform': 'Audio Waveform',
};

function App() {
  const { palette } = useColorPalette();
  const { layout, setLayout, resetLayout } = useWidgetLayout();
  const [serverStatus, setServerStatus] = useState({ label: 'Checking…', tone: 'loading' });
  const [apiData, setApiData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isDarkMode, setIsDarkMode] = useState(true); // Dark theme by default
  const [showModal, setShowModal] = useState(false);
  const [toast, setToast] = useState(null);
  const [copiedCommand, setCopiedCommand] = useState(null);
  const [memorySeries, setMemorySeries] = useState(INITIAL_MEMORY_POINTS);
  const [gridWidth, setGridWidth] = useState(1200);
  const [viewSource, setViewSource] = useState({ widgetId: null, source: null });
  const [debugStates, setDebugStates] = useState({ forceLoading: false, forceError: false });
  const [showLogCenter, setShowLogCenter] = useState(false);
  const [logHistory, setLogHistory] = useState([]);
  const [minimizedWidgets, setMinimizedWidgets] = useState([]);
  const [globalLock, setGlobalLock] = useState(false);
  const [currentUser, setCurrentUser] = useState(authService.getCurrentUser());
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(!authService.isAuthenticated());

  // Widget visibility and window state
  // Initialize all widgets as closed (false) by default
  const [widgetVisibility, setWidgetVisibility] = useState(() => {
    const saved = localStorage.getItem('react_node_template_widget_visibility');
    if (saved) {
      return JSON.parse(saved);
    }
    // Default: all widgets closed
    const defaultVisibility = {};
    Object.keys(WIDGET_TITLES).forEach(widgetId => {
      defaultVisibility[widgetId] = false;
    });
    return defaultVisibility;
  });

  const [widgetStates, setWidgetStates] = useState(() => {
    const saved = localStorage.getItem('react_node_template_widget_states');
    const defaultStates = {
      api: { minimized: false, maximized: false, locked: false },
      palette: { minimized: false, maximized: false, locked: false },
      checklist: { minimized: false, maximized: false, locked: false },
      telemetry: { minimized: false, maximized: false, locked: false },
      ux: { minimized: false, maximized: false, locked: false },
      socketio: { minimized: false, maximized: false, locked: false },
      'ping-api': { minimized: false, maximized: false, locked: false },
      'server-status': { minimized: false, maximized: false, locked: false },
      'bar-chart': { minimized: false, maximized: false, locked: false },
      'pie-chart': { minimized: false, maximized: false, locked: false },
      'line-chart': { minimized: false, maximized: false, locked: false },
      'area-chart': { minimized: false, maximized: false, locked: false },
      'scatter-plot': { minimized: false, maximized: false, locked: false },
      'moving-average': { minimized: false, maximized: false, locked: false },
      'audio-waveform': { minimized: false, maximized: false, locked: false },
      'simple-planet-menu': { minimized: false, maximized: false, locked: false },
      'draggable-planet-menu': { minimized: false, maximized: false, locked: false },
      'custom-orbit-menu': { minimized: false, maximized: false, locked: false },
      'nested-planet-menu': { minimized: false, maximized: false, locked: false },
    };
    if (saved) {
      const parsed = JSON.parse(saved);
      // Ensure all required properties exist
      Object.keys(defaultStates).forEach(key => {
        if (!parsed[key]) parsed[key] = defaultStates[key];
      });
      return parsed;
    }
    return defaultStates;
  });

  // Socket.io state - using direct state updates for chat messages (like socketIO_demo)
  const [socketConnected, setSocketConnected] = useState(false);
  const [socketId, setSocketId] = useState(null);
  const [clientCount, setClientCount] = useState(0);
  const [socketMessages, setSocketMessages] = useState([]); // Direct state for chat messages
  const [currentRoom, setCurrentRoom] = useState('general');
  const [typingStatus, setTypingStatus] = useState('');
  const [inputMessage, setInputMessage] = useState('');
  const socketRef = useRef(null);
  const messagesEndRef = useRef(null);
  const typingTimeoutRef = useRef(null);

  // Throttle layout changes to prevent excessive re-renders during drag/resize
  const layoutChangeTimerRef = useRef(null);
  const pendingLayoutRef = useRef(null);

  const throttledSetLayout = useCallback((newLayout) => {
    pendingLayoutRef.current = newLayout;

    if (!layoutChangeTimerRef.current) {
      layoutChangeTimerRef.current = setTimeout(() => {
        if (pendingLayoutRef.current) {
          setLayout(pendingLayoutRef.current);
          pendingLayoutRef.current = null;
        }
        layoutChangeTimerRef.current = null;
      }, 50); // Throttle to ~20fps during drag/resize
    }
  }, [setLayout]);

  const handleLoginSuccess = () => {
    const user = authService.getCurrentUser();
    setCurrentUser(user);
    setIsAuthModalOpen(false); // Close modal on successful login
    if (user) {
      setToast({ type: 'success', message: `Welcome back, ${user.username}!` });
      // Try to load user's layout from server
      handleLoadLayoutFromServer();
    }
  };

  const handleLogout = () => {
    authService.logout();
    setCurrentUser(null);
    setIsAuthModalOpen(true); // Show login modal after logout
    setToast({ type: 'info', message: 'Logged out successfully' });
  };

  const handleLoadLayoutFromServer = async () => {
    if (!authService.isAuthenticated()) return;
    try {
      const response = await authService.authenticatedFetch('/api/layout', {
        headers: { 'Authorization': `Bearer ${authService.getToken()}` }
      });
      if (response.ok) {
        const remoteLayout = await response.json();
        if (remoteLayout && remoteLayout.layout) {
          setLayout(remoteLayout.layout);
          setWidgetVisibility(remoteLayout.widgetVisibility || {});
          setWidgetStates(remoteLayout.widgetStates || {});
          setToast({ type: 'success', message: 'Layout synchronized with server' });
        }
      }
    } catch (error) {
      console.error('Failed to load layout from server:', error);
    }
  };

  useEffect(() => {
    if (currentUser) {
      handleLoadLayoutFromServer();
    }
  }, []);

  useEffect(() => {
    document.body.classList.toggle('theme-dark', isDarkMode);
    document.body.classList.toggle('theme-light', !isDarkMode);
  }, [isDarkMode]);

  // Save widget visibility to localStorage
  useEffect(() => {
    localStorage.setItem('react_node_template_widget_visibility', JSON.stringify(widgetVisibility));
  }, [widgetVisibility]);

  // Save widget states to localStorage
  useEffect(() => {
    localStorage.setItem('react_node_template_widget_states', JSON.stringify(widgetStates));
  }, [widgetStates]);

  // Sync layout with minimized widgets on initial mount (for widgets saved as minimized)
  useEffect(() => {
    // Only run once on mount to sync layout with saved minimized state
    const minimizedWidgets = Object.entries(widgetStates)
      .filter(([_, state]) => state?.minimized === true)
      .map(([id, _]) => id);

    if (minimizedWidgets.length > 0) {
      setLayout(prev => {
        const updated = prev.map(item => {
          if (minimizedWidgets.includes(item.i) && item.h !== 1) {
            // Widget is minimized but layout height is not 1, fix it
            return { ...item, h: 1, minH: 1 };
          }
          return item;
        });
        // Only return new array if something changed to avoid unnecessary re-renders
        return updated.some((item, idx) => item.h !== prev[idx]?.h) ? updated : prev;
      });
    }
  }, []); // Empty deps - only run once on mount


  const handleToggleWidget = (widgetId) => {
    const isCurrentlyVisible = widgetVisibility[widgetId] !== false;

    if (isCurrentlyVisible) {
      // Widget is being closed - save its current layout
      const currentLayoutItem = layout.find(item => item.i === widgetId);
      if (currentLayoutItem) {
        setWidgetStates(prev => ({
          ...prev,
          [widgetId]: {
            ...prev[widgetId],
            lastLayout: {
              x: currentLayoutItem.x,
              y: currentLayoutItem.y,
              w: currentLayoutItem.w,
              h: currentLayoutItem.h,
            },
          },
        }));
      }
      // Hide the widget
      setWidgetVisibility(prev => ({
        ...prev,
        [widgetId]: false,
      }));
    } else {
      // Widget is being reopened - restore its previous layout if it exists
      const lastLayout = widgetStates[widgetId]?.lastLayout;
      const defaultLayout = DEFAULT_LAYOUT.find(item => item.i === widgetId);

      if (lastLayout && defaultLayout) {
        // Restore with saved dimensions
        const restoredLayout = {
          i: widgetId,
          x: lastLayout.x,
          y: lastLayout.y,
          w: lastLayout.w,
          h: lastLayout.h,
          minW: defaultLayout.minW,
          minH: defaultLayout.minH,
          maxW: defaultLayout.maxW || 48,
        };

        // Add the restored widget to the layout
        setLayout(prev => {
          // Remove any existing entry for this widget (shouldn't exist, but just in case)
          const filtered = prev.filter(item => item.i !== widgetId);
          // Add the restored layout
          return [...filtered, restoredLayout];
        });
      } else if (defaultLayout) {
        // No saved layout, use default
        setLayout(prev => {
          const filtered = prev.filter(item => item.i !== widgetId);
          return [...filtered, { ...defaultLayout }];
        });
      }

      // Show the widget
      setWidgetVisibility(prev => ({
        ...prev,
        [widgetId]: true,
      }));
    }
  };

  const handleWidgetMinimize = (widgetId) => {
    const isCurrentlyMinimized = widgetStates[widgetId]?.minimized;
    const currentLayoutItem = layout.find(item => item.i === widgetId);

    if (!isCurrentlyMinimized) {
      // Minimizing: save current height and set to 1 row (just header)
      if (currentLayoutItem) {
        setWidgetStates(prev => ({
          ...prev,
          [widgetId]: {
            ...prev[widgetId],
            minimized: true,
            maximized: false,
            savedHeight: currentLayoutItem.h, // Save original height
          },
        }));

        // Update layout to minimal height (1 row for header)
        setLayout(prev => prev.map(item =>
          item.i === widgetId
            ? { ...item, h: 1, minH: 1 } // Set to 1 row, update minH
            : item
        ));
      }
    } else {
      // Restoring: restore saved height
      const savedHeight = widgetStates[widgetId]?.savedHeight;
      const defaultLayout = DEFAULT_LAYOUT.find(item => item.i === widgetId);
      const heightToRestore = savedHeight || defaultLayout?.h || 3;

      setWidgetStates(prev => ({
        ...prev,
        [widgetId]: {
          ...prev[widgetId],
          minimized: false,
          maximized: false,
        },
      }));

      // Restore layout height
      setLayout(prev => prev.map(item =>
        item.i === widgetId
          ? {
            ...item,
            h: heightToRestore,
            minH: defaultLayout?.minH || 2, // Restore original minH
          }
          : item
      ));
    }
  };

  const handleWidgetMaximize = (widgetId) => {
    const isCurrentlyMaximized = widgetStates[widgetId]?.maximized;
    const currentLayoutItem = layout.find(item => item.i === widgetId);

    if (!isCurrentlyMaximized) {
      // Maximizing: first move to top-left, then calculate content height and auto-resize
      // Use setTimeout to ensure DOM is ready
      setTimeout(() => {
        // Find widget by data attribute
        const widgetElement = document.querySelector(`[data-widget-id="${widgetId}"]`);

        if (widgetElement) {
          const contentSection = widgetElement.querySelector('section');
          if (contentSection) {
            // Temporarily remove height constraints to measure natural content height
            const originalOverflow = contentSection.style.overflow;
            const originalHeight = contentSection.style.height;
            contentSection.style.overflow = 'visible';
            contentSection.style.height = 'auto';

            const contentHeight = contentSection.scrollHeight;
            const headerHeight = 28; // Header height in pixels
            const totalHeight = contentHeight + headerHeight;
            const rowHeight = 60; // Grid row height
            const requiredRows = Math.ceil(totalHeight / rowHeight);

            // Restore original styles
            contentSection.style.overflow = originalOverflow;
            contentSection.style.height = originalHeight;

            // Save current dimensions before maximizing
            if (currentLayoutItem) {
              setWidgetStates(prev => ({
                ...prev,
                [widgetId]: {
                  ...prev[widgetId],
                  maximized: true,
                  minimized: false,
                  savedBeforeMaximize: {
                    x: currentLayoutItem.x,
                    y: currentLayoutItem.y,
                    w: currentLayoutItem.w,
                    h: currentLayoutItem.h,
                  },
                },
              }));

              // First move to top-left (x:0, y:0), then expand to fit content
              const maxWidth = currentLayoutItem.maxW || 48;
              setLayout(prev => prev.map(item =>
                item.i === widgetId
                  ? {
                    ...item,
                    x: 0,  // Move to top-left
                    y: 0,  // Move to top-left
                    h: Math.max(requiredRows, item.minH || 2),
                    w: Math.min(Math.max(item.w, 6), maxWidth), // Expand width but respect max
                  }
                  : item
              ));
            }
          }
        }
      }, 0);
    } else {
      // Restoring: restore saved dimensions
      const savedBeforeMaximize = widgetStates[widgetId]?.savedBeforeMaximize;
      const defaultLayout = DEFAULT_LAYOUT.find(item => item.i === widgetId);

      if (savedBeforeMaximize) {
        setWidgetStates(prev => ({
          ...prev,
          [widgetId]: {
            ...prev[widgetId],
            maximized: false,
            minimized: false,
          },
        }));

        // Restore layout dimensions
        setLayout(prev => prev.map(item =>
          item.i === widgetId
            ? {
              ...item,
              x: savedBeforeMaximize.x,
              y: savedBeforeMaximize.y,
              w: savedBeforeMaximize.w,
              h: savedBeforeMaximize.h,
            }
            : item
        ));
      } else if (defaultLayout) {
        // Fallback to default if no saved state
        setWidgetStates(prev => ({
          ...prev,
          [widgetId]: {
            ...prev[widgetId],
            maximized: false,
            minimized: false,
          },
        }));

        setLayout(prev => prev.map(item =>
          item.i === widgetId
            ? { ...defaultLayout }
            : item
        ));
      }
    }
  };

  const handleRestoreFromDock = (widgetId) => {
    // Restore widget from minimized state
    setWidgetStates(prev => ({
      ...prev,
      [widgetId]: {
        ...prev[widgetId],
        minimized: false,
      },
    }));
    setMinimizedWidgets(prev => prev.filter(id => id !== widgetId));
    setWidgetVisibility(prev => ({
      ...prev,
      [widgetId]: true,
    }));
  };

  const handleWidgetClose = (widgetId) => {
    // Save current layout before closing
    const currentLayoutItem = layout.find(item => item.i === widgetId);
    if (currentLayoutItem) {
      setWidgetStates(prev => ({
        ...prev,
        [widgetId]: {
          ...prev[widgetId],
          minimized: false,
          maximized: false,
          lastLayout: {
            x: currentLayoutItem.x,
            y: currentLayoutItem.y,
            w: currentLayoutItem.w,
            h: currentLayoutItem.h,
          },
        },
      }));
    }

    setWidgetVisibility(prev => ({
      ...prev,
      [widgetId]: false,
    }));
  };

  const handleWidgetLock = (widgetId) => {
    setWidgetStates(prev => ({
      ...prev,
      [widgetId]: { ...prev[widgetId], locked: !prev[widgetId]?.locked },
    }));
  };

  // Minimum Full View resize - resize widget to fit content exactly (no scrollbars)
  const handleMinimumFullView = (widgetId) => {
    const currentLayoutItem = layout.find(item => item.i === widgetId);
    if (!currentLayoutItem) return;

    setTimeout(() => {
      const widgetElement = document.querySelector(`[data-widget-id="${widgetId}"]`);
      if (!widgetElement) return;

      const contentSection = widgetElement.querySelector('section');
      if (!contentSection) return;

      // Temporarily remove constraints to measure natural content size
      const originalOverflow = contentSection.style.overflow;
      const originalHeight = contentSection.style.height;
      const originalWidth = contentSection.style.width;
      const originalMaxHeight = contentSection.style.maxHeight;
      const originalMaxWidth = contentSection.style.maxWidth;

      contentSection.style.overflow = 'visible';
      contentSection.style.height = 'auto';
      contentSection.style.width = 'auto';
      contentSection.style.maxHeight = 'none';
      contentSection.style.maxWidth = 'none';

      // Get computed styles to account for padding and borders
      const computedStyle = window.getComputedStyle(contentSection);
      const paddingTop = parseFloat(computedStyle.paddingTop) || 0;
      const paddingBottom = parseFloat(computedStyle.paddingBottom) || 0;
      const paddingLeft = parseFloat(computedStyle.paddingLeft) || 0;
      const paddingRight = parseFloat(computedStyle.paddingRight) || 0;
      const borderTop = parseFloat(computedStyle.borderTopWidth) || 0;
      const borderBottom = parseFloat(computedStyle.borderBottomWidth) || 0;
      const borderLeft = parseFloat(computedStyle.borderLeftWidth) || 0;
      const borderRight = parseFloat(computedStyle.borderRightWidth) || 0;

      // Calculate required dimensions
      const scrollWidth = contentSection.scrollWidth;
      const scrollHeight = contentSection.scrollHeight;

      // Account for padding and borders
      const requiredWidth = scrollWidth + paddingLeft + paddingRight + borderLeft + borderRight;
      const requiredHeight = scrollHeight + paddingTop + paddingBottom + borderTop + borderBottom;

      // Restore original styles
      contentSection.style.overflow = originalOverflow;
      contentSection.style.height = originalHeight;
      contentSection.style.width = originalWidth;
      contentSection.style.maxHeight = originalMaxHeight;
      contentSection.style.maxWidth = originalMaxWidth;

      // Convert to grid units
      const rowHeight = 60; // Grid row height
      const headerHeight = 28; // Header height
      const totalHeight = requiredHeight + headerHeight;
      const requiredRows = Math.ceil(totalHeight / rowHeight);

      // Calculate width in grid units (12 columns total)
      // Get current grid container width from state
      const currentGridWidth = gridWidth || 1200;
      const colWidth = currentGridWidth / 12;
      const requiredCols = Math.ceil(requiredWidth / colWidth);

      // Update layout with minimum required dimensions
      const maxWidth = currentLayoutItem.maxW || 48;
      const minWidth = currentLayoutItem.minW || 2;

      setLayout(prev => prev.map(item =>
        item.i === widgetId
          ? {
            ...item,
            w: Math.max(minWidth, Math.min(requiredCols, maxWidth)),
            h: Math.max(item.minH || 2, requiredRows),
          }
          : item
      ));
    }, 0);
  };

  // Auto-sort widgets to fit as many as possible high up
  const handleAutoSort = () => {
    const visibleLayout = layout.filter(item => widgetVisibility[item.i] !== false);
    const sortedLayout = [];
    const occupied = new Set();

    // Sort widgets by height (smaller first) then by width to optimize packing
    const sortedWidgets = [...visibleLayout].sort((a, b) => {
      if (a.h !== b.h) return a.h - b.h;
      return a.w - b.w;
    });

    // Try to place each widget as high and left as possible
    sortedWidgets.forEach(widget => {
      let placed = false;

      // Try positions from top-left, moving right then down
      for (let y = 0; y < 100 && !placed; y++) {
        for (let x = 0; x <= 12 - widget.w && !placed; x++) {
          // Check if this position is available
          let canPlace = true;
          for (let checkY = y; checkY < y + widget.h && canPlace; checkY++) {
            for (let checkX = x; checkX < x + widget.w && canPlace; checkX++) {
              const key = `${checkX},${checkY}`;
              if (occupied.has(key)) {
                canPlace = false;
              }
            }
          }

          if (canPlace) {
            // Mark cells as occupied
            for (let markY = y; markY < y + widget.h; markY++) {
              for (let markX = x; markX < x + widget.w; markX++) {
                occupied.add(`${markX},${markY}`);
              }
            }

            sortedLayout.push({
              ...widget,
              x,
              y,
            });
            placed = true;
          }
        }
      }
    });

    setLayout(sortedLayout);
  };

  // Handle window resize for responsive grid
  useEffect(() => {
    const updateGridWidth = () => {
      const container = document.querySelector('.widget-grid-container');
      if (container) {
        // Use full container width minus padding (1rem left + 1rem right = 32px total)
        setGridWidth(container.offsetWidth - 32);
      } else {
        // Fallback: use viewport width minus padding
        setGridWidth(window.innerWidth - 32);
      }
    };

    updateGridWidth();
    window.addEventListener('resize', updateGridWidth);
    return () => window.removeEventListener('resize', updateGridWidth);
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setMemorySeries((prev) => {
        const nextPoint = Math.max(48, Math.min(92, prev[prev.length - 1] + (Math.random() * 8 - 4)));
        return [...prev.slice(1), Number(nextPoint.toFixed(1))];
      });
    }, 3500);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (!toast) return;
    const timer = setTimeout(() => setToast(null), 4000);
    // Add to log history
    setLogHistory(prev => [...prev, {
      timestamp: new Date().toISOString(),
      type: toast.type,
      message: toast.message
    }]);
    return () => clearTimeout(timer);
  }, [toast]);

  // Handle View Source
  const handleViewSource = (widgetId) => {
    const source = COMPONENT_SOURCE_MAP[widgetId];
    if (source) {
      setViewSource({ widgetId, source });
    }
  };

  // Handle layout persistence
  const handleSaveLayout = async () => {
    const layoutData = {
      layout,
      widgetVisibility,
      widgetStates,
      timestamp: new Date().toISOString()
    };

    // Save to localStorage regardless
    localStorage.setItem('react_node_template_saved_layout', JSON.stringify(layoutData));

    // Save to server if authenticated
    if (authService.isAuthenticated()) {
      try {
        const response = await authService.authenticatedFetch('/api/layout', {
          method: 'POST',
          body: JSON.stringify({ layoutData })
        });
        if (!response.ok) throw new Error('Server save failed');
        setToast({ type: 'success', message: 'Layout saved locally and to cloud' });
      } catch (error) {
        console.error('Save to server failed:', error);
        setToast({ type: 'warning', message: 'Saved locally (Cloud sync failed)' });
      }
    } else {
      setToast({ type: 'success', message: 'Layout saved locally' });
    }
  };

  const handleLoadLayout = () => {
    if (authService.isAuthenticated()) {
      handleLoadLayoutFromServer();
    } else {
      const saved = localStorage.getItem('react_node_template_saved_layout');
      if (saved) {
        try {
          const layoutData = JSON.parse(saved);
          applyLoadedLayout(layoutData);
          setToast({ type: 'success', message: 'Layout loaded from local storage' });
        } catch (e) {
          console.error('Failed to parse local layout:', e);
          setToast({ type: 'error', message: 'Failed to load local layout' });
        }
      }
    }
  };

  const applyLoadedLayout = (layoutData) => {
    // Scale layout if it was saved with old 12-column grid
    const scaledLayout = layoutData.layout?.map(item => {
      // Check if layout uses old 12-column system (maxW <= 12)
      const needsScaling = item.maxW && item.maxW <= 12;
      if (needsScaling) {
        return {
          ...item,
          x: item.x * 4,
          w: item.w * 4,
          minW: item.minW ? item.minW * 4 : 16,
          maxW: item.maxW ? item.maxW * 4 : 48,
        };
      }
      return item;
    }) || DEFAULT_LAYOUT;

    setLayout(scaledLayout);
    setWidgetVisibility(layoutData.widgetVisibility || widgetVisibility);
    setWidgetStates(layoutData.widgetStates || widgetStates);
    setToast({ type: 'success', message: 'Layout loaded successfully' });
  };

  const handleClearSavedLayout = () => {
    localStorage.removeItem('react_node_template_saved_layout');
    setToast({ type: 'success', message: 'Saved layout cleared' });
  };

  // Load saved layout on mount
  useEffect(() => {
    const saved = localStorage.getItem('react_node_template_saved_layout');
    if (saved) {
      try {
        const layoutData = JSON.parse(saved);
        if (layoutData.layout) {
          // Scale layout if it was saved with old 12-column grid
          const scaledLayout = layoutData.layout.map(item => {
            const needsScaling = item.maxW && item.maxW <= 12;
            if (needsScaling) {
              return {
                ...item,
                x: item.x * 4,
                w: item.w * 4,
                minW: item.minW ? item.minW * 4 : 16,
                maxW: item.maxW ? item.maxW * 4 : 48,
              };
            }
            return item;
          });
          setLayout(scaledLayout);
        }
        if (layoutData.widgetVisibility) {
          setWidgetVisibility(layoutData.widgetVisibility);
        }
        if (layoutData.widgetStates) {
          setWidgetStates(layoutData.widgetStates);
        }
      } catch (err) {
        console.error('Failed to load saved layout:', err);
      }
    }
  }, []); // Only run on mount

  const fetchApiData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/example');
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const data = await response.json();
      setApiData(data);
      setToast({ type: 'success', message: 'API data refreshed' });
    } catch (err) {
      setError(err.message);
      setToast({ type: 'error', message: `API error: ${err.message}` });
      console.error('API Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const checkServerHealth = async () => {
    try {
      const response = await fetch('/api/health');
      if (!response.ok) throw new Error('Status not OK');
      const data = await response.json();
      if (data.status === 'ok') {
        setServerStatus({ label: 'Connected', tone: 'ok' });
      } else {
        setServerStatus({ label: 'Degraded', tone: 'warning' });
      }
    } catch (err) {
      setServerStatus({ label: 'Offline', tone: 'error' });
    }
  };

  useEffect(() => {
    checkServerHealth();
    const interval = setInterval(checkServerHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  // Socket.io connection setup
  useEffect(() => {
    // Only initialize socket once
    if (socketRef.current) {
      return;
    }

    socketRef.current = io(SOCKET_SERVER_URL, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5
    });
    const socket = socketRef.current;

    // Connection events
    socket.on('connect', () => {
      console.log(`[Socket.io] Connected with ID: ${socket.id}`);
      setSocketConnected(true);
      setSocketId(socket.id);
      // Join default room on connect
      socket.emit('joinRoom', { room: 'general', password: null });
    });

    socket.on('disconnect', () => {
      console.log('[Socket.io] Disconnected');
      setSocketConnected(false);
      setSocketId(null);
    });

    socket.on('connect_error', (error) => {
      console.error('[Socket.io] Connection error:', error);
      setSocketConnected(false);
    });

    // Socket.io event listeners
    socket.on('clientCount', (count) => {
      setClientCount(count);
    });

    socket.on('chatThread', (message) => {
      // Direct state update for chat messages (like socketIO_demo)
      // This ensures messages appear immediately without buffering delays
      try {
        console.log('[Socket.io] Received message:', JSON.stringify(message, null, 2));
        setSocketMessages((prev) => {
          const updated = [...prev, message];
          console.log('[Socket.io] Updated messages array, new count:', updated.length);
          return updated;
        });
      } catch (error) {
        console.error('[Socket.io] Error adding message:', error);
      }
    });

    socket.on('userTyping', (msg) => {
      setTypingStatus(msg);
    });

    return () => {
      if (socket) {
        socket.offAny();
        socket.disconnect();
        socketRef.current = null;
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Remove addSocketMessage from deps to prevent re-initialization

  // Cleanup layout change timer on unmount
  useEffect(() => {
    return () => {
      if (layoutChangeTimerRef.current) {
        clearTimeout(layoutChangeTimerRef.current);
      }
    };
  }, []);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    console.log('[Socket.io] Messages updated, count:', socketMessages.length);
    if (socketMessages.length > 0) {
      console.log('[Socket.io] Latest message:', socketMessages[socketMessages.length - 1]);
    }
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [socketMessages]);

  const handleCopy = async (command, id) => {
    if (!navigator?.clipboard) {
      setToast({ type: 'error', message: 'Clipboard API unavailable' });
      return;
    }
    try {
      await navigator.clipboard.writeText(command);
      setCopiedCommand(id);
      setTimeout(() => setCopiedCommand(null), 1800);
    } catch (err) {
      setToast({ type: 'error', message: 'Clipboard unavailable' });
    }
  };

  const syntaxMarkup = apiData ? formatJson(apiData) : '';

  const memoryStats = useMemo(() => {
    const current = memorySeries[memorySeries.length - 1];
    const average = memorySeries.reduce((sum, value) => sum + value, 0) / memorySeries.length;
    return { current, average: Number(average.toFixed(1)) };
  }, [memorySeries]);

  const toggleTheme = () => setIsDarkMode((prev) => !prev);

  const triggerModal = () => setShowModal(true);
  const closeModal = () => setShowModal(false);


  // Socket.io handlers
  const handleJoinRoom = (targetRoomObj) => {
    const targetRoom = targetRoomObj.id;
    if (targetRoom === currentRoom) return;

    let password = null;

    if (targetRoomObj.secure) {
      password = prompt(`Enter password for ${targetRoomObj.name}:`);
      if (password === null) return; // User clicked Cancel
    }

    const socket = socketRef.current;
    if (!socket || !socket.connected) {
      setToast({ type: 'error', message: 'Socket.io not connected' });
      return;
    }

    socket.emit('joinRoom', { room: targetRoom, password: password }, (response) => {
      if (response.status === 'ok') {
        setCurrentRoom(targetRoom);
        setSocketMessages([]); // Clear chat for new room
        setToast({ type: 'success', message: `Joined ${targetRoomObj.name}` });
      } else {
        setToast({ type: 'error', message: response.message || 'Failed to join room' });
      }
    });
  };

  const handleInputChange = (e) => {
    setInputMessage(e.target.value);
    const socket = socketRef.current;

    if (socket && socket.connected) {
      socket.emit('typing', currentRoom);
      if (typingTimeoutRef.current) clearTimeout(typingTimeoutRef.current);
      typingTimeoutRef.current = setTimeout(() => {
        socket.emit('stopTyping', currentRoom);
      }, 1000);
    }
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    const socket = socketRef.current;

    if (inputMessage.trim() && socket && socket.connected) {
      socket.emit('chatMessage', { room: currentRoom, message: inputMessage.trim() }, (response) => {
        if (response.status === 'ok') {
          // Message sent successfully
        } else {
          setToast({ type: 'error', message: response.message || 'Failed to send message' });
        }
      });

      setInputMessage('');
      socket.emit('stopTyping', currentRoom);
    }
  };

  const handleMenuAction = (action) => {
    switch (action) {
      case 'open-all-widgets': {
        // Set all widgets to visible
        const allWidgetsVisible = {};
        Object.keys(WIDGET_TITLES).forEach(widgetId => {
          allWidgetsVisible[widgetId] = true;
        });
        setWidgetVisibility(allWidgetsVisible);
        setToast({ type: 'success', message: 'All widgets opened' });
        break;
      }
      case 'close-all-widgets': {
        // Set all widgets to hidden
        const allWidgetsHidden = {};
        Object.keys(WIDGET_TITLES).forEach(widgetId => {
          allWidgetsHidden[widgetId] = false;
        });
        setWidgetVisibility(allWidgetsHidden);
        setToast({ type: 'success', message: 'All widgets closed' });
        break;
      }
      case 'toggle-theme':
        setIsDarkMode(!isDarkMode);
        break;
      case 'force-loading':
        setDebugStates(prev => ({ ...prev, forceLoading: !prev.forceLoading }));
        setToast({ type: 'info', message: `Force Loading: ${!debugStates.forceLoading ? 'ON' : 'OFF'}` });
        break;
      case 'force-error':
        setDebugStates(prev => ({ ...prev, forceError: !prev.forceError }));
        setToast({ type: 'info', message: `Force Error: ${!debugStates.forceError ? 'ON' : 'OFF'}` });
        break;
      case 'reset-layout':
        resetLayout();
        break;
      case 'lock-widgets':
        setGlobalLock(true);
        setToast({ type: 'success', message: 'All widgets locked' });
        break;
      case 'unlock-widgets':
        setGlobalLock(false);
        setToast({ type: 'success', message: 'All widgets unlocked' });
        break;
      case 'save-layout':
        // Layout is auto-saved, but we can show a toast
        setToast({ type: 'success', message: 'Layout saved automatically' });
        break;
      case 'load-layout':
        handleLoadLayout();
        break;
      case 'export-layout': {
        // Export layout to JSON
        const layoutJson = JSON.stringify(layout, null, 2);
        const blob = new Blob([layoutJson], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'dashboard-layout.json';
        a.click();
        URL.revokeObjectURL(url);
        setToast({ type: 'success', message: 'Layout exported' });
        break;
      }
      case 'import-layout': {
        // Import layout from JSON
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'application/json';
        input.onchange = (e) => {
          const file = e.target.files[0];
          if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
              try {
                const imported = JSON.parse(event.target.result);
                if (Array.isArray(imported)) {
                  setLayout(imported);
                  setToast({ type: 'success', message: 'Layout imported' });
                } else {
                  setToast({ type: 'error', message: 'Invalid layout file' });
                }
              } catch (error) {
                setToast({ type: 'error', message: 'Failed to import layout' });
              }
            };
            reader.readAsText(file);
          }
        };
        input.click();
        break;
      }
      case 'new-dashboard':
        resetLayout();
        setToast({ type: 'info', message: 'New dashboard created' });
        break;
      case 'toggle-fullscreen':
        if (!document.fullscreenElement) {
          document.documentElement.requestFullscreen();
        } else {
          document.exitFullscreen();
        }
        break;
      case 'dev-tools':
        setToast({ type: 'info', message: 'Press F12 to open browser DevTools' });
        break;
      case 'about':
        setToast({ type: 'info', message: 'React + Node.js Template v1.0.0' });
        break;
      case 'shortcuts':
        setToast({ type: 'info', message: 'Check menu items for keyboard shortcuts' });
        break;
      default:
        console.log('Menu action:', action);
    }
  };

  return (
    <div className={`app-shell ${isDarkMode ? 'dark' : 'light'}`}>
      <MenuBar
        onMenuAction={handleMenuAction}
        isDarkMode={isDarkMode}
        widgetVisibility={widgetVisibility}
        onToggleWidget={handleToggleWidget}
        onTriggerModal={() => setShowModal(true)}
        onResetLayout={resetLayout}
        toggleTheme={() => setIsDarkMode(!isDarkMode)}
        onAutoSort={handleAutoSort}
        onSaveLayout={handleSaveLayout}
        onLoadLayout={handleLoadLayout}
        onToggleLogCenter={() => setShowLogCenter(!showLogCenter)}
        showLogCenter={showLogCenter}
        debugStates={debugStates}
        widgetTitles={WIDGET_TITLES}
        currentUser={currentUser}
        onLogout={handleLogout}
        onSignin={() => setIsAuthModalOpen(true)}
      />

      <AuthGuard onShowLogin={() => setIsAuthModalOpen(true)}>
        {/* <div className="auth-bypass"> */}
        <header className="hero">
          <div className="hero-glow" />
          <div className="hero-body" data-animate="fade">
            <h1>Welcome to DataFathom</h1>
          </div>
        </header>

        <main className="widget-grid-container">
          <GridLayout
            className="layout"
            layout={layout.filter(item => widgetVisibility[item.i] !== false)}
            onLayoutChange={throttledSetLayout}
            cols={48}
            rowHeight={60}
            width={gridWidth}
            isDraggable={!globalLock}
            isResizable={!globalLock}
            draggableHandle=".widget-drag-handle"
            resizeHandles={['se', 'sw', 'ne', 'nw', 's', 'n', 'e', 'w']}
            margin={[8, 8]}
            containerPadding={[0, 0]}
            useCSSTransforms={true}
            compactType="vertical"
            preventCollision={false}
          >
            {widgetVisibility['monitor-view'] !== false && (
              <div
                key="monitor-view"
                data-widget-id="monitor-view"
                className={`widget-wrapper ${widgetStates['monitor-view']?.minimized ? 'minimized' : ''} ${widgetStates['monitor-view']?.maximized ? 'maximized' : ''}`}
              >
                <WindowHeader
                  title={WIDGET_TITLES['monitor-view']}
                  onMinimize={() => handleWidgetMinimize('monitor-view')}
                  onMaximize={() => handleWidgetMaximize('monitor-view')}
                  onClose={() => handleWidgetClose('monitor-view')}
                  onLock={() => handleWidgetLock('monitor-view')}
                  onZoomIn={undefined}
                  onZoomOut={undefined}
                  onMinimumFullView={() => handleMinimumFullView('monitor-view')}
                  onViewSource={() => handleViewSource('monitor-view')}
                  isMaximized={widgetStates['monitor-view']?.maximized}
                  isLocked={widgetStates['monitor-view']?.locked}
                />
                <div className="widget-drag-handle" title="Drag to rearrange">
                  <span>⋮⋮</span>
                </div>
                {!widgetStates['monitor-view']?.minimized && (
                  <section className="glass card" data-animate="delay-1" style={{ overflow: 'hidden' }}>
                    <MonitorWidget />
                  </section>
                )}
              </div>
            )}

            {widgetVisibility['command-view'] !== false && (
              <div
                key="command-view"
                data-widget-id="command-view"
                className={`widget-wrapper ${widgetStates['command-view']?.minimized ? 'minimized' : ''} ${widgetStates['command-view']?.maximized ? 'maximized' : ''}`}
              >
                <WindowHeader
                  title={WIDGET_TITLES['command-view']}
                  onMinimize={() => handleWidgetMinimize('command-view')}
                  onMaximize={() => handleWidgetMaximize('command-view')}
                  onClose={() => handleWidgetClose('command-view')}
                  onLock={() => handleWidgetLock('command-view')}
                  onZoomIn={undefined}
                  onZoomOut={undefined}
                  onMinimumFullView={() => handleMinimumFullView('command-view')}
                  onViewSource={() => handleViewSource('command-view')}
                  isMaximized={widgetStates['command-view']?.maximized}
                  isLocked={widgetStates['command-view']?.locked}
                />
                <div className="widget-drag-handle" title="Drag to rearrange">
                  <span>⋮⋮</span>
                </div>
                {!widgetStates['command-view']?.minimized && (
                  <section className="glass card" data-animate="delay-2" style={{ overflow: 'hidden' }}>
                    <CommandWidget />
                  </section>
                )}
              </div>
            )}

            {widgetVisibility['portfolio-view'] !== false && (
              <div
                key="portfolio-view"
                data-widget-id="portfolio-view"
                className={`widget-wrapper ${widgetStates['portfolio-view']?.minimized ? 'minimized' : ''} ${widgetStates['portfolio-view']?.maximized ? 'maximized' : ''}`}
              >
                <WindowHeader
                  title={WIDGET_TITLES['portfolio-view']}
                  onMinimize={() => handleWidgetMinimize('portfolio-view')}
                  onMaximize={() => handleWidgetMaximize('portfolio-view')}
                  onClose={() => handleWidgetClose('portfolio-view')}
                  onLock={() => handleWidgetLock('portfolio-view')}
                  onZoomIn={undefined}
                  onZoomOut={undefined}
                  onMinimumFullView={() => handleMinimumFullView('portfolio-view')}
                  onViewSource={() => handleViewSource('portfolio-view')}
                  isMaximized={widgetStates['portfolio-view']?.maximized}
                  isLocked={widgetStates['portfolio-view']?.locked}
                />
                <div className="widget-drag-handle" title="Drag to rearrange">
                  <span>⋮⋮</span>
                </div>
                {!widgetStates['portfolio-view']?.minimized && (
                  <section className="glass card" data-animate="delay-3" style={{ overflow: 'hidden' }}>
                    <PortfolioWidget />
                  </section>
                )}
              </div>
            )}

            {widgetVisibility['research-view'] !== false && (
              <div
                key="research-view"
                data-widget-id="research-view"
                className={`widget-wrapper ${widgetStates['research-view']?.minimized ? 'minimized' : ''} ${widgetStates['research-view']?.maximized ? 'maximized' : ''}`}
              >
                <WindowHeader
                  title={WIDGET_TITLES['research-view']}
                  onMinimize={() => handleWidgetMinimize('research-view')}
                  onMaximize={() => handleWidgetMaximize('research-view')}
                  onClose={() => handleWidgetClose('research-view')}
                  onLock={() => handleWidgetLock('research-view')}
                  onZoomIn={undefined}
                  onZoomOut={undefined}
                  onMinimumFullView={() => handleMinimumFullView('research-view')}
                  onViewSource={() => handleViewSource('research-view')}
                  isMaximized={widgetStates['research-view']?.maximized}
                  isLocked={widgetStates['research-view']?.locked}
                />
                <div className="widget-drag-handle" title="Drag to rearrange">
                  <span>⋮⋮</span>
                </div>
                {!widgetStates['research-view']?.minimized && (
                  <section className="glass card" data-animate="delay-4" style={{ overflow: 'hidden' }}>
                    <ResearchWidget />
                  </section>
                )}
              </div>
            )}

            {widgetVisibility.api !== false && (
              <div
                key="api"
                data-widget-id="api"
                className={`widget-wrapper ${widgetStates.api?.minimized ? 'minimized' : ''} ${widgetStates.api?.maximized ? 'maximized' : ''}`}
              >
                <WindowHeader
                  title={WIDGET_TITLES.api}
                  onMinimize={() => handleWidgetMinimize('api')}
                  onMaximize={() => handleWidgetMaximize('api')}
                  onClose={() => handleWidgetClose('api')}
                  onLock={() => handleWidgetLock('api')}
                  onZoomIn={undefined}
                  onZoomOut={undefined}
                  onMinimumFullView={() => handleMinimumFullView('api')}
                  onViewSource={() => handleViewSource('api')}
                  isMaximized={widgetStates.api?.maximized}
                  isLocked={widgetStates.api?.locked}
                />
                <div className="widget-drag-handle" title="Drag to rearrange">
                  <span>⋮⋮</span>
                </div>
                {!widgetStates.api?.minimized && (
                  <section className="glass card api-card" data-animate="delay-1">
                    <header>
                      <h2>API Integration</h2>
                      <p>Demonstrates proxying API calls through Vite to Express.</p>
                    </header>
                    <div className="api-actions">
                      <button className="btn btn-primary" onClick={fetchApiData} disabled={loading || debugStates.forceLoading}>
                        {(loading || debugStates.forceLoading) ? 'Fetching…' : 'Fetch API Data'}
                      </button>
                      <button className="btn btn-secondary" onClick={() => setToast({ type: 'info', message: 'Simulated request sent' })}>
                        Simulate Request
                      </button>
                    </div>

                    <div className="api-panel">
                      {(loading || debugStates.forceLoading) && (
                        <div className="skeleton-block">
                          <div className="skeleton shimmer" />
                          <div className="skeleton shimmer" />
                          <div className="skeleton shimmer" />
                        </div>
                      )}

                      {!loading && !debugStates.forceLoading && (error || debugStates.forceError) && (
                        <div className="toast-inline error">
                          <strong>Request failed:</strong> {debugStates.forceError ? 'Debug: Forced error state' : error}
                        </div>
                      )}

                      {apiData && (
                        <>
                          <div className="data-grid">
                            {Object.entries(apiData).map(([key, value]) => (
                              <div key={key} className="data-row">
                                <span>{key}</span>
                                <span>{typeof value === 'object' ? JSON.stringify(value) : value?.toString()}</span>
                              </div>
                            ))}
                          </div>
                          <pre className="code-block" dangerouslySetInnerHTML={{ __html: syntaxMarkup }} />
                        </>
                      )}

                      {!loading && !apiData && !error && (
                        <p className="muted">Run the request to preview live data formatting.</p>
                      )}
                    </div>
                  </section>
                )}
              </div>
            )}

            {widgetVisibility.palette !== false && (
              <div
                key="palette"
                data-widget-id="palette"
                className={`widget-wrapper ${widgetStates.palette?.minimized ? 'minimized' : ''} ${widgetStates.palette?.maximized ? 'maximized' : ''}`}
              >
                <WindowHeader
                  title={WIDGET_TITLES.palette}
                  onMinimize={() => handleWidgetMinimize('palette')}
                  onMaximize={() => handleWidgetMaximize('palette')}
                  onClose={() => handleWidgetClose('palette')}
                  onLock={() => handleWidgetLock('palette')}
                  onZoomIn={undefined}
                  onZoomOut={undefined}
                  onMinimumFullView={() => handleMinimumFullView('palette')}
                  onViewSource={() => handleViewSource('palette')}
                  isMaximized={widgetStates.palette?.maximized}
                  isLocked={widgetStates.palette?.locked}
                />
                <div className="widget-drag-handle" title="Drag to rearrange">
                  <span>⋮⋮</span>
                </div>
                {!widgetStates.palette?.minimized && (
                  <section className="glass card palette-card" data-animate="delay-2">
                    <header>
                      <h2>Color System</h2>
                      <p>Driven entirely by <code>config/color_palette.json</code>.</p>
                    </header>
                    <div className="palette-swatches">
                      {COLOR_TOKENS.map((token) => {
                        const value = token.path.reduce((acc, key) => acc?.[key], palette) || '--';
                        const cssVarName = `--color-${token.path.join('-')}`;
                        const jsToken = `palette.${token.path.join('.')}`;

                        const handleCopyToken = async (text) => {
                          try {
                            await navigator.clipboard.writeText(text);
                            setToast({ type: 'success', message: `Copied: ${text}` });
                          } catch (err) {
                            setToast({ type: 'error', message: 'Failed to copy' });
                          }
                        };

                        return (
                          <div key={token.label} className="palette-swatch">
                            <span className="swatch-dot" style={{ backgroundColor: value }} />
                            <div>
                              <p>{token.label}</p>
                              <small
                                className="token-name"
                                onClick={() => handleCopyToken(cssVarName)}
                                title="Click to copy CSS variable"
                                style={{ cursor: 'pointer', textDecoration: 'underline' }}
                              >
                                CSS: var({cssVarName})
                              </small>
                              <small
                                className="token-name"
                                onClick={() => handleCopyToken(jsToken)}
                                title="Click to copy JS token"
                                style={{ cursor: 'pointer', textDecoration: 'underline', marginLeft: '0.5rem' }}
                              >
                                JS: {jsToken}
                              </small>
                              <small style={{ display: 'block', marginTop: '0.25rem', opacity: 0.7 }}>
                                Value: {value}
                              </small>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                    <div className="surface-stack">
                      {SURFACE_SCALE.map((surface) => (
                        <div key={surface.label} className="surface-chip" style={{ background: `var(${surface.token})` }}>
                          {surface.label}
                        </div>
                      ))}
                    </div>
                  </section>
                )}
              </div>
            )}

            {widgetVisibility.docker !== false && (
              <div
                key="docker"
                data-widget-id="docker"
                className={`widget-wrapper ${widgetStates.docker?.minimized ? 'minimized' : ''} ${widgetStates.docker?.maximized ? 'maximized' : ''}`}
              >
                <WindowHeader
                  title={WIDGET_TITLES.docker}
                  onMinimize={() => handleWidgetMinimize('docker')}
                  onMaximize={() => handleWidgetMaximize('docker')}
                  onClose={() => handleWidgetClose('docker')}
                  onLock={() => handleWidgetLock('docker')}
                  onZoomIn={undefined}
                  onZoomOut={undefined}
                  onMinimumFullView={() => handleMinimumFullView('docker')}
                  onViewSource={() => handleViewSource('docker')}
                  isMaximized={widgetStates.docker?.maximized}
                  isLocked={widgetStates.docker?.locked}
                />
                <div className="widget-drag-handle" title="Drag to rearrange">
                  <span>⋮⋮</span>
                </div>
                {!widgetStates.docker?.minimized && (
                  <section className="glass card" data-animate="delay-3">
                    <DockerWidget onToast={setToast} />
                  </section>
                )}
              </div>
            )}

            {widgetVisibility['window-manager'] !== false && (
              <div
                key="window-manager"
                data-widget-id="window-manager"
                className={`widget-wrapper ${widgetStates['window-manager']?.minimized ? 'minimized' : ''} ${widgetStates['window-manager']?.maximized ? 'maximized' : ''}`}
              >
                <WindowHeader
                  title={WIDGET_TITLES['window-manager']}
                  onMinimize={() => handleWidgetMinimize('window-manager')}
                  onMaximize={() => handleWidgetMaximize('window-manager')}
                  onClose={() => handleWidgetClose('window-manager')}
                  onLock={() => handleWidgetLock('window-manager')}
                  onZoomIn={undefined}
                  onZoomOut={undefined}
                  onMinimumFullView={() => handleMinimumFullView('window-manager')}
                  onViewSource={() => handleViewSource('window-manager')}
                  isMaximized={widgetStates['window-manager']?.maximized}
                  isLocked={widgetStates['window-manager']?.locked}
                />
                <div className="widget-drag-handle" title="Drag to rearrange">
                  <span>⋮⋮</span>
                </div>
                {!widgetStates['window-manager']?.minimized && (
                  <section className="glass card" data-animate="delay-3">
                    <WindowManagerWidget />
                  </section>
                )}
              </div>
            )}

            {widgetVisibility.checklist !== false && (
              <div
                key="checklist"
                data-widget-id="checklist"
                className={`widget-wrapper ${widgetStates.checklist?.minimized ? 'minimized' : ''} ${widgetStates.checklist?.maximized ? 'maximized' : ''}`}
              >
                <WindowHeader
                  title={WIDGET_TITLES.checklist}
                  onMinimize={() => handleWidgetMinimize('checklist')}
                  onMaximize={() => handleWidgetMaximize('checklist')}
                  onClose={() => handleWidgetClose('checklist')}
                  onLock={() => handleWidgetLock('checklist')}
                  onZoomIn={undefined}
                  onZoomOut={undefined}
                  onMinimumFullView={() => handleMinimumFullView('checklist')}
                  onViewSource={() => handleViewSource('checklist')}
                  isMaximized={widgetStates.checklist?.maximized}
                  isLocked={widgetStates.checklist?.locked}
                />
                <div className="widget-drag-handle" title="Drag to rearrange">
                  <span>⋮⋮</span>
                </div>
                {!widgetStates.checklist?.minimized && (
                  <section className="glass card checklist-card" data-animate="delay-3">
                    <header>
                      <h2>Launch Checklist</h2>
                      <p>Gamified tasks engineers can check off.</p>
                    </header>

                    <ol className="stepper">
                      {CHECKLIST_STEPS.map((step, idx) => (
                        <li key={step.title}>
                          <div className="step-icon">{idx + 1}</div>
                          <div>
                            <strong>{step.title}</strong>
                            <p>{step.description}</p>
                            <div className="command-chip">
                              <code>{step.command}</code>
                              <button onClick={() => handleCopy(step.command, `step-${idx}`)} aria-label={`Copy ${step.title} command`}>
                                {copiedCommand === `step-${idx}` ? 'Copied!' : '📋'}
                              </button>
                            </div>
                          </div>
                        </li>
                      ))}
                    </ol>
                  </section>
                )}
              </div>
            )}

            {widgetVisibility.telemetry !== false && (
              <div
                key="telemetry"
                data-widget-id="telemetry"
                className={`widget-wrapper ${widgetStates.telemetry?.minimized ? 'minimized' : ''} ${widgetStates.telemetry?.maximized ? 'maximized' : ''}`}
              >
                <WindowHeader
                  title={WIDGET_TITLES.telemetry}
                  onMinimize={() => handleWidgetMinimize('telemetry')}
                  onMaximize={() => handleWidgetMaximize('telemetry')}
                  onClose={() => handleWidgetClose('telemetry')}
                  onLock={() => handleWidgetLock('telemetry')}
                  onZoomIn={undefined}
                  onZoomOut={undefined}
                  onMinimumFullView={() => handleMinimumFullView('telemetry')}
                  onViewSource={() => handleViewSource('telemetry')}
                  isMaximized={widgetStates.telemetry?.maximized}
                  isLocked={widgetStates.telemetry?.locked}
                />
                <div className="widget-drag-handle" title="Drag to rearrange">
                  <span>⋮⋮</span>
                </div>
                {!widgetStates.telemetry?.minimized && (
                  <section className="glass card telemetry-card" data-animate="delay-4">
                    <header>
                      <h2>Server Telemetry</h2>
                      <p>Mocked memory usage sparkline.</p>
                    </header>
                    <div className="telemetry-body">
                      <div className="telemetry-stats">
                        <div>
                          <span>Current</span>
                          <strong>{memoryStats.current}%</strong>
                        </div>
                        <div>
                          <span>24h Avg</span>
                          <strong>{memoryStats.average}%</strong>
                        </div>
                      </div>
                      <MemoryChart data={memorySeries} />
                    </div>
                  </section>
                )}
              </div>
            )}

            {widgetVisibility.ux !== false && (
              <div
                key="ux"
                data-widget-id="ux"
                className={`widget-wrapper ${widgetStates.ux?.minimized ? 'minimized' : ''} ${widgetStates.ux?.maximized ? 'maximized' : ''}`}
              >
                <WindowHeader
                  title={WIDGET_TITLES.ux}
                  onMinimize={() => handleWidgetMinimize('ux')}
                  onMaximize={() => handleWidgetMaximize('ux')}
                  onClose={() => handleWidgetClose('ux')}
                  onLock={() => handleWidgetLock('ux')}
                  onZoomIn={undefined}
                  onZoomOut={undefined}
                  onMinimumFullView={() => handleMinimumFullView('ux')}
                  onViewSource={() => handleViewSource('ux')}
                  isMaximized={widgetStates.ux?.maximized}
                  isLocked={widgetStates.ux?.locked}
                />
                <div className="widget-drag-handle" title="Drag to rearrange">
                  <span>⋮⋮</span>
                </div>
                {!widgetStates.ux?.minimized && (
                  <section className="glass card ux-card" data-animate="delay-5">
                    <header>
                      <h2>Experience Controls</h2>
                      <p>Modal, toast, and copy interactions.</p>
                    </header>

                    <div className="command-list">
                      {TERMINAL_SNIPPETS.map((snippet, idx) => (
                        <div key={snippet.label} className="command-row">
                          <div>
                            <p>{snippet.label}</p>
                            <code>{snippet.command}</code>
                          </div>
                          <button onClick={() => handleCopy(snippet.command, `cmd-${idx}`)} className="btn-icon" aria-label={`Copy ${snippet.label}`}>
                            {copiedCommand === `cmd-${idx}` ? '✓' : '📋'}
                          </button>
                        </div>
                      ))}
                    </div>
                    <div className="ux-actions">
                      <button className="btn btn-secondary" onClick={() => setToast({ type: 'info', message: 'Toast notification triggered' })}>
                        Show Toast
                      </button>
                      <button className="btn btn-primary" onClick={triggerModal}>
                        View Logs Modal
                      </button>
                    </div>
                  </section>
                )}
              </div>
            )}

            {widgetVisibility.socketio !== false && (
              <div
                key="socketio"
                data-widget-id="socketio"
                className={`widget-wrapper ${widgetStates.socketio?.minimized ? 'minimized' : ''} ${widgetStates.socketio?.maximized ? 'maximized' : ''}`}
              >
                <WindowHeader
                  title={WIDGET_TITLES.socketio}
                  onMinimize={() => handleWidgetMinimize('socketio')}
                  onMaximize={() => handleWidgetMaximize('socketio')}
                  onClose={() => handleWidgetClose('socketio')}
                  onLock={() => handleWidgetLock('socketio')}
                  onZoomIn={undefined}
                  onZoomOut={undefined}
                  onMinimumFullView={() => handleMinimumFullView('socketio')}
                  onViewSource={() => handleViewSource('socketio')}
                  isMaximized={widgetStates.socketio?.maximized}
                  isLocked={widgetStates.socketio?.locked}
                />
                <div className="widget-drag-handle" title="Drag to rearrange">
                  <span>⋮⋮</span>
                </div>
                {!widgetStates.socketio?.minimized && (
                  <section className="glass card socketio-card" data-animate="delay-6">
                    <header>
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%' }}>
                        <div>
                          <h2>Socket.io Realtime</h2>
                          <p>Secure rooms, chat, and real-time communication.</p>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            <div
                              style={{
                                width: '12px',
                                height: '12px',
                                borderRadius: '50%',
                                backgroundColor: socketConnected ? '#10b981' : '#ef4444',
                                boxShadow: socketConnected ? '0 0 8px rgba(16, 185, 129, 0.6)' : 'none',
                                animation: socketConnected ? 'pulse 2s infinite' : 'none'
                              }}
                            />
                            <span style={{ fontSize: '0.875rem', fontWeight: 600 }}>
                              {socketConnected ? 'Connected' : 'Disconnected'}
                            </span>
                          </div>
                          {socketId && (
                            <span style={{ fontSize: '0.75rem', opacity: 0.7 }}>
                              ID: {socketId.substring(0, 8)}...
                            </span>
                          )}
                        </div>
                      </div>
                    </header>

                    <div className="socketio-panel">
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                          {ROOM_LIST.map((room) => (
                            <button
                              key={room.id}
                              onClick={() => handleJoinRoom(room)}
                              className={`btn ${currentRoom === room.id ? 'btn-primary' : 'btn-secondary'}`}
                              style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }}
                              disabled={!socketConnected}
                            >
                              {room.name}
                            </button>
                          ))}
                        </div>
                        <div style={{ fontSize: '0.875rem', opacity: 0.8 }}>
                          <strong>{clientCount}</strong> client{clientCount !== 1 ? 's' : ''} online
                        </div>
                      </div>

                      <div
                        style={{
                          border: '1px solid rgba(0,0,0,0.1)',
                          borderRadius: 'var(--radius-chip)',
                          padding: '1rem',
                          backgroundColor: 'rgba(0,0,0,0.02)',
                          marginBottom: '1rem',
                          minHeight: '200px',
                          maxHeight: '400px',
                          overflow: 'hidden',
                          display: 'flex',
                          flexDirection: 'column'
                        }}
                      >
                        <VirtualizedChatMessages
                          messages={socketMessages}
                          socketId={socketId}
                          messagesEndRef={messagesEndRef}
                          height={300}
                        />

                        {typingStatus && (
                          <div style={{
                            marginTop: '0.5rem',
                            fontSize: '0.75rem',
                            fontStyle: 'italic',
                            opacity: 0.7,
                            animation: 'pulse 1.5s infinite'
                          }}>
                            {typingStatus}
                          </div>
                        )}
                      </div>

                      <form onSubmit={handleSendMessage} style={{ display: 'flex', gap: '0.5rem' }}>
                        <input
                          type="text"
                          value={inputMessage}
                          onChange={handleInputChange}
                          placeholder={`Message #${currentRoom}...`}
                          disabled={!socketConnected}
                          style={{
                            flex: 1,
                            padding: '0.75rem',
                            border: '1px solid rgba(0,0,0,0.1)',
                            borderRadius: 'var(--radius-chip)',
                            fontSize: '0.875rem',
                            backgroundColor: 'rgba(255,255,255,0.8)'
                          }}
                        />
                        <button
                          type="submit"
                          className="btn btn-primary"
                          disabled={!socketConnected || !inputMessage.trim()}
                          style={{ padding: '0.75rem 1.5rem' }}
                        >
                          Send
                        </button>
                      </form>
                    </div>
                  </section>
                )}
              </div>
            )}

            {widgetVisibility['ping-api'] !== false && (
              <div
                key="ping-api"
                data-widget-id="ping-api"
                className={`widget-wrapper ${widgetStates['ping-api']?.minimized ? 'minimized' : ''} ${widgetStates['ping-api']?.maximized ? 'maximized' : ''}`}
              >
                <WindowHeader
                  title={WIDGET_TITLES['ping-api']}
                  onMinimize={() => handleWidgetMinimize('ping-api')}
                  onMaximize={() => handleWidgetMaximize('ping-api')}
                  onClose={() => handleWidgetClose('ping-api')}
                  onLock={() => handleWidgetLock('ping-api')}
                  onZoomIn={undefined}
                  onZoomOut={undefined}
                  onMinimumFullView={() => handleMinimumFullView('ping-api')}
                  onViewSource={() => handleViewSource('ping-api')}
                  isMaximized={widgetStates['ping-api']?.maximized}
                  isLocked={widgetStates['ping-api']?.locked}
                />
                <div className="widget-drag-handle" title="Drag to rearrange">
                  <span>⋮⋮</span>
                </div>
                {!widgetStates['ping-api']?.minimized && (
                  <section className="glass card ping-api-card" data-animate="delay-1">
                    <header>
                      <h2>Ping API</h2>
                      <p>Test API connectivity and view response data.</p>
                    </header>
                    <div className="api-actions" style={{ padding: '1rem' }}>
                      <button className="btn btn-primary" onClick={fetchApiData} disabled={loading} style={{ width: '100%' }}>
                        {loading ? 'Fetching…' : 'Fetch API Data'}
                      </button>
                      <button className="btn btn-secondary" onClick={() => setToast({ type: 'info', message: 'Simulated request sent' })} style={{ width: '100%', marginTop: '0.5rem' }}>
                        Simulate Request
                      </button>
                    </div>
                    {apiData && (
                      <div className="api-panel" style={{ padding: '0 1rem 1rem' }}>
                        <div className="data-grid">
                          {Object.entries(apiData).slice(0, 3).map(([key, value]) => (
                            <div key={key} className="data-row">
                              <span>{key}</span>
                              <span>{typeof value === 'object' ? JSON.stringify(value) : value?.toString()}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </section>
                )}
              </div>
            )}

            {widgetVisibility['server-status'] !== false && (
              <div
                key="server-status"
                data-widget-id="server-status"
                className={`widget-wrapper ${widgetStates['server-status']?.minimized ? 'minimized' : ''} ${widgetStates['server-status']?.maximized ? 'maximized' : ''}`}
              >
                <WindowHeader
                  title={WIDGET_TITLES['server-status']}
                  onMinimize={() => handleWidgetMinimize('server-status')}
                  onMaximize={() => handleWidgetMaximize('server-status')}
                  onClose={() => handleWidgetClose('server-status')}
                  onLock={() => handleWidgetLock('server-status')}
                  onZoomIn={undefined}
                  onZoomOut={undefined}
                  onMinimumFullView={() => handleMinimumFullView('server-status')}
                  onViewSource={() => handleViewSource('server-status')}
                  isMaximized={widgetStates['server-status']?.maximized}
                  isLocked={widgetStates['server-status']?.locked}
                />
                <div className="widget-drag-handle" title="Drag to rearrange">
                  <span>⋮⋮</span>
                </div>
                {!widgetStates['server-status']?.minimized && (
                  <section className="glass card server-status-card" data-animate="delay-1">
                    <header>
                      <h2>Server Status</h2>
                      <p>Monitor server and Socket.io connection status.</p>
                    </header>
                    <div style={{ padding: '1rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0.75rem', background: 'rgba(0,0,0,0.05)', borderRadius: 'var(--radius-chip)' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                          <div
                            style={{
                              width: '12px',
                              height: '12px',
                              borderRadius: '50%',
                              backgroundColor: serverStatus.tone === 'success' ? '#10b981' : serverStatus.tone === 'error' ? '#ef4444' : '#f59e0b',
                              boxShadow: serverStatus.tone === 'success' ? '0 0 8px rgba(16, 185, 129, 0.6)' : 'none',
                              animation: serverStatus.tone === 'success' ? 'pulse 2s infinite' : 'none'
                            }}
                          />
                          <div>
                            <p style={{ margin: 0, fontSize: '0.875rem', fontWeight: 600 }}>Server</p>
                            <p style={{ margin: 0, fontSize: '0.75rem', opacity: 0.7 }}>{serverStatus.label}</p>
                          </div>
                        </div>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0.75rem', background: 'rgba(0,0,0,0.05)', borderRadius: 'var(--radius-chip)' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                          <div
                            style={{
                              width: '12px',
                              height: '12px',
                              borderRadius: '50%',
                              backgroundColor: socketConnected ? '#10b981' : '#ef4444',
                              boxShadow: socketConnected ? '0 0 8px rgba(16, 185, 129, 0.6)' : 'none',
                              animation: socketConnected ? 'pulse 2s infinite' : 'none'
                            }}
                          />
                          <div>
                            <p style={{ margin: 0, fontSize: '0.875rem', fontWeight: 600 }}>Socket.io</p>
                            <p style={{ margin: 0, fontSize: '0.75rem', opacity: 0.7 }}>
                              {socketConnected ? 'Connected' : 'Disconnected'}
                              {socketConnected && clientCount > 0 && ` • ${clientCount} client${clientCount !== 1 ? 's' : ''}`}
                            </p>
                          </div>
                        </div>
                        {socketId && (
                          <span style={{ fontSize: '0.7rem', opacity: 0.6, fontFamily: 'monospace' }}>
                            {socketId.substring(0, 8)}...
                          </span>
                        )}
                      </div>
                    </div>
                  </section>
                )}
              </div>
            )}

            {widgetVisibility['bar-chart'] !== false && (
              <div
                key="bar-chart"
                data-widget-id="bar-chart"
                className={`widget-wrapper ${widgetStates['bar-chart']?.minimized ? 'minimized' : ''} ${widgetStates['bar-chart']?.maximized ? 'maximized' : ''}`}
              >
                <WindowHeader
                  title={WIDGET_TITLES['bar-chart']}
                  onMinimize={() => handleWidgetMinimize('bar-chart')}
                  onMaximize={() => handleWidgetMaximize('bar-chart')}
                  onClose={() => handleWidgetClose('bar-chart')}
                  onLock={() => handleWidgetLock('bar-chart')}
                  onZoomIn={undefined}
                  onZoomOut={undefined}
                  onMinimumFullView={() => handleMinimumFullView('bar-chart')}
                  onViewSource={() => handleViewSource('bar-chart')}
                  isMaximized={widgetStates['bar-chart']?.maximized}
                  isLocked={widgetStates['bar-chart']?.locked}
                />
                <div className="widget-drag-handle" title="Drag to rearrange">
                  <span>⋮⋮</span>
                </div>
                {!widgetStates['bar-chart']?.minimized && (
                  <section className="glass card bar-chart-card" data-animate="delay-1" style={{ padding: 0, margin: 0, height: '100%', display: 'flex', flexDirection: 'column' }}>
                    <header style={{ padding: '0.25rem', margin: 0, flexShrink: 0 }}>
                      <h2 style={{ margin: 0, fontSize: '1rem' }}>Bar Chart</h2>
                    </header>
                    <div style={{ flex: 1, padding: 0, margin: 0, overflow: 'hidden', minHeight: 0 }}>
                      <SimpleBarChart
                        data={[
                          {
                            label: 'Q1 Sales',
                            values: [
                              { x: 'Jan', y: 45 },
                              { x: 'Feb', y: 52 },
                              { x: 'Mar', y: 48 },
                            ]
                          },
                          {
                            label: 'Q2 Sales',
                            values: [
                              { x: 'Apr', y: 61 },
                              { x: 'May', y: 55 },
                              { x: 'Jun', y: 67 },
                            ]
                          },
                          {
                            label: 'Q3 Sales',
                            values: [
                              { x: 'Jul', y: 58 },
                              { x: 'Aug', y: 64 },
                              { x: 'Sep', y: 72 },
                            ]
                          },
                          {
                            label: 'Q4 Sales',
                            values: [
                              { x: 'Oct', y: 68 },
                              { x: 'Nov', y: 75 },
                              { x: 'Dec', y: 82 },
                            ]
                          }
                        ]}
                      />
                    </div>
                  </section>
                )}
              </div>
            )}

            {widgetVisibility['pie-chart'] !== false && (
              <div
                key="pie-chart"
                data-widget-id="pie-chart"
                className={`widget-wrapper ${widgetStates['pie-chart']?.minimized ? 'minimized' : ''} ${widgetStates['pie-chart']?.maximized ? 'maximized' : ''}`}
              >
                <WindowHeader
                  title={WIDGET_TITLES['pie-chart']}
                  onMinimize={() => handleWidgetMinimize('pie-chart')}
                  onMaximize={() => handleWidgetMaximize('pie-chart')}
                  onClose={() => handleWidgetClose('pie-chart')}
                  onLock={() => handleWidgetLock('pie-chart')}
                  onZoomIn={undefined}
                  onZoomOut={undefined}
                  onMinimumFullView={() => handleMinimumFullView('pie-chart')}
                  onViewSource={() => handleViewSource('pie-chart')}
                  isMaximized={widgetStates['pie-chart']?.maximized}
                  isLocked={widgetStates['pie-chart']?.locked}
                />
                <div className="widget-drag-handle" title="Drag to rearrange">
                  <span>⋮⋮</span>
                </div>
                {!widgetStates['pie-chart']?.minimized && (
                  <section className="glass card pie-chart-card" data-animate="delay-1" style={{ padding: 0, margin: 0, height: '100%', display: 'flex', flexDirection: 'column' }}>
                    <header style={{ padding: '0.25rem', margin: 0, flexShrink: 0 }}>
                      <h2 style={{ margin: 0, fontSize: '1rem' }}>Pie Chart</h2>
                    </header>
                    <div style={{ flex: 1, padding: 0, margin: 0, overflow: 'hidden', minHeight: 0 }}>
                      <SimplePieChart
                        data={{
                          label: 'Market Share',
                          values: [
                            { x: 'Product A', y: 35 },
                            { x: 'Product B', y: 28 },
                            { x: 'Product C', y: 22 },
                            { x: 'Product D', y: 15 },
                          ]
                        }}
                      />
                    </div>
                  </section>
                )}
              </div>
            )}

            {widgetVisibility['line-chart'] !== false && (
              <div
                key="line-chart"
                data-widget-id="line-chart"
                className={`widget-wrapper ${widgetStates['line-chart']?.minimized ? 'minimized' : ''} ${widgetStates['line-chart']?.maximized ? 'maximized' : ''}`}
              >
                <WindowHeader
                  title={WIDGET_TITLES['line-chart']}
                  onMinimize={() => handleWidgetMinimize('line-chart')}
                  onMaximize={() => handleWidgetMaximize('line-chart')}
                  onClose={() => handleWidgetClose('line-chart')}
                  onLock={() => handleWidgetLock('line-chart')}
                  onZoomIn={undefined}
                  onZoomOut={undefined}
                  onMinimumFullView={() => handleMinimumFullView('line-chart')}
                  onViewSource={() => handleViewSource('line-chart')}
                  isMaximized={widgetStates['line-chart']?.maximized}
                  isLocked={widgetStates['line-chart']?.locked}
                />
                <div className="widget-drag-handle" title="Drag to rearrange">
                  <span>⋮⋮</span>
                </div>
                {!widgetStates['line-chart']?.minimized && (
                  <section className="glass card line-chart-card" data-animate="delay-1" style={{ padding: 0, margin: 0, height: '100%', display: 'flex', flexDirection: 'column' }}>
                    <header style={{ padding: '0.25rem', margin: 0, flexShrink: 0 }}>
                      <h2 style={{ margin: 0, fontSize: '1rem' }}>Line Chart</h2>
                    </header>
                    <div style={{ flex: 1, padding: 0, margin: 0, overflow: 'hidden', minHeight: 0 }}>
                      <SimpleLineChart
                        data={[
                          {
                            label: 'Revenue',
                            values: [
                              { x: 'Week 1', y: 1200 },
                              { x: 'Week 2', y: 1900 },
                              { x: 'Week 3', y: 3000 },
                              { x: 'Week 4', y: 2800 },
                              { x: 'Week 5', y: 3500 },
                              { x: 'Week 6', y: 4200 },
                            ]
                          },
                          {
                            label: 'Expenses',
                            values: [
                              { x: 'Week 1', y: 800 },
                              { x: 'Week 2', y: 1100 },
                              { x: 'Week 3', y: 1500 },
                              { x: 'Week 4', y: 1400 },
                              { x: 'Week 5', y: 1800 },
                              { x: 'Week 6', y: 2100 },
                            ]
                          }
                        ]}
                      />
                    </div>
                  </section>
                )}
              </div>
            )}

            {widgetVisibility['area-chart'] !== false && (
              <div
                key="area-chart"
                data-widget-id="area-chart"
                className={`widget-wrapper ${widgetStates['area-chart']?.minimized ? 'minimized' : ''} ${widgetStates['area-chart']?.maximized ? 'maximized' : ''}`}
              >
                <WindowHeader
                  title={WIDGET_TITLES['area-chart']}
                  onMinimize={() => handleWidgetMinimize('area-chart')}
                  onMaximize={() => handleWidgetMaximize('area-chart')}
                  onClose={() => handleWidgetClose('area-chart')}
                  onLock={() => handleWidgetLock('area-chart')}
                  onZoomIn={undefined}
                  onZoomOut={undefined}
                  onMinimumFullView={() => handleMinimumFullView('area-chart')}
                  onViewSource={() => handleViewSource('area-chart')}
                  isMaximized={widgetStates['area-chart']?.maximized}
                  isLocked={widgetStates['area-chart']?.locked}
                />
                <div className="widget-drag-handle" title="Drag to rearrange">
                  <span>⋮⋮</span>
                </div>
                {!widgetStates['area-chart']?.minimized && (
                  <section className="glass card area-chart-card" data-animate="delay-1" style={{ padding: 0, margin: 0, height: '100%', display: 'flex', flexDirection: 'column' }}>
                    <header style={{ padding: '0.25rem', margin: 0, flexShrink: 0 }}>
                      <h2 style={{ margin: 0, fontSize: '1rem' }}>Area Chart</h2>
                    </header>
                    <div style={{ flex: 1, padding: 0, margin: 0, overflow: 'hidden', minHeight: 0 }}>
                      <SimpleAreaChart
                        data={[
                          {
                            label: 'Desktop',
                            values: [
                              { x: 'Jan', y: 4000 },
                              { x: 'Feb', y: 3000 },
                              { x: 'Mar', y: 5000 },
                              { x: 'Apr', y: 2780 },
                              { x: 'May', y: 1890 },
                            ]
                          },
                          {
                            label: 'Mobile',
                            values: [
                              { x: 'Jan', y: 2400 },
                              { x: 'Feb', y: 1398 },
                              { x: 'Mar', y: 9800 },
                              { x: 'Apr', y: 3908 },
                              { x: 'May', y: 4800 },
                            ]
                          },
                          {
                            label: 'Tablet',
                            values: [
                              { x: 'Jan', y: 2000 },
                              { x: 'Feb', y: 1800 },
                              { x: 'Mar', y: 3000 },
                              { x: 'Apr', y: 2500 },
                              { x: 'May', y: 2200 },
                            ]
                          }
                        ]}
                      />
                    </div>
                  </section>
                )}
              </div>
            )}

            {widgetVisibility['scatter-plot'] !== false && (
              <div
                key="scatter-plot"
                data-widget-id="scatter-plot"
                className={`widget-wrapper ${widgetStates['scatter-plot']?.minimized ? 'minimized' : ''} ${widgetStates['scatter-plot']?.maximized ? 'maximized' : ''}`}
              >
                <WindowHeader
                  title={WIDGET_TITLES['scatter-plot']}
                  onMinimize={() => handleWidgetMinimize('scatter-plot')}
                  onMaximize={() => handleWidgetMaximize('scatter-plot')}
                  onClose={() => handleWidgetClose('scatter-plot')}
                  onLock={() => handleWidgetLock('scatter-plot')}
                  onZoomIn={undefined}
                  onZoomOut={undefined}
                  onMinimumFullView={() => handleMinimumFullView('scatter-plot')}
                  onViewSource={() => handleViewSource('scatter-plot')}
                  isMaximized={widgetStates['scatter-plot']?.maximized}
                  isLocked={widgetStates['scatter-plot']?.locked}
                />
                <div className="widget-drag-handle" title="Drag to rearrange">
                  <span>⋮⋮</span>
                </div>
                {!widgetStates['scatter-plot']?.minimized && (
                  <section className="glass card scatter-plot-card" data-animate="delay-1" style={{ padding: 0, margin: 0, height: '100%', display: 'flex', flexDirection: 'column' }}>
                    <header style={{ padding: '0.25rem', margin: 0, flexShrink: 0 }}>
                      <h2 style={{ margin: 0, fontSize: '1rem' }}>Scatter Plot</h2>
                    </header>
                    <div style={{ flex: 1, padding: 0, margin: 0, overflow: 'hidden', minHeight: 0 }}>
                      <Suspense fallback={<div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>Loading chart...</div>}>
                        <SimpleScatterPlot
                          data={[
                            {
                              label: 'Group A',
                              values: [
                                { x: 100, y: 200 },
                                { x: 120, y: 100 },
                                { x: 170, y: 300 },
                                { x: 140, y: 250 },
                                { x: 150, y: 400 },
                                { x: 110, y: 280 },
                              ]
                            },
                            {
                              label: 'Group B',
                              values: [
                                { x: 200, y: 100 },
                                { x: 220, y: 300 },
                                { x: 270, y: 200 },
                                { x: 240, y: 350 },
                                { x: 250, y: 150 },
                                { x: 210, y: 180 },
                              ]
                            }
                          ]}
                        />
                      </Suspense>
                    </div>
                  </section>
                )}
              </div>
            )}

            {widgetVisibility['moving-average'] !== false && (
              <div
                key="moving-average"
                data-widget-id="moving-average"
                className={`widget-wrapper ${widgetStates['moving-average']?.minimized ? 'minimized' : ''} ${widgetStates['moving-average']?.maximized ? 'maximized' : ''}`}
              >
                <WindowHeader
                  title={WIDGET_TITLES['moving-average']}
                  onMinimize={() => handleWidgetMinimize('moving-average')}
                  onMaximize={() => handleWidgetMaximize('moving-average')}
                  onClose={() => handleWidgetClose('moving-average')}
                  onLock={() => handleWidgetLock('moving-average')}
                  onZoomIn={undefined}
                  onZoomOut={undefined}
                  onMinimumFullView={() => handleMinimumFullView('moving-average')}
                  onViewSource={() => handleViewSource('moving-average')}
                  isMaximized={widgetStates['moving-average']?.maximized}
                  isLocked={widgetStates['moving-average']?.locked}
                />
                <div className="widget-drag-handle" title="Drag to rearrange">
                  <span>⋮⋮</span>
                </div>
                {!widgetStates['moving-average']?.minimized && (
                  <section className="glass card moving-average-card" data-animate="delay-1" style={{ padding: 0, margin: 0, height: '100%', display: 'flex', flexDirection: 'column' }}>
                    <header style={{ padding: '0.25rem', margin: 0, flexShrink: 0 }}>
                      <h2 style={{ margin: 0, fontSize: '1rem' }}>Moving Average</h2>
                    </header>
                    <div style={{ flex: 1, padding: 0, margin: 0, overflow: 'hidden', minHeight: 0 }}>
                      <Suspense fallback={<div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>Loading chart...</div>}>
                        <MovingAverageChart
                          rawData={[
                            { x: 'Day 1', y: 62 },
                            { x: 'Day 2', y: 65 },
                            { x: 'Day 3', y: 64 },
                            { x: 'Day 4', y: 70 },
                            { x: 'Day 5', y: 66 },
                            { x: 'Day 6', y: 72 },
                            { x: 'Day 7', y: 68 },
                            { x: 'Day 8', y: 73 },
                            { x: 'Day 9', y: 69 },
                            { x: 'Day 10', y: 75 },
                            { x: 'Day 11', y: 71 },
                            { x: 'Day 12', y: 78 },
                          ]}
                          windowSize={5}
                        />
                      </Suspense>
                    </div>
                  </section>
                )}
              </div>
            )}

            {widgetVisibility['audio-waveform'] !== false && (
              <div
                key="audio-waveform"
                data-widget-id="audio-waveform"
                className={`widget-wrapper ${widgetStates['audio-waveform']?.minimized ? 'minimized' : ''} ${widgetStates['audio-waveform']?.maximized ? 'maximized' : ''}`}
              >
                <WindowHeader
                  title={WIDGET_TITLES['audio-waveform']}
                  onMinimize={() => handleWidgetMinimize('audio-waveform')}
                  onMaximize={() => handleWidgetMaximize('audio-waveform')}
                  onClose={() => handleWidgetClose('audio-waveform')}
                  onLock={() => handleWidgetLock('audio-waveform')}
                  onZoomIn={undefined}
                  onZoomOut={undefined}
                  onMinimumFullView={() => handleMinimumFullView('audio-waveform')}
                  onViewSource={() => handleViewSource('audio-waveform')}
                  isMaximized={widgetStates['audio-waveform']?.maximized}
                  isLocked={widgetStates['audio-waveform']?.locked}
                />
                <div className="widget-drag-handle" title="Drag to rearrange">
                  <span>⋮⋮</span>
                </div>
                {!widgetStates['audio-waveform']?.minimized && (
                  <section className="glass card audio-waveform-card" data-animate="delay-1" style={{ padding: 0, margin: 0, height: '100%', display: 'flex', flexDirection: 'column' }}>
                    <header style={{ padding: '0.25rem', margin: 0, flexShrink: 0 }}>
                      <h2 style={{ margin: 0, fontSize: '1rem' }}>Audio Waveform</h2>
                    </header>
                    <div style={{ flex: 1, padding: 0, margin: 0, overflow: 'hidden', minHeight: 0 }}>
                      <Suspense fallback={<div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>Loading waveform...</div>}>
                        <AudioWaveform
                          data={Array.from({ length: 100 }, (_, i) => Math.random() * 0.8 + 0.1)}
                        />
                      </Suspense>
                    </div>
                  </section>
                )}
              </div>
            )}








          </GridLayout>
        </main>

        <footer className="app-footer">
          <p>Modernized React + Node template · Glass / Motion ready · Dark mode aware</p>
        </footer>

      </AuthGuard >

      {
        toast && (
          <div className={`toast toast-${toast.type}`}>
            <span>{toast.message}</span>
            <button onClick={() => setToast(null)} aria-label="Dismiss notification">
              ×
            </button>
          </div>
        )
      }

      {
        showModal && (
          <div className="modal-overlay" role="dialog" aria-modal="true" aria-label="Detailed logs">
            <div className="modal glass">
              <header>
                <h3>Deployment Logs</h3>
                <button onClick={closeModal} className="btn-icon" aria-label="Close modal">
                  ×
                </button>
              </header>
              <div className="modal-body">
                <code>
                  <span>[04:00:12]</span> ✅ Build complete (3.4s)
                  <br />
                  <span>[04:00:13]</span> 🚀 Deploying to nodes…
                  <br />
                  <span>[04:00:18]</span> 💡 Tip: Hook into the CLI to register new micro-apps.
                </code>
              </div>
              <div className="modal-actions">
                <button className="btn btn-secondary" onClick={closeModal}>
                  Dismiss
                </button>
                <button className="btn btn-primary" onClick={() => setToast({ type: 'success', message: 'Logs exported' })}>
                  Export Logs
                </button>
              </div>
            </div>
          </div>
        )
      }

      {/* View Source Modal */}
      {
        viewSource.source && (
          <ViewSource
            source={viewSource.source}
            onClose={() => setViewSource({ widgetId: null, source: null })}
          />
        )
      }

      {/* Minimized Widget Dock */}
      {
        minimizedWidgets.length > 0 && (
          <div className="widget-dock">
            <div className="dock-header">Minimized Widgets</div>
            <div className="dock-items">
              {minimizedWidgets.map(widgetId => (
                <button
                  key={widgetId}
                  className="dock-item"
                  onClick={() => handleRestoreFromDock(widgetId)}
                  title={`Restore ${WIDGET_TITLES[widgetId] || widgetId}`}
                >
                  {WIDGET_TITLES[widgetId] || widgetId}
                </button>
              ))}
            </div>
          </div>
        )
      }

      {/* Log Center Drawer */}
      <LogCenter
        isOpen={showLogCenter}
        onClose={() => setShowLogCenter(false)}
        logHistory={logHistory}
      />
      <LoginModal
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
        onLoginSuccess={handleLoginSuccess}
      />
    </div >

  );
}

export default App;

