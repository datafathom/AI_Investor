
import React, { useEffect, useState, useRef, Suspense, lazy } from 'react';
import { useColorPalette } from './hooks/useColorPalette';
import { useWidgetLayout } from './hooks/useWidgetLayout';
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
import Taskbar from './components/Taskbar/Taskbar';

// Phase 5: Risk & Safety
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
const AuditDashboard = lazy(() => import('./pages/AuditDashboard')); // Phase 16
const ScenarioDashboard = lazy(() => import('./pages/ScenarioDashboard')); // Phase 17
const ImpactDashboard = lazy(() => import('./pages/ImpactDashboard')); // Phase 18
const SystemHealthDashboard = lazy(() => import('./pages/SystemHealthDashboard')); // Phase 19
const CorporateDashboard = lazy(() => import('./pages/CorporateDashboard')); // Phase 20
const MarginDashboard = lazy(() => import('./pages/MarginDashboard')); // Phase 21
const MobileDashboard = lazy(() => import('./pages/MobileDashboard')); // Phase 22
const APIDashboard = lazy(() => import('./pages/APIDashboard')); // Phase 23
const AssetsDashboard = lazy(() => import('./pages/AssetsDashboard')); // Phase 24
const ZenMode = lazy(() => import('./pages/ZenMode')); // Phase 24 (Zen)
const CashFlowDashboard = lazy(() => import('./pages/CashFlowDashboard')); // Phase 10
const RoleOverview = lazy(() => import('./pages/RoleOverview'));
const TenantDashboard = lazy(() => import('./pages/TenantDashboard'));
// App Hardening & Improvements - New Phases
const AdvancedPortfolioAnalytics = lazy(() => import('./pages/AdvancedPortfolioAnalytics')); // Phase 1
const NewsSentimentDashboard = lazy(() => import('./pages/NewsSentimentDashboard')); // Phase 16
const WatchlistsAlertsDashboard = lazy(() => import('./pages/WatchlistsAlertsDashboard')); // Phase 17
const AIPredictionsDashboard = lazy(() => import('./pages/AIPredictionsDashboard')); // Phase 25
const AIAssistantDashboard = lazy(() => import('./pages/AIAssistantDashboard')); // Phase 26
const PortfolioOptimizationDashboard = lazy(() => import('./pages/PortfolioOptimizationDashboard')); // Phase 2
const AdvancedRiskDashboard = lazy(() => import('./pages/AdvancedRiskDashboard')); // Phase 3
const TaxOptimizationDashboard = lazy(() => import('./pages/TaxOptimizationDashboard')); // Phase 4
const FinancialPlanningDashboard = lazy(() => import('./pages/FinancialPlanningDashboard')); // Phase 7
const RetirementPlanningDashboard = lazy(() => import('./pages/RetirementPlanningDashboard')); // Phase 8
const BudgetingDashboard = lazy(() => import('./pages/BudgetingDashboard')); // Phase 10
const OptionsStrategyDashboard = lazy(() => import('./pages/OptionsStrategyDashboard')); // Phase 6
const PaperTradingDashboard = lazy(() => import('./pages/PaperTradingDashboard')); // Phase 14
const AlgorithmicTradingDashboard = lazy(() => import('./pages/AlgorithmicTradingDashboard')); // Phase 15
const EstatePlanningDashboard = lazy(() => import('./pages/EstatePlanningDashboard')); // Phase 9
const BillPaymentDashboard = lazy(() => import('./pages/BillPaymentDashboard')); // Phase 11
const CreditMonitoringDashboard = lazy(() => import('./pages/CreditMonitoringDashboard')); // Phase 12
const ResearchReportsDashboard = lazy(() => import('./pages/ResearchReportsDashboard')); // Phase 18
const SocialTradingDashboard = lazy(() => import('./pages/SocialTradingDashboard')); // Phase 19
const CommunityForumsDashboard = lazy(() => import('./pages/CommunityForumsDashboard')); // Phase 20
const EducationPlatformDashboard = lazy(() => import('./pages/EducationPlatformDashboard')); // Phase 21
const AdvancedChartingDashboard = lazy(() => import('./pages/AdvancedChartingDashboard')); // Phase 5
const AdvancedOrdersDashboard = lazy(() => import('./pages/AdvancedOrdersDashboard')); // Phase 13
const EnterpriseDashboard = lazy(() => import('./pages/EnterpriseDashboard')); // Phase 31
const InstitutionalToolsDashboard = lazy(() => import('./pages/InstitutionalToolsDashboard')); // Phase 33
const MLTrainingDashboard = lazy(() => import('./pages/MLTrainingDashboard')); // Phase 27
const IntegrationsDashboard = lazy(() => import('./pages/IntegrationsDashboard')); // Phase 28
const DeveloperPlatformDashboard = lazy(() => import('./pages/DeveloperPlatformDashboard')); // Phase 29
const MarketplaceDashboard = lazy(() => import('./pages/MarketplaceDashboard')); // Phase 30
const TermsOfService = lazy(() => import('./pages/Legal/TermsOfService'));
const PrivacyPolicy = lazy(() => import('./pages/Legal/PrivacyPolicy'));
const OnboardingFlow = lazy(() => import('./components/Onboarding/OnboardingFlow'));

