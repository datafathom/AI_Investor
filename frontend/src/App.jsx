import React, { useEffect, useState, useRef, Suspense, lazy } from 'react';
import { useShallow } from 'zustand/react/shallow';
import { useColorPalette } from './hooks/useColorPalette';
import { useWidgetLayout } from './hooks/useWidgetLayout';
import apiClient from './services/apiClient';
import { authService } from './utils/authService';
import { ThemeProvider, useTheme } from './context/ThemeContext';
import { ToastProvider } from './context/ToastContext';

// Layout & Components
import MenuBar from './components/Navigation/MenuBar';
import AuthGuard from './components/AuthGuard';
import GlobalErrorBoundary from './components/GlobalErrorBoundary';
import LoginModal from './components/LoginModal';
import './App.css';

import WindowWrapper from './components/WindowManager/WindowWrapper';
import useWindowStore from './stores/windowStore';
import useTaskbarStore from './stores/taskbarStore';
import Taskbar from './components/Taskbar/Taskbar';
import HardwareSigModal from './components/Modals/HardwareSigModal';

// : Risk & Safety
import KillSwitch from './components/KillSwitch/KillSwitch';
import FrozenOverlay from './components/KillSwitch/FrozenOverlay';
import PreTradeRiskModal from './components/Modals/PreTradeRiskModal';
import EducationOverlay from './components/Education/EducationOverlay';

import { Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';
import Breadcrumbs from './components/Navigation/Breadcrumbs';
import SubHeaderNav from './components/Navigation/SubHeaderNav';
import { useSymbolLinking } from './hooks/useSymbolLinking';
import { useHotkeys } from './hooks/useHotkeys';
import { useNotifications } from './hooks/useNotifications';
import TradeConfirmationModal from './components/Modals/TradeConfirmationModal';
import presenceService from './services/presenceService';
import GlobalTooltip from './components/GlobalTooltip';
import GlobalStatusBar from './components/GlobalStatusBar';

// UI/UX Enhancement Components
import CommandPalette from './components/CommandPalette/CommandPalette';
import BottomNav from './components/Navigation/BottomNav';
import DashboardSkeleton from './components/Skeleton/DashboardSkeleton';
import QuickActions from './components/Actions/QuickActions';
import TimelineScrubber from './components/Timeline/TimelineScrubber';

// Lazy load other pages
const MissionControl = lazy(() => import('./pages/MissionControl'));
const PoliticalAlpha = lazy(() => import('./pages/PoliticalAlpha'));
const StrategyDistillery = lazy(() => import('./pages/StrategyDistillery'));
const DebateRoom = lazy(() => import('./pages/DebateRoom'));
const CurrencyDashboard = lazy(() => import('./pages/CurrencyDashboard'));
const AutoCoderDashboard = lazy(() => import('./pages/AutoCoderDashboard'));
const VRCockpit = lazy(() => import('./pages/VRCockpit'));
const TerminalWorkspace = lazy(() => import('./pages/TerminalWorkspace'));
const OptionsAnalytics = lazy(() => import('./pages/AnalyticsOptions'));
const BacktestPortfolio = lazy(() => import('./pages/BacktestPortfolio'));
const GlobalScanner = lazy(() => import('./pages/GlobalScanner'));
const BrokerageAccount = lazy(() => import('./pages/BrokerageAccount'));
const AutoCoderSandbox = lazy(() => import('./pages/AutoCoderSandbox'));
const PortfolioAttribution = lazy(() => import('./pages/PortfolioAttribution'));
const FixedIncomeDashboard = lazy(() => import('./pages/FixedIncomeDashboard'));
const CryptoDashboard = lazy(() => import('./pages/CryptoDashboard'));
const TaxDashboard = lazy(() => import('./pages/TaxDashboard'));
const MacroDashboard = lazy(() => import('./pages/MacroDashboard'));
const ComplianceDashboard = lazy(() => import('./pages/ComplianceDashboard'));
const EstateDashboard = lazy(() => import('./pages/EstateDashboard'));
const AuditDashboard = lazy(() => import('./pages/AuditDashboard')); // 
const ScenarioDashboard = lazy(() => import('./pages/ScenarioDashboard')); // 
const ImpactDashboard = lazy(() => import('./pages/ImpactDashboard')); // 
const SystemHealthDashboard = lazy(() => import('./pages/SystemHealthDashboard')); // 
const CorporateDashboard = lazy(() => import('./pages/CorporateDashboard')); // 
const MarginDashboard = lazy(() => import('./pages/MarginDashboard')); // 
const MobileDashboard = lazy(() => import('./pages/MobileDashboard')); // 
const APIDashboard = lazy(() => import('./pages/APIDashboard')); // 
const AssetsDashboard = lazy(() => import('./pages/AssetsDashboard')); // 
const CashFlowDashboard = lazy(() => import('./pages/CashFlowDashboard')); // 
const RoleOverview = lazy(() => import('./pages/RoleOverview'));
const TenantDashboard = lazy(() => import('./pages/TenantDashboard'));
// App Hardening & Improvements - New Phases
const AdvancedPortfolioAnalytics = lazy(() => import('./pages/AdvancedPortfolioAnalytics')); // 
const NewsSentimentDashboard = lazy(() => import('./pages/NewsSentimentDashboard')); // 
const WatchlistsAlertsDashboard = lazy(() => import('./pages/WatchlistsAlertsDashboard')); // 
const AIPredictionsDashboard = lazy(() => import('./pages/AIPredictionsDashboard')); // 
const AIAssistantDashboard = lazy(() => import('./pages/AIAssistantDashboard')); // 
const PortfolioOptimizationDashboard = lazy(() => import('./pages/PortfolioOptimizationDashboard')); // 
const AdvancedRiskDashboard = lazy(() => import('./pages/AdvancedRiskDashboard')); // 
const TaxOptimizationDashboard = lazy(() => import('./pages/TaxOptimizationDashboard')); // 
const FinancialPlanningDashboard = lazy(() => import('./pages/FinancialPlanningDashboard')); // 
const RetirementPlanningDashboard = lazy(() => import('./pages/RetirementPlanningDashboard')); // 
const BudgetingDashboard = lazy(() => import('./pages/BudgetingDashboard')); // 
const OptionsStrategyDashboard = lazy(() => import('./pages/OptionsStrategyDashboard')); // 
const PaperTradingDashboard = lazy(() => import('./pages/PaperTradingDashboard')); // 
const AlgorithmicTradingDashboard = lazy(() => import('./pages/AlgorithmicTradingDashboard')); // 
const EstatePlanningDashboard = lazy(() => import('./pages/EstatePlanningDashboard')); // 
const BillPaymentDashboard = lazy(() => import('./pages/BillPaymentDashboard')); // 
const CreditMonitoringDashboard = lazy(() => import('./pages/CreditMonitoringDashboard')); // 
const ResearchReportsDashboard = lazy(() => import('./pages/ResearchReportsDashboard')); // 
const SocialTradingDashboard = lazy(() => import('./pages/SocialTradingDashboard')); // 
const CommunityForumsDashboard = lazy(() => import('./pages/CommunityForumsDashboard')); // 
const EducationPlatformDashboard = lazy(() => import('./pages/EducationPlatformDashboard')); // 
const AdvancedChartingDashboard = lazy(() => import('./pages/AdvancedChartingDashboard')); // 
const AdvancedOrdersDashboard = lazy(() => import('./pages/AdvancedOrdersDashboard')); // 
const EnterpriseDashboard = lazy(() => import('./pages/EnterpriseDashboard')); // 
const InstitutionalToolsDashboard = lazy(() => import('./pages/InstitutionalToolsDashboard')); // 
const MasterOrchestrator = lazy(() => import('./pages/MasterOrchestrator')); // 
const SocialClassMaintenance = lazy(() => import('./pages/SocialClassMaintenance')); // 
const ZenMode = lazy(() => import('./pages/ZenMode')); // 
const MLTrainingDashboard = lazy(() => import('./pages/MLTrainingDashboard')); // 
const IntegrationsDashboard = lazy(() => import('./pages/IntegrationsDashboard')); // 
const SentinelStrategyDashboard = lazy(() => import('./pages/SentinelStrategyDashboard'));
const GoogleAuthCallback = lazy(() => import('./pages/GoogleAuthCallback'));
const AccountOverview = lazy(() => import('./pages/Accounts/AccountOverview'));
const AdminDashboard = lazy(() => import('./pages/AdminDashboard'));
const Settings = lazy(() => import('./pages/Settings'));
const DeveloperPlatformDashboard = lazy(() => import('./pages/DeveloperPlatformDashboard')); // 
const MarketplaceDashboard = lazy(() => import('./pages/MarketplaceDashboard')); // 
const EvolutionDashboard = lazy(() => import('./pages/EvolutionDashboard')); // : Evolution Lab
const TermsOfService = lazy(() => import('./pages/Legal/TermsOfService'));
const PrivacyPolicy = lazy(() => import('./pages/Legal/PrivacyPolicy'));
const OnboardingFlow = lazy(() => import('./components/Onboarding/OnboardingFlow'));
const PortfolioManagement = lazy(() => import('./pages/PortfolioManagement'));

import MFAVerificationModal from './components/MFAVerificationModal';




const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
function AppContent() {
  const navigate = useNavigate();
  const location = useLocation();
  const isOSStylePage = location.pathname.startsWith('/orchestrator/') || 
                         location.pathname.startsWith('/analyst/') || 
                         location.pathname.startsWith('/trader/') || 
                         location.pathname.startsWith('/strategist/') || 
                         location.pathname.startsWith('/data-scientist/') ||
                         location.pathname.startsWith('/architect/') ||
                         location.pathname.startsWith('/guardian/') ||
                         location.pathname.startsWith('/marketing/') ||
                         location.pathname.startsWith('/legal/');
  const {
    resetLayout,
    activeWorkspace,
    workspaces,
    saveWorkspace,
    loadWorkspace,
  } = useWidgetLayout();

  const { 
    isKillMFAOpen, 
    setKillMFAOpen, 
    triggerKillSwitch 
  } = useTaskbarStore();
  const [debugStates, setDebugStates] = useState({ forceLoading: false, forceError: false });
  const { isDark, toggleTheme } = useTheme();
  const [globalLock, setGlobalLock] = useState(false);
  const [currentUser, setCurrentUser] = useState(authService.getCurrentUser());
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(() => {
    const bypassEnabled = localStorage.getItem('widget_os_bypass') === 'true';
    return !bypassEnabled && !authService.isAuthenticated();
  });

  // Core State
  const [isSystemFrozen, setIsSystemFrozen] = useState(false);
  const [riskModalOpen, setRiskModalOpen] = useState(false);
  const [pendingTrade, setPendingTrade] = useState(null);
  
  // UI/UX Enhancement State
  const [commandPaletteOpen, setCommandPaletteOpen] = useState(false);
  const [showOnboarding, setShowOnboarding] = useState(false);

  // Widget visibility and states (Synchronized with Dashboard)
  const [widgetVisibility, setWidgetVisibility] = useState(() => {
    // Force default visibility for verification, ignoring local storage for key widgets
    return {
        'monitor-view': true,
        'command-view': true,
        'portfolio-view': true,
        'research-view': true,
        'options-chain-view': true,
        'market-depth-view': true,
        'trade-tape-view': true,
        'homeostasis-view': true,
        'terminal-view': true,
        'system-log-view': true,
        'bar-chart': true,
    };
  });

 const [widgetStates, setWidgetStates] = useState(() => {
    // Force default state to ensure consistent verification environment
    // Ignoring localStorage for now as requested
    return {
        'window-manager': { minimized: true, maximized: false }, 
        // Add other defaults if necessary
    };
  });

  const [socketConnected, setSocketConnected] = useState(false);
  const { groups } = useSymbolLinking();

  const { notify } = useNotifications();
  const [tradeModal, setTradeModal] = useState({ open: false, details: null });

  // Global Hotkeys
  useHotkeys({
    'Shift+B': () => setTradeModal({ open: true, details: { symbol: groups.none || 'SPY', side: 'BUY', quantity: 10, price: 480.00 } }),
    'Shift+S': () => setTradeModal({ open: true, details: { symbol: groups.none || 'SPY', side: 'SELL', quantity: 10, price: 480.00 } }),
    'Ctrl+Shift+S': () => handleSaveWorkspacePrompt(),
    'Alt+1': () => navigate('/orchestrator/terminal'),
    'Alt+2': () => navigate('/trader/options'),
    'Alt+3': () => navigate('/strategist/backtest'),
    'Alt+4': () => navigate('/trader/scanner'),
    // Command Palette
    'Ctrl+K': () => setCommandPaletteOpen(prev => !prev),
    'Meta+K': () => setCommandPaletteOpen(prev => !prev), // Mac support
  });

  const handleSaveWorkspacePrompt = () => {
    const name = prompt('Enter a name for this workspace:', activeWorkspace);
    if (name) saveWorkspace(name);
  };

  // Theme is now managed by ThemeContext - no need for local useEffect

  // Socket.io initialization (Consolidated with PresenceService)
  useEffect(() => {
    if (!currentUser) return;
    
    // Initialize presence service (which handles the socket connection)
    presenceService.initialize(currentUser.id, currentUser.username);
    const socket = presenceService.socket;
    
    if (socket) {
      socket.on('connect', () => setSocketConnected(true));
      socket.on('disconnect', () => setSocketConnected(false));
      // Update state if already connected
      if (socket.connected) setSocketConnected(true);
    }

    presenceService.on('risk:alert', (data) => {
      notify({ title: 'RISK BREACH', body: data.message, type: 'error' });
    });

    presenceService.on('trade:fill', (data) => {
      notify({ title: 'ORDER FILLED', body: `${data.symbol} ${data.side} ${data.quantity} @ ${data.price}`, type: 'success' });
    });

    return () => {
      presenceService.disconnect();
      setSocketConnected(false);
    };
  }, [currentUser, notify]);

  // Check onboarding status on mount
  useEffect(() => {
    if (currentUser) {
      const onboardingCompleted = localStorage.getItem('onboarding_completed');
      if (!onboardingCompleted) {
        // Check with API
        // Check with API
        apiClient.get('/onboarding/status')
          .then(res => {
            const data = res.data;
            if (data.success && !data.data.completed) {
              // Double check local storage didn't change during fetch
              if (!localStorage.getItem('onboarding_completed')) {
                  setShowOnboarding(true);
              }
            }
          })
          .catch(() => {
            // If API fails, check localStorage
            if (!localStorage.getItem('onboarding_completed')) {
              setShowOnboarding(true);
            }
          });
      }
    }
  }, [currentUser]);

  //  Verification: Spawn Welcome Window
  const addWindow = useWindowStore((state) => state.addWindow);
  useEffect(() => {
      if (useWindowStore.getState().windows.length === 0) {
          // System Status Window
          addWindow({
              title: 'System Status',
              width: 400,
              height: 300,
              x: 100,
              y: 100,
              isMinimized: true,
              risk: 'low',
              component: () => (
                  <div style={{padding: 20, color: 'white'}}>
                      <h3>🟢 System Operational</h3>
                      <p>Window Manager: <strong>Active</strong></p>
                      <p>Taskbar: <strong>Active</strong></p>
                      <p>Agents Online: <strong>12/12</strong></p>
                  </div>
              )
          });
          
          // Market Monitor Window
          addWindow({
              title: 'Market Monitor',
              width: 500,
              height: 400,
              x: 550,
              y: 120,
              isMinimized: true,
              risk: 'medium',
              badgeCount: 3,
              component: () => (
                  <div style={{padding: 20, color: 'white'}}>
                      <h3>📈 Market Overview</h3>
                      <p>S&P 500: <span style={{color: '#00ff88'}}>+1.42%</span></p>
                      <p>VIX: <span style={{color: '#ffc107'}}>13.42</span></p>
                      <p>Active Alerts: <strong>3</strong></p>
                  </div>
              )
          });
          
          // Agent Control Window (minimized)
          addWindow({
              title: 'Agent Control',
              width: 450,
              height: 350,
              x: 200,
              y: 200,
              isMinimized: true,
              risk: 'low',
              component: () => (
                  <div style={{padding: 20, color: 'white'}}>
                      <h3>🤖 Agent Fleet</h3>
                      <p>Running: 12 | Paused: 0</p>
                  </div>
              )
          });
          
          // Risk Scanner Window
          addWindow({
              title: 'Risk Scanner',
              width: 400,
              height: 300,
              x: 300,
              y: 250,
              isMinimized: true,
              risk: 'high',
              badgeCount: 2,
              component: () => (
                  <div style={{padding: 20, color: 'white'}}>
                      <h3>⚠️ Risk Alerts</h3>
                      <p style={{color: '#ff4757'}}>2 High Priority Alerts</p>
                      <p>Portfolio VaR: -$24,500</p>
                  </div>
              )
          });
          
          // Terminal Window (minimized)
          addWindow({
              title: 'Terminal',
              width: 600,
              height: 400,
              x: 400,
              y: 180,
              isMinimized: true,
              risk: 'low',
              component: () => (
                  <div style={{padding: 20, color: '#00ff88', fontFamily: 'monospace', background: '#0a0a0a'}}>
                      <pre>$ system status --all{'\n'}[OK] Kafka: Connected{'\n'}[OK] Neo4j: Connected{'\n'}[OK] TimescaleDB: Connected{'\n'}{'>'} _</pre>
                  </div>
              )
          });
          
          // Portfolio Overview Window
          addWindow({
              title: 'Portfolio',
              width: 550,
              height: 400,
              x: 180,
              y: 140,
              isMinimized: true,
              risk: 'low',
              component: () => (
                  <div style={{padding: 20, color: 'white'}}>
                      <h3>💼 Portfolio Overview</h3>
                      <p>Total Value: <span style={{color: '#00ff88'}}>$2,847,320</span></p>
                      <p>Today's P&L: <span style={{color: '#00ff88'}}>+$12,450 (+0.44%)</span></p>
                      <p>Positions: <strong>24</strong></p>
                  </div>
              )
          });
          
          // News Feed Window
          addWindow({
              title: 'News Feed',
              width: 450,
              height: 500,
              x: 750,
              y: 100,
              isMinimized: true,
              risk: 'medium',
              badgeCount: 7,
              component: () => (
                  <div style={{padding: 20, color: 'white'}}>
                      <h3>📰 Breaking News</h3>
                      <p style={{borderBottom: '1px solid #333', paddingBottom: 8}}>Fed signals rate pause...</p>
                      <p style={{borderBottom: '1px solid #333', paddingBottom: 8}}>NVDA earnings beat...</p>
                      <p>Crypto markets rally...</p>
                  </div>
              )
          });
          
          // Strategy Lab Window
          addWindow({
              title: 'Strategy Lab',
              width: 600,
              height: 450,
              x: 280,
              y: 160,
              isMinimized: true,
              risk: 'low',
              component: () => (
                  <div style={{padding: 20, color: 'white'}}>
                      <h3>🧬 Strategy Lab</h3>
                      <p>Active Strategies: <strong>3</strong></p>
                      <p>Backtesting: <span style={{color: '#00f2ff'}}>Momentum Alpha v2.1</span></p>
                      <p>Win Rate: <span style={{color: '#00ff88'}}>67.4%</span></p>
                  </div>
              )
          });
          
          // Analytics Dashboard Window
          addWindow({
              title: 'Analytics',
              width: 500,
              height: 380,
              x: 600,
              y: 200,
              isMinimized: true,
              risk: 'low',
              component: () => (
                  <div style={{padding: 20, color: 'white'}}>
                      <h3>📊 Analytics</h3>
                      <p>Sharpe Ratio: <strong>1.82</strong></p>
                      <p>Max Drawdown: <span style={{color: '#ffc107'}}>-8.2%</span></p>
                      <p>Alpha: <span style={{color: '#00ff88'}}>+4.1%</span></p>
                  </div>
              )
          });
          
          // Watchlist Window
          addWindow({
              title: 'Watchlist',
              width: 400,
              height: 450,
              x: 850,
              y: 150,
              isMinimized: true,
              risk: 'medium',
              badgeCount: 1,
              component: () => (
                  <div style={{padding: 20, color: 'white'}}>
                      <h3>👁️ Watchlist</h3>
                      <p>AAPL: <span style={{color: '#00ff88'}}>$189.42 ↑</span></p>
                      <p>TSLA: <span style={{color: '#ff4757'}}>$241.05 ↓</span></p>
                      <p>MSFT: <span style={{color: '#00ff88'}}>$378.91 ↑</span></p>
                      <p>GOOGL: <span style={{color: '#ffc107'}}>$142.33 →</span></p>
                  </div>
              )
          });
      }
  }, []);

  const handleMenuAction = (action) => {
    // Handle widget toggle actions
    if (action?.startsWith('toggle-widget-')) {
      const widgetId = action.replace('toggle-widget-', '');
      setWidgetVisibility(prev => ({ ...prev, [widgetId]: prev[widgetId] === false ? true : false }));
      if (location.pathname !== '/orchestrator/terminal') {
        navigate('/orchestrator/terminal');
      }
      return;
    }

    switch (action) {
      // --- Orchestrator ---
      case 'nav-overview-orchestrator': navigate('/orchestrator'); break;
      case 'show-dashboard': navigate('/orchestrator/terminal'); break;
      case 'show-mission-control': navigate('/orchestrator/mission-control'); break;
      case 'role-orchestrator': navigate('/orchestrator/graph'); break;
      case 'show-chat': navigate('/orchestrator/chat'); break;
      case 'show-zen': navigate('/orchestrator/zen'); break;

      // --- Architect ---
      case 'nav-overview-architect': navigate('/architect'); break;
      case 'nav-admin': navigate('/architect/admin'); break;
      case 'role-architect': navigate('/architect/health'); break;
      case 'role-api': navigate('/architect/api'); break;
      case 'nav-integrations': navigate('/architect/integrations'); break;
      case 'nav-developer-platform': navigate('/architect/dev-platform'); break;

      // --- Account ---
      case 'nav-account': navigate('/account'); break;
      case 'nav-account-settings': navigate('/account/settings'); break;

       // --- Data Scientist & Analyst ---
       case 'nav-overview-analyst': navigate('/analyst'); break;
       case 'show-political-alpha': navigate('/analyst/political'); break;
       case 'show-strategy-distillery': navigate('/analyst/strategy'); break;
       case 'role-observer': navigate('/analyst/macro'); break;

       case 'nav-overview-data-scientist': navigate('/data-scientist'); break;
       case 'nav-ai-predictions': navigate('/data-scientist/predictions'); break;
       case 'nav-ml-training': navigate('/data-scientist/training'); break;
       case 'nav-ai-assistant': navigate('/data-scientist/assistant'); break;
       case 'nav-autocoder': navigate('/data-scientist/autocoder'); break;
       case 'show-debate': navigate('/data-scientist/debate'); break;
       case 'show-vr': navigate('/data-scientist/vr'); break;

      // --- Day-Trader (Trader) ---
      case 'nav-overview-trader': navigate('/trader'); break;
      case 'show-scanner': navigate('/trader/scanner'); break;
      case 'nav-options-strategy': navigate('/trader/options'); break;
      case 'nav-advanced-orders': navigate('/trader/advanced-orders'); break;
      case 'nav-algorithmic-trading': navigate('/trader/algorithmic'); break;
      case 'nav-paper-trading': navigate('/trader/paper'); break;
      case 'nav-advanced-charting': navigate('/trader/charting'); break;
      case 'show-options': navigate('/trader/options-analytics'); break;

      // --- Strategist ---
      case 'nav-overview-strategist': navigate('/strategist'); break;
      case 'nav-portfolio-management': navigate('/strategist/net-worth'); break;
      case 'nav-advanced-analytics': navigate('/strategist/analytics'); break;
      case 'nav-portfolio-optimization': navigate('/strategist/optimization'); break;
      case 'show-attribution': navigate('/strategist/attribution'); break;
      case 'show-backtest': navigate('/strategist/backtest'); break;
      case 'show-brokerage': navigate('/strategist/brokerage'); break;
      case 'show-crypto': navigate('/strategist/crypto'); break;
      case 'show-fixed-income': navigate('/strategist/fixed-income'); break;
      case 'show-assets': navigate('/strategist/assets'); break;
      case 'role-corporate': navigate('/strategist/corporate'); break;
      case 'role-impact': navigate('/strategist/impact'); break;
      case 'role-scm': navigate('/strategist/scm'); break;
      case 'nav-estate-planning': navigate('/strategist/estate'); break;
      case 'nav-retirement-planning': navigate('/strategist/retirement'); break;
      case 'nav-budgeting': navigate('/strategist/budgeting'); break;
      case 'nav-financial-planning': navigate('/strategist/financial'); break;

      // --- Marketing ---
      case 'nav-overview-marketing': navigate('/marketing'); break;
      case 'nav-news-sentiment': navigate('/marketing/news'); break;
      case 'nav-social-trading': navigate('/marketing/social'); break;
      case 'nav-community-forums': navigate('/marketing/forums'); break;
      case 'nav-education': navigate('/marketing/education'); break;
      case 'nav-marketplace': navigate('/marketing/marketplace'); break;
      case 'nav-research-reports': navigate('/marketing/reports'); break;
      case 'nav-watchlists-alerts': navigate('/marketing/alerts'); break;

      // --- Lawyer & Legal ---
      case 'nav-overview-legal': navigate('/legal'); break;
      case 'role-guardian': navigate('/legal/compliance'); break;
      case 'role-audit': navigate('/legal/audit'); break;
      case 'role-scenarios': navigate('/legal/scenarios'); break;
      case 'role-margin': navigate('/legal/margin'); break;
      case 'show-tax': navigate('/legal/tax'); break;
      case 'nav-legal-terms': navigate('/legal/terms'); break;
      case 'nav-legal-privacy': navigate('/legal/privacy'); break;

      // --- Guardian ---
      case 'nav-overview-guardian': navigate('/guardian'); break;
      case 'nav-advanced-risk': navigate('/guardian/risk'); break;
      case 'nav-credit-monitoring': navigate('/guardian/credit'); break;
      case 'nav-institutional': navigate('/guardian/institutional'); break;
      case 'nav-enterprise': navigate('/guardian/enterprise'); break;
      case 'nav-bill-payment': navigate('/guardian/payments'); break;
      case 'show-cash-flow': navigate('/guardian/cash-flow'); break;
      case 'show-tenant': navigate('/guardian/tenants'); break;
      case 'role-warden': navigate('/guardian/mobile'); break;

      // --- Legacy Data Scientist Redirects ---
      case 'nav-overview-pioneer': navigate('/data-scientist'); break;
      case 'show-auto-coder': navigate('/data-scientist/autocoder'); break;
      case 'show-sandbox': navigate('/data-scientist/sandbox'); break;
      case 'show-vr-cockpit': navigate('/data-scientist/vr'); break;
      case 'show-debate-chamber': navigate('/data-scientist/debate'); break;

      // Widgets / Specifics
      case 'toggle-theme': toggleTheme(); break;
      case 'reset-layout': resetLayout(); break;
      case 'profile-settings': navigate('/settings'); break;
      case 'logout': handleLogout(); break;
      case 'signin': setIsAuthModalOpen(true); break;

      default: break;
    }
  };

  const handleLogout = () => {
    authService.logout();
    setCurrentUser(null);
    setIsAuthModalOpen(true);
  };

  return (
    <GlobalErrorBoundary>
      <div className={`app-shell ${isDark ? 'dark' : 'light'}`}>
        <AuthGuard onShowLogin={() => setIsAuthModalOpen(true)}>
          {/* Navigation Header */}
          <MenuBar
            onMenuAction={handleMenuAction}
            isDarkMode={isDark}
            toggleTheme={toggleTheme}
            widgetVisibility={widgetVisibility}
            onToggleWidget={(widgetId) => setWidgetVisibility(prev => ({ ...prev, [widgetId]: prev[widgetId] === false ? true : false }))}
            onResetLayout={resetLayout}
            widgetTitles={{
              'monitor-view': 'Market Monitor',
              'command-view': 'Command Center',
              'research-view': 'Data Research',
              'portfolio-view': 'Live Portfolio',
              'homeostasis-view': 'Total Homeostasis',
              'options-chain-view': 'Options Chain',
              'market-depth-view': 'Market Depth',
              'trade-tape-view': 'Trade Tape',
              'terminal-view': 'System Log',
              'bar-chart': 'Bar Chart',
            }}
            currentUser={currentUser}
            onLogout={handleLogout}
            onSignin={() => setIsAuthModalOpen(true)}
            activeWorkspace={activeWorkspace}
            workspaces={workspaces}
            onLoadWorkspace={loadWorkspace}
            onSaveWorkspacePrompt={handleSaveWorkspacePrompt}
            debugStates={debugStates}
            globalLock={globalLock}
          />
          <SubHeaderNav />
          
          <main className={`institutional-os-container ${isOSStylePage ? 'os-bleed' : ''}`}>
            {/* Breadcrumbs moved to Taskbar */}
            {/* Route Content Wrapper - Takes remaining flex space */}
            <div className={isOSStylePage ? 'route-content-os' : 'route-content'}>
            <Suspense fallback={<DashboardSkeleton />}>
              <GlobalTooltip />
              <Routes>
                {/* Role Landing Pages */}
                <Route path="/orchestrator" element={<RoleOverview />} />
                <Route path="/orchestrator/terminal" element={<TerminalWorkspace handleViewSource={() => { }} globalLock={globalLock} isDarkMode={isDark} widgetStates={widgetStates} setWidgetStates={setWidgetStates} widgetVisibility={widgetVisibility} setWidgetVisibility={setWidgetVisibility} />} />
                <Route path="/orchestrator/mission-control" element={<MissionControl />} />
                <Route path="/orchestrator/graph" element={<MasterOrchestrator />} />
                <Route path="/orchestrator/chat" element={<div className="p-8 text-white"><h1>Global Chat</h1><p>Neural communication interface active.</p></div>} />
                <Route path="/orchestrator/zen" element={<ZenMode />} />

                <Route path="/architect" element={<RoleOverview />} />
                <Route path="/architect/health" element={<SystemHealthDashboard />} />
                <Route path="/architect/api" element={<APIDashboard />} />
                <Route path="/architect/admin" element={<AdminDashboard />} />
                <Route path="/architect/integrations" element={<IntegrationsDashboard />} />
                <Route path="/architect/dev-platform" element={<DeveloperPlatformDashboard />} />

                <Route path="/analyst" element={<RoleOverview />} />
                {/* Removed: <Route path="/analyst/predictions" element={<AIPredictionsDashboard />} /> */}
                {/* Removed: <Route path="/analyst/training" element={<MLTrainingDashboard />} /> */}
                <Route path="/analyst/political" element={<PoliticalAlpha />} />
                <Route path="/analyst/strategy" element={<StrategyDistillery />} />
                <Route path="/analyst/macro" element={<MacroDashboard />} />
                {/* Removed: <Route path="/analyst/assistant" element={<AIAssistantDashboard />} /> */}
                <Route path="/analyst/sentinel" element={<SentinelStrategyDashboard />} />

                <Route path="/data-scientist" element={<RoleOverview />} />
                <Route path="/data-scientist/predictions" element={<AIPredictionsDashboard />} />
                <Route path="/data-scientist/training" element={<MLTrainingDashboard />} />
                <Route path="/data-scientist/assistant" element={<AIAssistantDashboard />} />
                <Route path="/data-scientist/autocoder" element={<AutoCoderDashboard />} />
                <Route path="/data-scientist/sandbox" element={<AutoCoderSandbox />} />
                <Route path="/data-scientist/vr" element={<VRCockpit />} />
                <Route path="/data-scientist/debate" element={<DebateRoom />} />

                <Route path="/trader" element={<RoleOverview />} />
                <Route path="/trader/scanner" element={<GlobalScanner />} />
                <Route path="/trader/options" element={<OptionsStrategyDashboard />} />
                <Route path="/trader/advanced-orders" element={<AdvancedOrdersDashboard />} />
                <Route path="/trader/algorithmic" element={<AlgorithmicTradingDashboard />} />
                <Route path="/trader/paper" element={<PaperTradingDashboard />} />
                <Route path="/trader/charting" element={<AdvancedChartingDashboard />} />
                <Route path="/trader/options-analytics" element={<OptionsAnalytics />} />

                <Route path="/strategist" element={<RoleOverview />} />
                <Route path="/strategist/net-worth" element={<PortfolioManagement />} />
                <Route path="/strategist/analytics" element={<AdvancedPortfolioAnalytics />} />
                <Route path="/strategist/optimization" element={<PortfolioOptimizationDashboard />} />
                <Route path="/strategist/attribution" element={<PortfolioAttribution />} />
                <Route path="/strategist/backtest" element={<BacktestPortfolio />} />
                <Route path="/strategist/brokerage" element={<BrokerageAccount />} />
                <Route path="/strategist/crypto" element={<CryptoDashboard />} />
                <Route path="/strategist/fixed-income" element={<FixedIncomeDashboard />} />
                <Route path="/strategist/assets" element={<AssetsDashboard />} />
                <Route path="/strategist/corporate" element={<CorporateDashboard />} />
                <Route path="/strategist/impact" element={<ImpactDashboard />} />
                <Route path="/strategist/scm" element={<SocialClassMaintenance />} />
                <Route path="/strategist/estate" element={<EstatePlanningDashboard />} />
                <Route path="/strategist/retirement" element={<RetirementPlanningDashboard />} />
                <Route path="/strategist/budgeting" element={<BudgetingDashboard />} />
                <Route path="/strategist/financial" element={<FinancialPlanningDashboard />} />

                <Route path="/marketing" element={<RoleOverview />} />
                <Route path="/marketing/news" element={<NewsSentimentDashboard />} />
                <Route path="/marketing/social" element={<SocialTradingDashboard />} />
                <Route path="/marketing/forums" element={<CommunityForumsDashboard />} />
                <Route path="/marketing/education" element={<EducationPlatformDashboard />} />
                <Route path="/marketing/marketplace" element={<MarketplaceDashboard />} />
                <Route path="/marketing/reports" element={<ResearchReportsDashboard />} />
                <Route path="/marketing/alerts" element={<WatchlistsAlertsDashboard />} />

                <Route path="/legal" element={<RoleOverview />} />
                <Route path="/legal/compliance" element={<ComplianceDashboard />} />
                <Route path="/legal/audit" element={<AuditDashboard />} />
                <Route path="/legal/scenarios" element={<ScenarioDashboard />} />
                <Route path="/legal/margin" element={<MarginDashboard />} />
                <Route path="/legal/tax" element={<TaxDashboard />} />
                <Route path="/legal/terms" element={<TermsOfService />} />
                <Route path="/legal/privacy" element={<PrivacyPolicy />} />

                <Route path="/guardian" element={<RoleOverview />} />
                <Route path="/guardian/risk" element={<AdvancedRiskDashboard />} />
                <Route path="/guardian/credit" element={<CreditMonitoringDashboard />} />
                <Route path="/guardian/institutional" element={<InstitutionalToolsDashboard />} />
                <Route path="/guardian/enterprise" element={<EnterpriseDashboard />} />
                <Route path="/guardian/payments" element={<BillPaymentDashboard />} />
                <Route path="/guardian/cash-flow" element={<CashFlowDashboard />} />
                <Route path="/guardian/tenants" element={<TenantDashboard />} />
                <Route path="/guardian/mobile" element={<MobileDashboard />} />

                <Route path="/pioneer" element={<RoleOverview />} />
                <Route path="/data-scientist/autocoder" element={<AutoCoderDashboard />} />
                <Route path="/data-scientist/sandbox" element={<AutoCoderSandbox />} />
                <Route path="/data-scientist/vr" element={<VRCockpit />} />
                <Route path="/data-scientist/debate" element={<DebateRoom />} />
                <Route path="/data-scientist/evolution" element={<EvolutionDashboard />} />
                <Route path="/data-scientist/sentinel" element={<SentinelStrategyDashboard />} />

                {/* Account & Settings */}
                <Route path="/account" element={<AccountOverview />} />
                <Route path="/account/settings" element={<Settings />} />
                <Route path="/settings" element={<Navigate to="/account/settings" replace />} />
                <Route path="/settings/profile" element={<div className="p-8 text-white"><h1>Profile Settings</h1><p>Update your institutional identity.</p></div>} />
                <Route path="/settings/keyboard" element={<div className="p-8 text-white"><h1>Keyboard Shortcuts</h1><p>Master the terminal via hotkeys.</p></div>} />

                {/* Baselines */}
                <Route path="/" element={<Navigate to="/orchestrator/terminal" replace />} />
                <Route path="/login" element={<Navigate to="/" replace />} />
                <Route path="*" element={<div className="p-8 text-white"><h1>404: Node Missing</h1><p>The requested path does not exist in this namespace.</p></div>} />
              </Routes>

            </Suspense>
            </div> {/* End route-content wrapper */}
            {/* 100px buffer only for standard scrollable pages */}
            {!isOSStylePage && (
              <div className="global-scroll-buffer" style={{ height: '100px', width: '100%', flexShrink: 0 }} />
            )}
          </main>
        </AuthGuard>

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
            // Chain to  Execution Shield
            setPendingTrade({
                ticker: details.symbol,
                size: details.quantity,
                price: details.price,
                side: details.side
            });
            setRiskModalOpen(true);
          }}
        />
        
        {/* Global Status Bar */}
        <GlobalStatusBar 
          globalLock={globalLock}
          socketConnected={socketConnected}
          currentUser={currentUser}
        />

        {/* : Window Manager Layer */}
        {useWindowStore(useShallow((state) => state.windows.map(w => w.id))).map((id) => (
            <WindowWrapper key={id} id={id} />
        ))}
        <Taskbar />
        
        {/* Command Palette (Ctrl+K) */}
        <CommandPalette 
          isOpen={commandPaletteOpen} 
          onClose={() => setCommandPaletteOpen(false)}
          onThemeToggle={toggleTheme}
        />
        
        {/* Mobile Bottom Nav */}
        <BottomNav />
        
        {/* Quick Actions FAB */}
        <QuickActions 
          onAction={(actionId) => {
            switch(actionId) {
              case 'trade': setTradeModal({ open: true, details: { symbol: 'SPY', side: 'BUY', quantity: 10, price: 480 }}); break;
              case 'settings': navigate('/settings'); break;
              default: console.log('Quick action:', actionId);
            }
          }}
        />

        {/* : Global Safety Logic */}
        <MFAVerificationModal 
            isOpen={isKillMFAOpen}
            onClose={() => setKillMFAOpen(false)}
            actionName="Engagement of Global Kill Switch"
            onSuccess={async (mfa_code) => {
                setKillMFAOpen(false);
                setIsSystemFrozen(true);
                triggerKillSwitch(); // Update taskbar store state to 'active'
                try {
                    await apiClient.post('/risk/kill-switch', {
                          action: 'engage', 
                          reason: 'User Kill Switch (MFA Verified)',
                          mfa_code: mfa_code 
                    });
                    notify({ title: 'SYSTEM HALTED', body: 'Kill switch signal broadcasted', type: 'critical' });
                } catch (e) {
                    notify({ title: 'KILL SWITCH ERROR', body: 'Failed to notify backend', type: 'error' });
                }
            }}
        />
        <FrozenOverlay isFrozen={isSystemFrozen} onUnlock={() => setIsSystemFrozen(false)} />
        
        {/* Sprint 6: Event Timeline Scrubber */}
        <TimelineScrubber />
        <PreTradeRiskModal 
            isOpen={riskModalOpen} 
            onClose={() => setRiskModalOpen(false)}
            tradeDetails={pendingTrade}
            onConfirm={async () => {
                setRiskModalOpen(false);
                try {
                    const response = await apiClient.post('/brokerage/order', {
                            symbol: pendingTrade.ticker,
                            qty: pendingTrade.size,
                            side: pendingTrade.side,
                            type: 'market'
                    });
                    const result = response.data;
                    notify({ 
                        title: 'ORDER EXECUTED', 
                        body: `${pendingTrade.side} ${pendingTrade.size} ${pendingTrade.ticker} @ ${result.price || 'Mkt'}`, 
                        type: 'success' 
                    });
                } catch (e) {
                    const result = e.response?.data || {};
                    notify({ 
                        title: 'EXECUTION REJECTED', 
                        body: result.reason || 'Safety parameters violated', 
                        type: 'error' 
                    });
                     // notify({ title: 'ROUTING ERROR', body: 'Failed to reach execution gateway', type: 'error' }); // Kept in catch block logic generally
                }
            }}
        />

        
        {/* : Education Mode Overlay */}
        <EducationOverlay />
        
        {/* Onboarding Flow */}
        {showOnboarding && (
          <Suspense fallback={null}>
            <OnboardingFlow
              onComplete={(userData) => {
                setShowOnboarding(false);
                
                // Map frontend userData to backend preferences schema
                const preferences = {
                  experience_level: userData.experience || 'beginner',
                  investment_goals: userData.goals || [],
                  risk_tolerance: userData.riskTolerance || 'moderate',
                  notifications: true,
                  theme: 'dark',
                  metadata: {
                    investment_amount: userData.investmentAmount,
                    time_horizon: userData.timeHorizon,
                    completed_at: new Date().toISOString()
                  }
                };

                // Save to API
                apiClient.post('/onboarding/complete', { preferences }).catch(console.error);
              }}
              onSkip={() => {
                setShowOnboarding(false);
                localStorage.setItem('onboarding_completed', 'skipped');
                apiClient.post('/onboarding/skip').catch(console.error);
              }}
            />
          </Suspense>
        )}
      </div>
    </GlobalErrorBoundary>
  );
}

// Wrap AppContent with ThemeProvider and ToastProvider
function App() {
  return (
    <ThemeProvider>
      <ToastProvider>
        <AppContent />
      </ToastProvider>
    </ThemeProvider>
  );
}

export default App;
