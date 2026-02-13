import React, { useEffect, useState, useRef, Suspense, lazy, useMemo, useCallback } from 'react';
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
import SubPageBoilerplate from './components/Common/SubPageBoilerplate';
import './App.css';

import PageContextPanel from './components/Common/PageContextPanel';
import { DEPT_REGISTRY } from './config/departmentRegistry';
import { getIcon } from './config/iconRegistry';
import useDepartmentStore from './stores/departmentStore';

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

import { Routes, Route, Navigate, useNavigate, useLocation, useParams } from 'react-router-dom';
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
const Homeostasis = lazy(() => import('./pages/Homeostasis'));
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
const MissionsOverview = lazy(() => import('./pages/MissionsOverview'));
const FleetDashboard = lazy(() => import('./pages/FleetDashboard'));
const GlobalSearchPage = lazy(() => import('./pages/GlobalSearch'));
const CommandCenter = lazy(() => import('./components/Admin/CommandCenter'));
const EventBusMonitor = lazy(() => import('./pages/admin/EventBusMonitor'));
const StorageManager = lazy(() => import('./pages/admin/StorageManager'));
const GraphBrowser = lazy(() => import('./pages/admin/GraphBrowser'));
const LogViewer = lazy(() => import('./pages/admin/LogViewer'));
const ServiceHealthGrid = lazy(() => import('./pages/admin/ServiceHealthGrid'));
const MiddlewarePipeline = lazy(() => import('./pages/admin/MiddlewarePipeline'));
const MonitoringDashboard = lazy(() => import('./pages/admin/MonitoringDashboard'));
const AlertConfigPage = lazy(() => import('./pages/admin/AlertConfigPage'));
const DeploymentController = lazy(() => import('./pages/admin/DeploymentController'));
const OperationsDashboard = lazy(() => import('./pages/admin/OperationsDashboard'));
const WorkspaceManager = lazy(() => import('./pages/admin/WorkspaceManager'));
const FeatureFlagManager = lazy(() => import('./pages/admin/FeatureFlagManager'));
const EnvironmentSettings = lazy(() => import('./pages/admin/EnvironmentSettings'));
const ForcedSellerMonitor = lazy(() => import('./pages/data-scientist/ForcedSellerMonitor'));
const WhaleFlowTerminal = lazy(() => import('./pages/data-scientist/WhaleFlowTerminal'));
const TechnicalIndicatorsPage = lazy(() => import('./pages/data-scientist/TechnicalIndicatorsPage'));
const Rule144CompliancePage = lazy(() => import('./pages/legal/Rule144CompliancePage'));
const DataPipelineManager = lazy(() => import('./pages/admin/DataPipelineManager'));
const APIConnectorHub = lazy(() => import('./pages/admin/APIConnectorHub'));
const ExternalDataSources = lazy(() => import('./pages/admin/ExternalDataSources'));
const WebhookReceiver = lazy(() => import('./pages/admin/WebhookReceiver'));
const DataQualityDashboard = lazy(() => import('./pages/admin/DataQualityDashboard'));
const NewsAggregator = lazy(() => import('./pages/hunter/NewsAggregator'));
const SocialSentimentRadar = lazy(() => import('./pages/data-scientist/SocialSentimentRadar'));
const SocialTradingFeed = lazy(() => import('./pages/hunter/SocialTradingFeed'));
const RumorMill = lazy(() => import('./pages/hunter/RumorMill'));
const ResearchWorkspace = lazy(() => import('./pages/data-scientist/ResearchWorkspace'));
const FactorAnalysisSuite = lazy(() => import('./pages/data-scientist/FactorAnalysisSuite'));
const FundamentalScanner = lazy(() => import('./pages/data-scientist/FundamentalScanner'));
const QuantBacktestLab = lazy(() => import('./pages/data-scientist/QuantBacktestLab'));
const AdvancedChartBuilder = lazy(() => import('./pages/data-scientist/AdvancedChartBuilder'));
const HeatmapGenerator = lazy(() => import('./pages/data-scientist/HeatmapGenerator'));
const AgentFleetOverview = lazy(() => import('./pages/admin/AgentFleetOverview'));
const AgentTaskQueue = lazy(() => import('./pages/admin/AgentTaskQueue'));
const AgentLogsViewer = lazy(() => import('./pages/admin/AgentLogsViewer'));
const DebateArena = lazy(() => import('./pages/data-scientist/DebateArena'));
const DebateHistory = lazy(() => import('./pages/data-scientist/DebateHistory'));
const OrderManagementSystem = lazy(() => import('./pages/admin/OrderManagementSystem'));
const RiskLimitManager = lazy(() => import('./pages/admin/RiskLimitManager'));
const ComplianceTracker = lazy(() => import('./pages/admin/ComplianceTracker'));
const DataValidation = lazy(() => import('./pages/admin/DataValidation'));
const ReconciliationDashboard = lazy(() => import('./pages/admin/ReconciliationDashboard'));
const TreasuryDashboard = lazy(() => import('./pages/admin/TreasuryDashboard'));
const PortfolioOverview = lazy(() => import('./pages/admin/PortfolioOverview'));
const CryptoWalletPage = lazy(() => import('./pages/admin/CryptoWalletPage'));
const ExecSummaryPage = lazy(() => import('./pages/admin/ExecSummaryPage'));
const CrashSimulator = lazy(() => import('./pages/admin/CrashSimulator'));
const TacticalCommandCenter = lazy(() => import('./pages/admin/TacticalCommandCenter'));
const PricingVerifier = lazy(() => import('./pages/admin/PricingVerifier'));
const SourceReputation = lazy(() => import('./pages/admin/SourceReputation'));
const QualityIncidents = lazy(() => import('./pages/admin/QualityIncidents'));
const DiscrepancyResolution = lazy(() => import('./pages/admin/DiscrepancyResolution'));
const TransactionLedger = lazy(() => import('./pages/admin/TransactionLedger'));
const TransferCenter = lazy(() => import('./pages/admin/TransferCenter'));
const TaxHarvester = lazy(() => import('./pages/admin/TaxHarvester'));
const TaxLiabilityDashboard = lazy(() => import('./pages/admin/TaxLiabilityDashboard'));
const ExpenseManager = lazy(() => import('./pages/admin/ExpenseManager'));
const YieldOptimizer = lazy(() => import('./pages/admin/YieldOptimizer'));
const TrustAdmin = lazy(() => import('./pages/admin/TrustAdmin'));
const DonationManager = lazy(() => import('./pages/admin/DonationManager'));
const PhilanthropyCenter = lazy(() => import('./pages/admin/PhilanthropyCenter'));
const SuccessionModeler = lazy(() => import('./pages/admin/SuccessionModeler'));
const EstateVisualizer = lazy(() => import('./pages/admin/EstateVisualizer'));
const GiftingOptimizer = lazy(() => import('./pages/admin/GiftingOptimizer'));
const BlackSwanGenerator = lazy(() => import('./pages/admin/BlackSwanGenerator'));
const WarGameArena = lazy(() => import('./pages/admin/WarGameArena'));
const RobustnessLab = lazy(() => import('./pages/admin/RobustnessLab'));