import MFAVerificationModal from './components/MFAVerificationModal';




const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
function AppContent() {
  const navigate = useNavigate();
  const location = useLocation();
  const isOSStylePage = [
    '/workspace/terminal', 
    '/zen', 
    '/analytics/political', 
    '/portfolio/advanced-analytics',
    '/trading/advanced-orders',
    '/portfolio/brokerage',
    '/portfolio/attribution',
    '/portfolio/fixed-income',
    '/portfolio/crypto',
    '/portfolio/optimization',
    '/planning/financial',
    '/planning/retirement',
    '/planning/estate',
    '/analytics/cashflow',
    '/planning/budgeting',
    '/billing/payments',
    '/portfolio/tax-optimization',
    '/portfolio/tax',
    '/trading/algorithmic',
    '/trading/options',
    '/trading/paper',
    '/analytics/political',
    '/analytics/strategy',
    '/workspace/debate',
    '/research/reports',
    '/workspace/mission-control',
    '/scanner/global',
    '/assets',
    '/tenant',
    '/portfolio/risk',
    '/credit/monitoring',
    '/architect/system',
    '/architect/api',
    '/mobile',
    '/workspace/autocoder',
    '/workspace/vr'
  ].includes(location.pathname);
  const {
    resetLayout,
    activeWorkspace,
    workspaces,
    saveWorkspace,
    loadWorkspace,
  } = useWidgetLayout();
  const [debugStates, setDebugStates] = useState({ forceLoading: false, forceError: false });
  const { isDark, toggleTheme } = useTheme();
  const [globalLock, setGlobalLock] = useState(false);
  const [currentUser, setCurrentUser] = useState(authService.getCurrentUser());
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(!authService.isAuthenticated());

  // Phase 5 State
  const [isSystemFrozen, setIsSystemFrozen] = useState(false);
  const [riskModalOpen, setRiskModalOpen] = useState(false);
  const [pendingTrade, setPendingTrade] = useState(null);
  const [showKillMFA, setShowKillMFA] = useState(false);
  
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
    'Alt+1': () => navigate('/workspace/terminal'),
    'Alt+2': () => navigate('/analytics/options'),
    'Alt+3': () => navigate('/portfolio/backtest'),
    'Alt+4': () => navigate('/scanner/global'),
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
        fetch('/api/v1/onboarding/status')
          .then(res => res.json())
          .then(data => {
            if (data.success && !data.data.completed) {
              setShowOnboarding(true);
            }
          })
          .catch(() => {
            // If API fails, check localStorage
            if (!onboardingCompleted) {
              setShowOnboarding(true);
            }
          });
      }
    }
  }, [currentUser]);

  // Phase 1 Verification: Spawn Welcome Window
  const addWindow = useWindowStore((state) => state.addWindow);
  useEffect(() => {
      if (useWindowStore.getState().windows.length === 0) {
          addWindow({
              title: 'Phase 1: Window Manager Ready',
              width: 500,
              height: 400,
              x: 150,
              y: 150,
              isMinimized: true,
              component: () => (
                  <div style={{padding: 20, color: 'white'}}>
                      <h3>System Operational</h3>
                      <p>Window Manager: <strong>Active</strong></p>
                      <p>Taskbar: <strong>Active</strong></p>
                      <p>Glassmorphism: <strong>Enabled</strong></p>
                      <br/>
                      <button onClick={() => addWindow({title: 'New Window', x: 200, y: 200})}>
                          Spawn Another Window
                      </button>
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
      return;
    }

    switch (action) {
      // Navigation
      case 'show-dashboard': navigate('/workspace/terminal'); break;
      case 'show-mission-control': navigate('/workspace/mission-control'); break;
      case 'show-political-alpha': navigate('/analytics/political'); break;
      case 'show-strategy-distillery': navigate('/analytics/strategy'); break;
      case 'show-debate-chamber': navigate('/workspace/debate'); break;
      case 'show-auto-coder': navigate('/workspace/autocoder'); break;
      case 'show-sandbox': navigate('/workspace/auto-coder'); break;
      case 'show-vr-cockpit': navigate('/workspace/vr'); break;
      case 'show-options': navigate('/analytics/options'); break;
      case 'show-backtest': navigate('/portfolio/backtest'); break;
      case 'show-brokerage': navigate('/portfolio/brokerage'); break;
      case 'show-scanner': navigate('/scanner/global'); break; // Phase 4

      // Roles & New Phases
      case 'role-observer': navigate('/observer/macro'); break; // Phase 10
      case 'role-estate': navigate('/strategist/estate'); break; // Phase 15
      case 'role-guardian': navigate('/guardian/compliance'); break; // Phase 11
      case 'role-warden': navigate('/mobile'); break; // Phase 22
      case 'role-audit': navigate('/guardian/compliance/audit'); break; // Phase 16
      case 'role-margin': navigate('/guardian/margin'); break; // Phase 21
      case 'role-scenarios': navigate('/guardian/scenarios'); break; // Phase 17
      case 'role-analyst': navigate('/analyst/debate'); break; // Phase 12
      case 'role-strategist': navigate('/strategist/currency'); break; // Phase 13
      case 'role-impact': navigate('/strategist/impact'); break; // Phase 18
      case 'role-corporate': navigate('/strategist/corporate'); break; // Phase 20
      case 'role-architect': navigate('/architect/system'); break; // Phase 19
      case 'role-api': navigate('/architect/api'); break; // Phase 23
      case 'show-tax': navigate('/portfolio/tax'); break; // Phase 9
      case 'show-crypto': navigate('/portfolio/crypto'); break; // Phase 8
      case 'show-fixed-income': navigate('/portfolio/fixed-income'); break; // Phase 7 (FixedIncomeDashboard)
      case 'show-attribution': navigate('/portfolio/attribution'); break; // Phase 6 (PortfolioAttribution)
      case 'show-assets': navigate('/assets'); break; // Phase 24
      case 'show-zen': navigate('/zen'); break; // Phase 24 (Zen)
      case 'show-cash-flow': navigate('/portfolio/cash-flow'); break; // Phase 10
      case 'show-tenant': navigate('/tenant'); break;
      case 'profile-settings': navigate('/settings'); break;
      
      // App Hardening & Improvements - Portfolio Analytics
      case 'nav-advanced-analytics': navigate('/portfolio/advanced-analytics'); break;
      case 'nav-portfolio-optimization': navigate('/portfolio/optimization'); break;
      case 'nav-advanced-risk': navigate('/portfolio/risk'); break;
      case 'nav-tax-optimization': navigate('/portfolio/tax-optimization'); break;
      
      // Trading & Execution
      case 'nav-options-strategy': navigate('/trading/options'); break;
      case 'nav-advanced-orders': navigate('/trading/advanced-orders'); break;
      case 'nav-paper-trading': navigate('/trading/paper'); break;
      case 'nav-algorithmic-trading': navigate('/trading/algorithmic'); break;
      
      // Financial Planning
      case 'nav-financial-planning': navigate('/planning/financial'); break;
      case 'nav-retirement-planning': navigate('/planning/retirement'); break;
      case 'nav-estate-planning': navigate('/planning/estate'); break;
      case 'nav-budgeting': navigate('/budgeting'); break;
      case 'nav-bill-payment': navigate('/billing/payments'); break;
      case 'nav-credit-monitoring': navigate('/credit/monitoring'); break;
      
      // Market Intelligence
      case 'nav-news-sentiment': navigate('/news/sentiment'); break;
      case 'nav-watchlists-alerts': navigate('/watchlists/alerts'); break;
      case 'nav-research-reports': navigate('/research/reports'); break;
      case 'nav-advanced-charting': navigate('/charting/advanced'); break;
      
      // Social & Community
      case 'nav-social-trading': navigate('/social/trading'); break;
      case 'nav-community-forums': navigate('/community/forums'); break;
      case 'nav-education': navigate('/education'); break;
      
      // AI & Machine Learning
      case 'nav-ai-predictions': navigate('/ai/predictions'); break;
      case 'nav-ai-assistant': navigate('/ai/assistant'); break;
      case 'nav-ml-training': navigate('/ml/training'); break;
      
      // Integrations & Platform
      case 'nav-integrations': navigate('/integrations'); break;
      case 'nav-developer-platform': navigate('/developer/platform'); break;
      case 'nav-marketplace': navigate('/marketplace'); break;
      
      // Enterprise & Compliance
      case 'nav-enterprise': navigate('/enterprise'); break;
      case 'nav-compliance': navigate('/compliance'); break;
      case 'nav-institutional': navigate('/institutional'); break;
      
      // View & Theme
      case 'toggle-theme': toggleTheme(); break;
      case 'toggle-fullscreen':
        if (document.fullscreenElement) {
          document.exitFullscreen();
        } else {
          document.documentElement.requestFullscreen();
        }
        break;
      
      // Layout & Widgets
      case 'reset-layout': resetLayout(); break;
      case 'lock-widgets': setGlobalLock(true); break;
      case 'unlock-widgets': setGlobalLock(false); break;
      case 'toggle-lock': setGlobalLock(prev => !prev); break;
      case 'open-all-widgets': {
        // Set all widgets to visible and clear corrupted layout
        const allVisible = {};
        const widgetKeys = ['monitor-view', 'command-view', 'research-view', 'portfolio-view', 
                           'homeostasis-view', 'options-chain-view', 'market-depth-view', 
                           'trade-tape-view', 'terminal-view', 'bar-chart'];
        widgetKeys.forEach(k => allVisible[k] = true);
        setWidgetVisibility(allVisible);
        // Clear corrupted layout coordinates
        localStorage.removeItem('react_node_template_widget_layout');
        // Force reset to DEFAULT_LAYOUT
        resetLayout();
        break;
      }
      case 'close-all-widgets': {
        const allHidden = {};
        const allWidgetKeys = ['monitor-view', 'command-view', 'research-view', 'portfolio-view', 
                              'homeostasis-view', 'options-chain-view', 'market-depth-view', 
                              'trade-tape-view', 'terminal-view', 'bar-chart'];
        allWidgetKeys.forEach(k => allHidden[k] = false);
        setWidgetVisibility(allHidden);
        break;
      }
      
      // Auth
      case 'logout': handleLogout(); break;
      case 'signin': setIsAuthModalOpen(true); break;
      
      // Debug
      case 'force-loading': setDebugStates(prev => ({ ...prev, forceLoading: !prev.forceLoading })); break;
      case 'force-error': setDebugStates(prev => ({ ...prev, forceError: !prev.forceError })); break;

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
            <Breadcrumbs />
            {/* Route Content Wrapper - Takes remaining flex space */}
            <div className={isOSStylePage ? 'route-content-os' : 'route-content'}>
            <Suspense fallback={<DashboardSkeleton />}>
              <GlobalTooltip />
              <Routes>
                {/* Overview Landing Pages */}
                <Route path="/workspace" element={<RoleOverview />} />
                <Route path="/analytics" element={<RoleOverview />} />
                <Route path="/analyst" element={<RoleOverview />} />
                <Route path="/portfolio" element={<RoleOverview />} />
                <Route path="/guardian" element={<RoleOverview />} />
                <Route path="/strategist" element={<RoleOverview />} />
                <Route path="/architect" element={<RoleOverview />} />
                <Route path="/observer" element={<RoleOverview />} />
                <Route path="/scanner" element={<RoleOverview />} />

                <Route path="/" element={<Navigate to="/workspace/terminal" replace />} />
                <Route path="/workspace/terminal" element={
                  <TerminalWorkspace
                    handleViewSource={() => { }}
                    globalLock={globalLock}
                    isDarkMode={isDark}
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
                <Route path="/strategist/estate" element={<EstateDashboard />} />
                <Route path="/strategist/impact" element={<ImpactDashboard />} />
                <Route path="/strategist/corporate" element={<CorporateDashboard />} />
                <Route path="/architect/system" element={<SystemHealthDashboard />} />
                <Route path="/architect/api" element={<APIDashboard />} />
                <Route path="/architect/system" element={<SystemHealthDashboard />} />
                <Route path="/guardian/compliance/audit" element={<AuditDashboard />} />
                <Route path="/guardian/scenarios" element={<ScenarioDashboard />} />
                <Route path="/guardian/margin" element={<MarginDashboard />} />
                <Route path="/mobile" element={<MobileDashboard />} />
                <Route path="/portfolio/brokerage" element={<BrokerageAccount />} />
                <Route path="/workspace/auto-coder" element={<AutoCoderSandbox />} />
                <Route path="/portfolio/attribution" element={<PortfolioAttribution />} />
                <Route path="/portfolio/fixed-income" element={<FixedIncomeDashboard />} />
                <Route path="/portfolio/crypto" element={<CryptoDashboard />} />
                <Route path="/portfolio/tax" element={<TaxDashboard />} />
                <Route path="/observer/macro" element={<MacroDashboard />} />
                <Route path="/guardian/compliance" element={<ComplianceDashboard />} />
                <Route path="/analyst/debate" element={<DebateRoom />} />
                <Route path="/strategist/currency" element={<CurrencyDashboard />} />
                <Route path="/scanner/global" element={<GlobalScanner />} />
                <Route path="/assets" element={<AssetsDashboard />} />
                <Route path="/portfolio/cash-flow" element={<CashFlowDashboard />} />
                <Route path="/zen" element={<ZenMode />} />
                <Route path="/tenant" element={<TenantDashboard />} />
                {/* App Hardening & Improvements Routes */}
                <Route path="/portfolio/advanced-analytics" element={<AdvancedPortfolioAnalytics />} />
                <Route path="/portfolio/optimization" element={<PortfolioOptimizationDashboard />} />
                <Route path="/portfolio/risk" element={<AdvancedRiskDashboard />} />
                <Route path="/portfolio/tax-optimization" element={<TaxOptimizationDashboard />} />
                <Route path="/planning/financial" element={<FinancialPlanningDashboard />} />
                <Route path="/planning/retirement" element={<RetirementPlanningDashboard />} />
                <Route path="/budgeting" element={<BudgetingDashboard />} />
                <Route path="/trading/options" element={<OptionsStrategyDashboard />} />
                <Route path="/trading/paper" element={<PaperTradingDashboard />} />
                <Route path="/trading/algorithmic" element={<AlgorithmicTradingDashboard />} />
                <Route path="/planning/estate" element={<EstatePlanningDashboard />} />
                <Route path="/billing/payments" element={<BillPaymentDashboard />} />
                <Route path="/credit/monitoring" element={<CreditMonitoringDashboard />} />
                <Route path="/research/reports" element={<ResearchReportsDashboard />} />
                <Route path="/social/trading" element={<SocialTradingDashboard />} />
                <Route path="/community/forums" element={<CommunityForumsDashboard />} />
                <Route path="/education" element={<EducationPlatformDashboard />} />
                <Route path="/charting/advanced" element={<AdvancedChartingDashboard />} />
                <Route path="/trading/advanced-orders" element={<AdvancedOrdersDashboard />} />
                <Route path="/enterprise" element={<EnterpriseDashboard />} />
                <Route path="/compliance" element={<ComplianceDashboard />} />
                <Route path="/institutional" element={<InstitutionalToolsDashboard />} />
                <Route path="/ml/training" element={<MLTrainingDashboard />} />
                <Route path="/integrations" element={<IntegrationsDashboard />} />
                <Route path="/developer/platform" element={<DeveloperPlatformDashboard />} />
                <Route path="/marketplace" element={<MarketplaceDashboard />} />
                <Route path="/news/sentiment" element={<NewsSentimentDashboard />} />
                <Route path="/watchlists/alerts" element={<WatchlistsAlertsDashboard />} />
                <Route path="/ai/predictions" element={<AIPredictionsDashboard />} />
                <Route path="/ai/assistant" element={<AIAssistantDashboard />} />
                <Route path="/legal/terms" element={<TermsOfService />} />
                <Route path="/legal/privacy" element={<PrivacyPolicy />} />
                <Route path="/settings" element={<div className="p-8 text-white"><h1>Settings</h1><p>Configuration panel coming soon.</p></div>} />
                <Route path="/chat" element={<div className="p-8 text-white"><h1>Chat</h1><p>Real-time chat interface coming soon.</p></div>} />
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
            // Chain to Phase 5 Execution Shield
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

        {/* Phase 1: Window Manager Layer */}
        {useWindowStore((state) => state.windows).map((window) => (
            <WindowWrapper key={window.id} id={window.id} />
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

        {/* Phase 5: Global Safety Logic */}
        <MFAVerificationModal 
            isOpen={showKillMFA}
            onClose={() => setShowKillMFA(false)}
            actionName="Engagement of Global Kill Switch"
            onSuccess={async (mfa_code) => {
                setIsSystemFrozen(true);
                try {
                    await fetch('/api/v1/risk/kill-switch', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ 
                          action: 'engage', 
                          reason: 'User Kill Switch (MFA Verified)',
                          mfa_code: mfa_code // Sent to backend
                        })
                    });
                    notify({ title: 'SYSTEM HALTED', body: 'Kill switch signal broadcasted', type: 'critical' });
                } catch (e) {
                    notify({ title: 'KILL SWITCH ERROR', body: 'Failed to notify backend', type: 'error' });
                }
            }}
        />
        <KillSwitch onTrigger={() => setShowKillMFA(true)} />
        <FrozenOverlay isFrozen={isSystemFrozen} onUnlock={() => setIsSystemFrozen(false)} />
        <PreTradeRiskModal 
            isOpen={riskModalOpen} 
            onClose={() => setRiskModalOpen(false)}
            tradeDetails={pendingTrade}
            onConfirm={async () => {
                setRiskModalOpen(false);
                try {
                    const token = localStorage.getItem('token');
                    const response = await fetch('/api/v1/brokerage/order', {
                        method: 'POST',
                        headers: { 
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        },
                        body: JSON.stringify({
                            symbol: pendingTrade.ticker,
                            qty: pendingTrade.size,
                            side: pendingTrade.side,
                            type: 'market'
                        })
                    });
                    const result = await response.json();
                    if (response.ok) {
                        notify({ 
                            title: 'ORDER EXECUTED', 
                            body: `${pendingTrade.side} ${pendingTrade.size} ${pendingTrade.ticker} @ ${result.price || 'Mkt'}`, 
                            type: 'success' 
                        });
                    } else {
                        notify({ 
                            title: 'EXECUTION REJECTED', 
                            body: result.reason || 'Safety parameters violated', 
                            type: 'error' 
                        });
                    }
                } catch (e) {
                    notify({ title: 'ROUTING ERROR', body: 'Failed to reach execution gateway', type: 'error' });
                }
            }}
        />

        
        {/* Phase 01: Education Mode Overlay */}
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
                fetch('/api/v1/onboarding/complete', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ preferences })
                }).catch(console.error);
              }}
              onSkip={() => {
                setShowOnboarding(false);
                localStorage.setItem('onboarding_completed', 'skipped');
                fetch('/api/v1/onboarding/skip', { method: 'POST' }).catch(console.error);
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
