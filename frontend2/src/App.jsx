
import React, { useEffect, useMemo, useState, useRef, useCallback, Suspense, lazy } from 'react';
import { useColorPalette } from './hooks/useColorPalette';
import { useWidgetLayout } from './hooks/useWidgetLayout';
import { authService } from './utils/authService';
import io from 'socket.io-client';

// Layout & Components
import MenuBar from './components/MenuBar';
import AuthGuard from './components/AuthGuard';
import GlobalErrorBoundary from './components/GlobalErrorBoundary';
import LoginModal from './components/LoginModal';
import Dashboard from './pages/Dashboard';
import './App.css';

import { Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';
import Breadcrumbs from './components/Navigation/Breadcrumbs';
import SubHeaderNav from './components/Navigation/SubHeaderNav';
import { useSymbolLinking } from './hooks/useSymbolLinking';
import { useHotkeys } from './hooks/useHotkeys';
import { useNotifications } from './hooks/useNotifications';
import TradeConfirmationModal from './components/Modals/TradeConfirmationModal';
import presenceService from './services/presenceService';

// Lazy load other pages
const MissionControl = lazy(() => import('./pages/MissionControl'));
const PoliticalAlpha = lazy(() => import('./pages/PoliticalAlpha'));
const StrategyDistillery = lazy(() => import('./pages/StrategyDistillery'));
const DebateRoom = lazy(() => import('./pages/DebateRoom'));
const AutoCoderDashboard = lazy(() => import('./pages/AutoCoderDashboard'));
const VRCockpit = lazy(() => import('./pages/VRCockpit'));
const TerminalWorkspace = lazy(() => import('./pages/TerminalWorkspace'));
const OptionsAnalytics = lazy(() => import('./pages/OptionsAnalytics'));
const BacktestPortfolio = lazy(() => import('./pages/BacktestPortfolio'));
const OptionsChainWidget = lazy(() => import('./components/AI_Investor/Views/OptionsChainWidget'));
const MarketDepthWidget = lazy(() => import('./components/AI_Investor/Views/MarketDepthWidget'));
const TradeTapeWidget = lazy(() => import('./components/AI_Investor/Views/TradeTapeWidget'));
const GlobalScanner = lazy(() => import('./pages/GlobalScanner'));

const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5000';
const SOCKET_SERVER_URL = `http://localhost:${BACKEND_PORT}`;

const INITIAL_MEMORY_POINTS = Array.from({ length: 100 }, (_, i) => 48 + Math.random() * 42);

function App() {
  const navigate = useNavigate();
  const location = useLocation();
  const { palette } = useColorPalette();
  const {
    layout,
    setLayout,
    resetLayout,
    activeWorkspace,
    workspaces,
    saveWorkspace,
    loadWorkspace
  } = useWidgetLayout();
  const [isDarkMode, setIsDarkMode] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [toast, setToast] = useState(null);
  const [globalLock, setGlobalLock] = useState(false);
  const [currentUser, setCurrentUser] = useState(authService.getCurrentUser());
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(!authService.isAuthenticated());
  const [showLogCenter, setShowLogCenter] = useState(false);
  const [debugStates, setDebugStates] = useState({ forceLoading: false, forceError: false });

  // Widget visibility and states (Synchronized with Dashboard)
  const [widgetVisibility, setWidgetVisibility] = useState(() => {
    const saved = localStorage.getItem('react_node_template_widget_visibility');
    return saved ? JSON.parse(saved) : {};
  });

  const [widgetStates, setWidgetStates] = useState(() => {
    const saved = localStorage.getItem('react_node_template_widget_states');
    return saved ? JSON.parse(saved) : {};
  });

  const [socketConnected, setSocketConnected] = useState(false);
  const { groups, setGroupTicker } = useSymbolLinking();
  const socketRef = useRef(null);

  const { notify } = useNotifications();
  const [tradeModal, setTradeModal] = useState({ open: false, details: null });

  // Global Hotkeys
  useHotkeys({
    'Shift+B': () => setTradeModal({ open: true, details: { symbol: groups.none || 'SPY', side: 'BUY', quantity: 10, price: 480.00 } }),
    'Shift+S': () => setTradeModal({ open: true, details: { symbol: groups.none || 'SPY', side: 'SELL', quantity: 10, price: 480.00 } }),
    'Ctrl+Shift+S': () => handleSaveWorkspacePrompt(),
    'Alt+1': () => navigate('/workspace/terminal'),
    'Alt+2': () => navigate('/analytics/options'),
    'Alt+3': () => navigate('/portfolio/backtest'),
    'Alt+4': () => navigate('/scanner/global'),
  });

  const handleSaveWorkspacePrompt = () => {
    const name = prompt('Enter a name for this workspace:', activeWorkspace);
    if (name) saveWorkspace(name);
  };

  useEffect(() => {
    document.body.classList.toggle('theme-dark', isDarkMode);
  }, [isDarkMode]);

  // Socket.io initialization
  useEffect(() => {
    if (socketRef.current) return;
    socketRef.current = io(SOCKET_SERVER_URL, { transports: ['websocket', 'polling'] });
    const socket = socketRef.current;
    socket.on('connect', () => setSocketConnected(true));
    socket.on('disconnect', () => setSocketConnected(false));

    // Presence Service listeners (Phase 48)
    if (currentUser) {
      presenceService.initialize(currentUser.id, currentUser.username);

      presenceService.on('risk:alert', (data) => {
        notify({ title: 'RISK BREACH', body: data.message, type: 'error' });
      });

      presenceService.on('trade:fill', (data) => {
        notify({ title: 'ORDER FILLED', body: `${data.symbol} ${data.side} ${data.quantity} @ ${data.price}`, type: 'success' });
      });
    }

    return () => {
      socket.disconnect();
      presenceService.disconnect();
    };
  }, [currentUser, notify]);

  const handleMenuAction = (action) => {
    switch (action) {
      case 'show-dashboard': navigate('/workspace/terminal'); break;
      case 'show-mission-control': navigate('/workspace/mission-control'); break;
      case 'show-political-alpha': navigate('/analytics/political'); break;
      case 'show-strategy-distillery': navigate('/analytics/strategy'); break;
      case 'show-debate-chamber': navigate('/workspace/debate'); break;
      case 'show-auto-coder': navigate('/workspace/autocoder'); break;
      case 'show-vr-cockpit': navigate('/workspace/vr'); break;
      case 'show-options': navigate('/analytics/options'); break;
      case 'show-backtest': navigate('/portfolio/backtest'); break;
      case 'show-scanner': navigate('/scanner/global'); break;
      case 'toggle-theme': setIsDarkMode(!isDarkMode); break;
      case 'reset-layout': resetLayout(); break;
      default: console.log('Menu action:', action);
    }
  };

  const handleLogout = () => {
    authService.logout();
    setCurrentUser(null);
    setIsAuthModalOpen(true);
  };

  return (
    <GlobalErrorBoundary>
      <div className={`app-shell ${isDarkMode ? 'dark' : 'light'}`}>
        <MenuBar
          onMenuAction={handleMenuAction}
          isDarkMode={isDarkMode}
          widgetVisibility={widgetVisibility}
          onToggleWidget={() => { }}
          onTriggerModal={() => setShowModal(true)}
          onResetLayout={resetLayout}
          toggleTheme={() => setIsDarkMode(!isDarkMode)}
          onSaveLayout={() => { }}
          onLoadLayout={() => { }}
          onToggleLogCenter={() => setShowLogCenter(!showLogCenter)}
          showLogCenter={showLogCenter}
          debugStates={debugStates}
          currentUser={currentUser}
          onLogout={handleLogout}
          onSignin={() => setIsAuthModalOpen(true)}
          activeWorkspace={activeWorkspace}
          workspaces={workspaces}
          onLoadWorkspace={loadWorkspace}
          onSaveWorkspacePrompt={handleSaveWorkspacePrompt}
        />

        <AuthGuard onShowLogin={() => setIsAuthModalOpen(true)}>
          <SubHeaderNav />
          <header className="hero">
            <div className="hero-glow" />
            <div className="hero-body">
              <h1>Welcome to DataFathom</h1>
            </div>
          </header>

          <main className="institutional-os-container">
            <Breadcrumbs />
            <Suspense fallback={<div className="loading-state">Loading View...</div>}>
              <Routes>
                <Route path="/" element={<Navigate to="/workspace/terminal" replace />} />
                <Route path="/workspace/terminal" element={
                  <TerminalWorkspace
                    setToast={setToast}
                    handleViewSource={() => { }}
                    globalLock={globalLock}
                    isDarkMode={isDarkMode}
                    widgetStates={widgetStates}
                    setWidgetStates={setWidgetStates}
                    widgetVisibility={widgetVisibility}
                    setWidgetVisibility={setWidgetVisibility}
                  />
                } />
                <Route path="/workspace/mission-control" element={<MissionControl />} />
                <Route path="/analytics/political" element={<PoliticalAlpha />} />
                <Route path="/analytics/strategy" element={<StrategyDistillery />} />
                <Route path="/workspace/debate" element={<DebateRoom />} />
                <Route path="/workspace/autocoder" element={<AutoCoderDashboard />} />
                <Route path="/workspace/vr" element={<VRCockpit />} />
                <Route path="/analytics/options" element={<OptionsAnalytics />} />
                <Route path="/portfolio/backtest" element={<BacktestPortfolio />} />
                <Route path="/scanner/global" element={<GlobalScanner />} />
              </Routes>
            </Suspense>
          </main>

          <footer className="app-footer">
            <p>AI Investor Platform | DataFathom DeepMind | Multi-Tenant Isolated</p>
          </footer>
        </AuthGuard>

        {toast && (
          <div className={`toast ${toast.type}`}>
            {toast.message}
          </div>
        )}

        <LoginModal
          isOpen={isAuthModalOpen}
          onClose={() => setIsAuthModalOpen(false)}
          onLoginSuccess={() => {
            setCurrentUser(authService.getCurrentUser());
            setIsAuthModalOpen(false);
          }}
        />

        <TradeConfirmationModal
          isOpen={tradeModal.open}
          onClose={() => setTradeModal({ ...tradeModal, open: false })}
          tradeDetails={tradeModal.details}
          onConfirm={(details) => {
            setTradeModal({ ...tradeModal, open: false });
            setToast({ message: `ORDER EXECUTED: ${details.symbol} ${details.side} ${details.quantity} @ ${details.price}`, type: 'success' });
            // In real app, dispatch to execution service
          }}
        />
      </div>
    </GlobalErrorBoundary>
  );
}

export default App;