// --- Dynamic Workstation Loader ---
// This loader dynamically imports components from the workstations directory based on the URL path.
const workstationModules = import.meta.glob('./pages/workstations/**/*.jsx');

const DynamicWorkstation = () => {
    const { deptSlug, subSlug } = useParams();
    const [Component, setComponent] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadComponent = async () => {
            setLoading(true);
            try {
                // Helper to convert kebab-case to PascalCase (e.g. debate-history -> DebateHistory)
                const toPascal = (s) => s.split('-').map(p => p.charAt(0).toUpperCase() + p.slice(1)).join('');

                const deptPascal = toPascal(deptSlug);
                const subPascal = toPascal(subSlug);

                // Strategy 1: Look for exact PascalCase submodule name in the department folder
                // e.g. /data-scientist/debate-history -> Look for .../DebateHistory.jsx
                let match = Object.keys(workstationModules).find(key => 
                    key.includes(`/${deptSlug}/`) && key.endsWith(`/${subPascal}.jsx`)
                );
                
                // Strategy 2: Look for Dept+Sub naming convention (legacy or specific files)
                // e.g. .../DatascientistDebatehistory.jsx OR .../DataScientistDebateHistory.jsx
                if (!match) {
                    const combinedName = deptPascal + subPascal;
                    match = Object.keys(workstationModules).find(key => 
                        key.includes(`/${deptSlug}/`) && 
                        (key.endsWith(`/${combinedName}.jsx`) || key.toLowerCase().endsWith(`/${combinedName.toLowerCase()}.jsx`))
                    );
                }

                // Strategy 3: Loose match (case-insensitive) for subPascal in the department folder
                if (!match) {
                     match = Object.keys(workstationModules).find(key => 
                        key.includes(`/${deptSlug}/`) && key.toLowerCase().endsWith(`/${subPascal.toLowerCase()}.jsx`)
                    );
                }

                if (match) {
                    const module = await workstationModules[match]();
                    setComponent(() => module.default);
                } else {
                    console.warn(`Workstation not found for path: ${deptSlug}/${subSlug}. Checked: ${subPascal}.jsx, ${deptPascal}${subPascal}.jsx`);
                }
            } catch (err) {
                console.error("Failed to load dynamic workstation:", err);
            } finally {
                setLoading(false);
            }
        };

        if (deptSlug && subSlug) {
            loadComponent();
        }
    }, [deptSlug, subSlug]);

    if (loading) return (
        <div className="flex items-center justify-center min-h-screen bg-black font-mono text-cyan-500">
            <div className="pulse">INITIALIZING_WORKSTATION_STREAM...</div>
        </div>
    );
    
    if (!Component) return (
        <div className="flex items-center justify-center min-h-screen bg-black font-mono text-red-500">
            <div>ERROR: WORKSTATION_NOT_FOUND // PATH: /{deptSlug}/{subSlug}</div>
        </div>
    );

    return <Component />;
};
const GoogleAuthCallback = lazy(() => import('./pages/GoogleAuthCallback'));

// --- Agent Departments ---
const ScrumMaster = lazy(() => import('./pages/Departments/ScrumMaster'));
const VennIntersectionView = lazy(() => import('./pages/Departments/VennIntersectionView'));
const OrchestratorPage = lazy(() => import('./pages/Departments/OrchestratorPage'));

const ArchitectPage = lazy(() => import('./pages/Departments/ArchitectPage'));
const DataScientistPage = lazy(() => import('./pages/Departments/DataScientistPage'));
const StrategistPage = lazy(() => import('./pages/Departments/StrategistPage'));
const TraderPage = lazy(() => import('./pages/Departments/TraderPage'));
const PhysicistPage = lazy(() => import('./pages/Departments/PhysicistPage'));
const HunterPage = lazy(() => import('./pages/Departments/HunterPage'));
const SentryPage = lazy(() => import('./pages/Departments/SentryPage'));
const StewardPage = lazy(() => import('./pages/Departments/StewardPage'));
const GuardianPage = lazy(() => import('./pages/Departments/GuardianPage'));
const LawyerPage = lazy(() => import('./pages/Departments/LawyerPage'));
const AuditorPage = lazy(() => import('./pages/Departments/AuditorPage'));
const EnvoyPage = lazy(() => import('./pages/Departments/EnvoyPage'));
const FrontOfficePage = lazy(() => import('./pages/Departments/FrontOfficePage'));
const HistorianPage = lazy(() => import('./pages/Departments/HistorianPage'));
const StressTesterPage = lazy(() => import('./pages/Departments/StressTesterPage'));
const RefinerPage = lazy(() => import('./pages/Departments/RefinerPage'));
const BankerPage = lazy(() => import('./pages/Departments/BankerPage'));
const AccountOverview = lazy(() => import('./pages/Accounts/AccountOverview'));
const AdminDashboard = lazy(() => import('./pages/AdminDashboard'));
const AdminPage = lazy(() => import('./pages/Departments/AdminPage'));
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
  const isOSStylePage = useMemo(() => {
    if (location.pathname.startsWith('/special/')) return true;
    if (location.pathname.startsWith('/dept/')) return true;
    if (location.pathname.startsWith('/scrum')) return true;
    if (location.pathname.startsWith('/account')) return false; // Account is standard
    
    // Check if the first segment is a known department slug
    const parts = location.pathname.split('/').filter(Boolean);
    if (parts.length === 0) return false;
    
    const slug = parts[0];
    const aliases = {
      'analyst': 'data-scientist',
      'legal': 'lawyer',
      'pioneer': 'data-scientist',
      'orchestrator': 'orchestrator'
    };
    const targetSlug = aliases[slug] || slug;
    return !!Object.values(DEPT_REGISTRY).find(d => d.slug === targetSlug);
  }, [location.pathname]);

  // Persistent Department Detection
  const currentDept = useMemo(() => {
    const parts = location.pathname.split('/').filter(Boolean);
    if (parts.length === 0) return null;
    
    // 1. Unified Special/Dept/Scrum check
    if (parts[0] === 'dept' || parts[0] === 'scrum' || parts[0] === 'special') {
      const target = parts[1];
      if (!target || parts[0] === 'scrum') {
        return { id: 'scrum', name: 'SCRUM OF SCORUMS', color: '#ffd700', agents: [], route: '/special/scrum' };
      }
      
      // If it's something like /special/terminal, we look for Orchestrator (ID 1) as the base context
      if (parts[0] === 'special') {
        return DEPT_REGISTRY[1]; 
      }

      if (/^\d+$/.test(target)) return DEPT_REGISTRY[target];
      return Object.values(DEPT_REGISTRY).find(d => d.slug === target);
    }

    // 2. Direct Slug Check (e.g., /physicist/...)
    const slug = parts[0];
    const aliases = {
      'analyst': 'data-scientist',
      'legal': 'lawyer',
      'pioneer': 'data-scientist'
    };
    const targetSlug = aliases[slug] || slug;
    return Object.values(DEPT_REGISTRY).find(d => d.slug === targetSlug);
  }, [location.pathname]);

  const departmentData = useDepartmentStore(state => currentDept ? state.departments[currentDept.id] : null);

  const telemetryData = useMemo(() => {
    if (!currentDept) return [];
    return [
      { 
        label: "KAFKA CHANNEL", 
        value: `DEPT.${currentDept.id}.LIVE`, 
        variant: "success",
        className: "kafka"
      },
      { 
        label: currentDept.primaryMetricLabel || "SYS PERFORMANCE", 
        value: `${departmentData?.metrics?.[currentDept.primaryMetric] || 0}${currentDept.primaryMetricUnit || ""}`, 
        variant: "highlight",
        className: "metric"
      },
      { 
        label: "NEURAL LOAD", 
        value: `${(Math.random() * 15 + 10).toFixed(1)}%`, 
        variant: "highlight",
        className: "load",
        showBar: true,
        barValue: Math.random() * 40 + 20
      },
      { 
        label: "AGENT FLEET", 
        value: `${currentDept.agents.length} ACTIVE`, 
        variant: "mono",
        className: "agents"
      }
    ];
  }, [currentDept, departmentData]);
  const {
    resetLayout = () => {},
    activeWorkspace = 'default',
    workspaces = [],
    saveWorkspace = () => {},
    loadWorkspace = () => {},
  } = useWidgetLayout() || {};

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


  // Theme is now managed by ThemeContext - no need for local useEffect


  // Socket.io initialization (Consolidated with PresenceService)
  useEffect(() => {
    if (!currentUser) return;
    
    // Initialize presence service (which handles the socket connection)
    presenceService.initialize(currentUser.id, currentUser.username);
    const socket = presenceService.socket;
    
    if (socket) {
      socket.on('connect', () => {
        setSocketConnected(true);
        // Initialize department store socket listeners
        useDepartmentStore.getState().initSocketListeners();
      });
      socket.on('disconnect', () => setSocketConnected(false));
      // Update state if already connected
      if (socket.connected) {
        setSocketConnected(true);
        useDepartmentStore.getState().initSocketListeners();
      }
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
          .then(data => {
            if (data.success && !data.data?.completed) {
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
  const windowIds = useWindowStore(useShallow((state) => state.windows.map(w => w.id)));
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

  const handleLogout = useCallback(() => {
    authService.logout();
    setCurrentUser(null);
    setIsAuthModalOpen(true);
  }, []);

  const handleSaveWorkspacePrompt = useCallback(() => {
    const name = prompt('Enter a name for this workspace:', activeWorkspace);
    if (name) saveWorkspace(name);
  }, [activeWorkspace, saveWorkspace]);

  const handleMenuAction = useCallback((action) => {
    // Handle widget toggle actions
    if (action?.startsWith('toggle-widget-')) {
      const widgetId = action.replace('toggle-widget-', '');
      setWidgetVisibility(prev => ({ ...prev, [widgetId]: prev[widgetId] === false ? true : false }));
      if (location.pathname !== '/orchestrator/terminal') {
        navigate('/orchestrator/terminal');
      }
      return;
    }

    if (action?.startsWith('nav-path:')) {
      const path = action.replace('nav-path:', '');
      navigate(path);
      return;
    }

    switch (action) {
      // --- Special Pages Actions (Consolidated) ---
      case 'nav-special-scrum': navigate('/special/scrum'); break;
      case 'nav-special-mobile': navigate('/special/mobile'); break;
      case 'nav-special-vr': navigate('/special/vr'); break;
      case 'nav-special-mission-control': navigate('/special/mission-control'); break;
      case 'nav-special-terminal': navigate('/special/terminal'); break;
      case 'nav-special-political': navigate('/special/political'); break;
      case 'nav-special-strategy': navigate('/special/strategy'); break;
      case 'nav-special-debate': navigate('/special/debate'); break;
      case 'nav-special-missions': navigate('/special/missions'); break;
      case 'nav-special-paper': navigate('/special/paper'); break;
      case 'nav-special-zen': navigate('/special/zen'); break;
      case 'nav-brokerage': navigate('/strategist/brokerage'); break;

      // --- Agent Departments (Phase 2/3) ---
      case 'nav-scrum-master': navigate('/special/scrum'); break;
      case 'nav-dept-1': navigate('/dept/orchestrator'); break;
      case 'nav-dept-2': navigate('/dept/architect'); break;
      case 'nav-dept-3': navigate('/dept/data-scientist'); break;
      case 'nav-dept-4': navigate('/dept/strategist'); break;
      case 'nav-dept-5': navigate('/dept/trader'); break;
      case 'nav-dept-6': navigate('/dept/physicist'); break;
      case 'nav-dept-7': navigate('/dept/hunter'); break;
      case 'nav-dept-8': navigate('/dept/sentry'); break;
      case 'nav-dept-9': navigate('/dept/steward'); break;
      case 'nav-dept-10': navigate('/dept/guardian'); break;
      case 'nav-dept-11': navigate('/dept/lawyer'); break;
      case 'nav-dept-12': navigate('/dept/auditor'); break;
      case 'nav-dept-13': navigate('/dept/envoy'); break;
      case 'nav-dept-14': navigate('/dept/front-office'); break;
      case 'nav-dept-15': navigate('/dept/historian'); break;
      case 'nav-dept-16': navigate('/dept/stress-tester'); break;
      case 'nav-dept-17': navigate('/dept/refiner'); break;
      case 'nav-dept-18': navigate('/dept/banker'); break;

      // Widgets / Specifics
      case 'toggle-theme': toggleTheme(); break;
      case 'reset-layout': resetLayout(); break;
      case 'profile-settings': navigate('/settings'); break;
      case 'logout': handleLogout(); break;
      case 'signin': setIsAuthModalOpen(true); break;

      default: break;
    }
  }, [navigate, location.pathname, toggleTheme, resetLayout, handleLogout]);

  const onToggleWidget = useCallback((widgetId) => {
    setWidgetVisibility(prev => ({ ...prev, [widgetId]: prev[widgetId] === false ? true : false }));
  }, []);

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
            onToggleWidget={onToggleWidget}
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
          {/* <SubHeaderNav /> */}
          
          <main className={`institutional-os-container ${isOSStylePage ? 'os-bleed' : ''}`}>
            {/* Persistent Department Header */}
            {isOSStylePage && currentDept && (
              <PageContextPanel 
                title={currentDept.name}
                color={currentDept.color}
                status="DEPARTMENT_ACTIVE"
                telemetry={telemetryData}
                isDashboard={location.pathname === currentDept.route}
                subPages={currentDept.subModules || []}
                onNavigate={(path) => {
                  if (path === 'dashboard') navigate(currentDept.route);
                  else navigate(path);
                }}
                icon={getIcon(currentDept.icon)}
              />
            )}
            
            <div className={isOSStylePage ? 'route-content-os' : 'route-content'}>
            <Suspense fallback={<DashboardSkeleton />}>
              <GlobalTooltip />
              <Routes>
                {/* Role Landing Pages */}
                {/* --- Legacy Category Redirects --- */}
                <Route path="/orchestrator/terminal" element={<Navigate to="/special/terminal" replace />} />
                <Route path="/orchestrator/mission-control" element={<Navigate to="/special/mission-control" replace />} />
                <Route path="/orchestrator/zen" element={<Navigate to="/special/zen" replace />} />
                <Route path="/orchestrator" element={<Navigate to="/dept/orchestrator" replace />} />
                <Route path="/architect" element={<Navigate to="/dept/architect" replace />} />
                <Route path="/analyst" element={<Navigate to="/dept/data-scientist" replace />} />
                <Route path="/trader" element={<Navigate to="/dept/trader" replace />} />
                <Route path="/strategist" element={<Navigate to="/dept/strategist" replace />} />
                 <Route path="/guardian" element={<Navigate to="/dept/guardian" replace />} />
                 <Route path="/marketing" element={<Navigate to="/dept/hunter" replace />} />
                 <Route path="/hunter" element={<Navigate to="/dept/hunter" replace />} />
                 <Route path="/legal" element={<Navigate to="/dept/lawyer" replace />} />
                 <Route path="/pioneer" element={<Navigate to="/dept/data-scientist" replace />} />

                {/* --- Sub-Module Routes --- */}
                <Route path="/orchestrator/graph" element={<MasterOrchestrator />} />

                <Route path="/architect/health" element={<SystemHealthDashboard />} />
                <Route path="/architect/api" element={<APIDashboard />} />
                <Route path="/architect/admin" element={<AdminDashboard />} />
                <Route path="/architect/integrations" element={<IntegrationsDashboard />} />
                <Route path="/architect/dev-platform" element={<DeveloperPlatformDashboard />} />
                <Route path="/special/fleet" element={<FleetDashboard />} />

                {/* Removed: <Route path="/analyst/predictions" element={<AIPredictionsDashboard />} /> */}
                {/* Removed: <Route path="/analyst/training" element={<MLTrainingDashboard />} /> */}
                <Route path="/analyst/political" element={<PoliticalAlpha />} />
                <Route path="/analyst/strategy" element={<StrategyDistillery />} />
                <Route path="/analyst/macro" element={<MacroDashboard />} />
                {/* Removed: <Route path="/analyst/assistant" element={<AIAssistantDashboard />} /> */}
                <Route path="/analyst/sentinel" element={<SentinelStrategyDashboard />} />

                <Route path="/data-scientist/predictions" element={<AIPredictionsDashboard />} />
                <Route path="/data-scientist/training" element={<MLTrainingDashboard />} />
                <Route path="/data-scientist/assistant" element={<AIAssistantDashboard />} />
                <Route path="/data-scientist/autocoder" element={<AutoCoderDashboard />} />
                <Route path="/data-scientist/sandbox" element={<AutoCoderSandbox />} />
                <Route path="/data-scientist/vr" element={<VRCockpit />} />
                <Route path="/data-scientist/debate" element={<DebateRoom />} />

                <Route path="/trader/scanner" element={<GlobalScanner />} />
                <Route path="/trader/options" element={<OptionsStrategyDashboard />} />
                <Route path="/trader/advanced-orders" element={<AdvancedOrdersDashboard />} />
                <Route path="/trader/algorithmic" element={<AlgorithmicTradingDashboard />} />
                <Route path="/trader/paper" element={<PaperTradingDashboard />} />
                <Route path="/trader/charting" element={<AdvancedChartingDashboard />} />
                <Route path="/trader/options-analytics" element={<OptionsAnalytics />} />

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

                 <Route path="/hunter/news" element={<NewsSentimentDashboard />} />
                 <Route path="/hunter/social" element={<SocialTradingDashboard />} />
                 <Route path="/hunter/forums" element={<CommunityForumsDashboard />} />
                 <Route path="/hunter/education" element={<EducationPlatformDashboard />} />
                 <Route path="/hunter/marketplace" element={<MarketplaceDashboard />} />
                 <Route path="/hunter/reports" element={<ResearchReportsDashboard />} />
                 <Route path="/hunter/alerts" element={<WatchlistsAlertsDashboard />} />

                <Route path="/legal/compliance" element={<ComplianceDashboard />} />
                <Route path="/legal/audit" element={<AuditDashboard />} />
                <Route path="/legal/scenarios" element={<ScenarioDashboard />} />

                {/* --- SECURE ADMIN ROUTES --- */}
                <Route path="/dept/admin" element={
                  <AuthGuard onShowLogin={() => setIsAuthModalOpen(true)} requiredRole="admin">
                    <AdminPage />
                  </AuthGuard>
                } />
                
                <Route path="/admin/*" element={
                  <AuthGuard onShowLogin={() => setIsAuthModalOpen(true)} requiredRole="admin">
                    <Routes>
                      <Route index element={<AdminDashboard />} />
                      <Route path="event-bus" element={<EventBusMonitor />} />
                      <Route path="storage" element={<StorageManager />} />
                      <Route path="graph" element={<GraphBrowser />} />
                      <Route path="logs" element={<LogViewer />} />
                      <Route path="health" element={<ServiceHealthGrid />} />
                      <Route path="middleware" element={<MiddlewarePipeline />} />
                      <Route path="performance" element={<MonitoringDashboard />} />
                      <Route path="alerts" element={<AlertConfigPage />} />
                      <Route path="deployments" element={<DeploymentController />} />
                      <Route path="ops" element={<OperationsDashboard />} />
                      <Route path="workspaces" element={<WorkspaceManager />} />
                      <Route path="features" element={<FeatureFlagManager />} />
                      <Route path="data-pipeline-manager" element={<DataPipelineManager />} />
                      <Route path="connections" element={<APIConnectorHub />} />
                      <Route path="external-data" element={<ExternalDataSources />} />
                      <Route path="webhooks" element={<WebhookReceiver />} />
                      <Route path="data-quality" element={<DataQualityDashboard />} />
                      <Route path="agents/fleet" element={<AgentFleetOverview />} />
                      <Route path="agents/tasks" element={<AgentTaskQueue />} />
                      <Route path="agents/logs" element={<AgentLogsViewer />} />
                      <Route path="env" element={<EnvironmentSettings />} />
                      <Route path="autocoder" element={<AutoCoderDashboard />} />
                      <Route path="order-management" element={<OrderManagementSystem />} />
                      <Route path="risk-limits" element={<RiskLimitManager />} />
                      <Route path="compliance-tracker" element={<ComplianceTracker />} />
                      <Route path="data-validation" element={<DataValidation />} />
                      <Route path="reconciliation" element={<ReconciliationDashboard />} />
                      <Route path="treasury" element={<TreasuryDashboard />} />
                      <Route path="portfolio-overview" element={<PortfolioOverview />} />
                      <Route path="crypto-wallet" element={<CryptoWalletPage />} />
                      <Route path="executive-summary" element={<ExecSummaryPage />} />
                      <Route path="crash-simulator" element={<CrashSimulator />} />
                      <Route path="tactical-command-center" element={<TacticalCommandCenter />} />
                      <Route path="pricing-verifier" element={<PricingVerifier />} />
                      <Route path="source-reputation" element={<SourceReputation />} />
                      <Route path="quality-incidents" element={<QualityIncidents />} />
                      <Route path="discrepancy-resolution" element={<DiscrepancyResolution />} />
                      <Route path="transaction-ledger" element={<TransactionLedger />} />
                      <Route path="transfer-center" element={<TransferCenter />} />
                      <Route path="tax-harvester" element={<TaxHarvester />} />
                      <Route path="tax-liability" element={<TaxLiabilityDashboard />} />
                      <Route path="expense-manager" element={<ExpenseManager />} />
                      <Route path="yield-optimizer" element={<YieldOptimizer />} />
                      <Route path="trust-admin" element={<TrustAdmin />} />
                      <Route path="donation-manager" element={<DonationManager />} />
                      <Route path="philanthropy-center" element={<PhilanthropyCenter />} />
                      <Route path="succession-modeler" element={<SuccessionModeler />} />
                      <Route path="/estate-visualizer" element={<EstateVisualizer />} />
                      <Route path="gifting-optimizer" element={<GiftingOptimizer />} />
                      <Route path="black-swan-generator" element={<BlackSwanGenerator />} />
                      <Route path="war-game-arena" element={<WarGameArena />} />
                      <Route path="robustness-lab" element={<RobustnessLab />} />
                    </Routes>
                  </AuthGuard>
                } />
                <Route path="/hunter/news" element={<NewsAggregator />} />
                <Route path="/social/sentiment" element={<SocialSentimentRadar />} />
                <Route path="/hunter/social-trading" element={<SocialTradingFeed />} />
                <Route path="/hunter/rumors" element={<RumorMill />} />
                <Route path="/data-scientist/research-workspace" element={<ResearchWorkspace />} />
                <Route path="/data-scientist/factor-analysis" element={<FactorAnalysisSuite />} />
                <Route path="/data-scientist/fundamental-scanner" element={<FundamentalScanner />} />
                <Route path="/data-scientist/quant-backtest" element={<QuantBacktestLab />} />
                <Route path="/data-scientist/advanced-charting" element={<AdvancedChartBuilder />} />
                <Route path="/data-scientist/heatmap" element={<HeatmapGenerator />} />
                <Route path="/data-scientist/debate" element={<DebateArena />} />
                <Route path="/data-scientist/debate-history" element={<DebateHistory />} />
                <Route path="/admin/autocoder" element={<AutoCoderDashboard />} />
                <Route path="/autocoder/dashboard" element={<AutoCoderDashboard />} />
                <Route path="/admin/executive-summary" element={<Navigate to="/admin/executive-summary" replace />} />

                {/* --- Special Routes --- */}
                <Route path="/special/scrum" element={<ScrumMaster />} />
                <Route path="/special/mobile" element={<MobileDashboard />} />
                <Route path="/special/vr" element={<VRCockpit />} />
                <Route path="/special/mission-control" element={<MissionControl />} />
                <Route path="/special/homeostasis" element={<Homeostasis />} />
                <Route path="/special/terminal" element={<TerminalWorkspace handleViewSource={() => { }} globalLock={globalLock} isDarkMode={isDark} widgetStates={widgetStates} setWidgetStates={setWidgetStates} widgetVisibility={widgetVisibility} setWidgetVisibility={setWidgetVisibility} />} />
                <Route path="/special/political" element={<PoliticalAlpha />} />
                <Route path="/special/strategy" element={<StrategyDistillery />} />
                <Route path="/special/debate" element={<DebateRoom />} />
                <Route path="/special/paper" element={<PaperTradingDashboard />} />
                <Route path="/special/zen" element={<ZenMode />} />
                <Route path="/special/missions" element={<MissionsOverview />} />
                <Route path="/special/search" element={<GlobalSearchPage />} />
                <Route path="/special/command" element={<CommandCenter />} />
                <Route path="/special/venn" element={<VennIntersectionView />} />
                <Route path="/missions" element={<Navigate to="/special/missions" replace />} />
                
                {/* --- Agent Department Routes --- */}
                <Route path="/dept" element={<Navigate to="/special/scrum" replace />} />
                <Route path="/scrum" element={<Navigate to="/special/scrum" replace />} />
                <Route path="/dept/scrum-master" element={<Navigate to="/special/scrum" replace />} />
                <Route path="/dept/venn" element={<VennIntersectionView />} />
                <Route path="/dept/orchestrator" element={<OrchestratorPage />} />

                <Route path="/dept/architect" element={<ArchitectPage />} />
                <Route path="/dept/data-scientist" element={<DataScientistPage />} />
                <Route path="/dept/strategist" element={<StrategistPage />} />
                <Route path="/dept/trader" element={<TraderPage />} />
                <Route path="/dept/physicist" element={<PhysicistPage />} />
                <Route path="/dept/hunter" element={<HunterPage />} />
                <Route path="/dept/sentry" element={<SentryPage />} />
                <Route path="/dept/steward" element={<StewardPage />} />
                <Route path="/dept/guardian" element={<GuardianPage />} />
                <Route path="/dept/lawyer" element={<LawyerPage />} />
                <Route path="/dept/auditor" element={<AuditorPage />} />
                <Route path="/dept/envoy" element={<EnvoyPage />} />
                <Route path="/dept/front-office" element={<FrontOfficePage />} />
                <Route path="/dept/historian" element={<HistorianPage />} />
                <Route path="/dept/stress-tester" element={<StressTesterPage />} />
                <Route path="/dept/refiner" element={<RefinerPage />} />
                <Route path="/dept/banker" element={<BankerPage />} />

                {/* --- Dynamic Workstation Routes --- */}
                <Route path="/:deptSlug/:subSlug" element={<DynamicWorkstation />} />

                {/* --- Catch-All Sub-Module Route --- */}
                <Route path="/:deptId/:subPage" element={<SubPageBoilerplate />} />

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


        {/* Window Manager Layer - conditionally rendered but hook called unconditionally above */}
        {!isAuthModalOpen && currentUser && windowIds.length > 0 && (
          <>
            {windowIds.map((id) => (
                <WindowWrapper key={id} id={id} />
            ))}
            <Taskbar />
          </>
        )}
        {!isAuthModalOpen && currentUser && windowIds.length === 0 && <Taskbar />}
        
        {/* Command Palette (Ctrl+K) */}
        <CommandPalette 
          isOpen={commandPaletteOpen} 
          onClose={() => setCommandPaletteOpen(false)}
          onThemeToggle={toggleTheme}
        />
        
        {/* Mobile Bottom Nav */}
        {!isAuthModalOpen && currentUser && <BottomNav />}
        
        {/* Quick Actions FAB */}
        {!isAuthModalOpen && currentUser && (
          <QuickActions 
            onAction={(actionId) => {
              switch(actionId) {
                case 'trade': setTradeModal({ open: true, details: { symbol: 'SPY', side: 'BUY', quantity: 10, price: 480 }}); break;
                case 'settings': navigate('/settings'); break;
                default: console.log('Quick action:', actionId);
              }
            }}
          />
        )}

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
        {!isAuthModalOpen && currentUser && <TimelineScrubber />}
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
