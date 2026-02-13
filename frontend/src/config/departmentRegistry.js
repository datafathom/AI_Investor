/**
 * Department Registry - Static configuration for all 18 departments
 * 
 * Maps departments to:
 * - Existing MenuBar.jsx route categories
 * - D3 visualization types
 * - Kafka topic subscriptions
 * - Agent IDs
 */

export const QUADRANTS = {
  ATTACK: 'ATTACK',
  DEFENSE: 'DEFENSE',
  HOUSEHOLD: 'HOUSEHOLD',
  META: 'META'
};

export const PARENT_ROLES = {
  ORCHESTRATOR: 'Orchestrator',
  ARCHITECT: 'Architect',
  DATA_SCIENTIST: 'Data Scientist',
  STRATEGIST: 'Strategist',
  TRADER: 'Trader',
  GUARDIAN: 'Guardian',
  LAWYER: 'Lawyer',
  AUDITOR: 'Auditor',
  ENVOY: 'Envoy',
  HUNTER: 'Hunter',
  SENTRY: 'Sentry',
  PHYSICIST: 'Physicist',
  STEWARD: 'Steward'
};

export const D3_TYPES = {
  FORCE_GRAPH: 'force-directed',
  SUNBURST: 'sunburst',
  SANKEY: 'sankey',
  RADIAL_TREE: 'radial-tree',
  THREE_D_SURFACE: '3d-surface',
  GLOBE_MESH: 'globe-mesh',
  TIMELINE: 'timeline',
  FLOWCHART: 'flowchart',
  FRACTAL: 'fractal',
  BUBBLE_CHART: 'bubble-chart'
};

export const DEPT_REGISTRY = {
  1: {
    id: 1,
    name: "The Orchestrator",
    shortName: "Orchestrator",
    slug: "orchestrator",
    route: "/dept/orchestrator",
    menuCategory: "Orchestrator",
    icon: "cpu",
    color: "#00f2ff",
    quadrant: QUADRANTS.META,
    parentRole: PARENT_ROLES.ORCHESTRATOR,
    d3Type: D3_TYPES.FORCE_GRAPH,
    description: "System coordination and agent orchestration",
    kafkaTopics: ["dept.1.events", "dept.1.metrics", "dept.1.agents"],
    agents: [
      "synthesizer",
      "command_interpreter", 
      "traffic_controller",
      "layout_morphologist",
      "red_team_sentry",
      "context_weaver"
    ],
    primaryMetric: "systemLatency",
    primaryMetricLabel: "System Latency",
    primaryMetricUnit: "ms",
    workflows: [
      { id: 'command_interpreter', label: 'Command Interpreter', icon: 'terminal', action: 'invoke_agent', agentId: 'command_interpreter' },
      { id: 'kill_switch', label: 'Emergency Kill-Switch', icon: 'power', action: 'system_halt', variant: 'danger' }
    ],
    subModules: [
      { path: "/special/terminal", label: "Terminal Workspace", description: "Multi-pane window manager for snapping widgets." },
      { path: "/special/mission-control", label: "Mission Control", description: "Real-time status of streams, health, and latencies." },
      { path: "/special/homeostasis", label: "Total Homeostasis", description: "Singular high-fidelity visualization of liquidity vs debt." },
      { path: "/special/command", label: "Global Command", description: "Natural language command bar for cross-role actions." },
      { path: "/special/venn", label: "Role Morphing", description: "Venn Diagram controller to blend role lenses." },
      { path: "/orchestrator/graph", label: "Dependency Graph", description: "Visual explorer of Neo4j nodes and goal impacts." },
      { path: "/special/search", label: "Global Search Bar", description: "Spotlight search for any transaction or document." },
      { path: "/orchestrator/permissions", label: "Role Permissions", description: "Defining action boundaries for different personas." },
      { path: "/orchestrator/layout", label: "Custom Layout Engine", description: "Drag-and-drop dashboard builder for saved workspaces." }
    ]
  },
  2: {
    id: 2,
    name: "The Architect",
    shortName: "Architect",
    slug: "architect",
    route: "/dept/architect",
    menuCategory: "Architect",
    icon: "drafting-compass",
    color: "#3b82f6",
    quadrant: QUADRANTS.META,
    parentRole: PARENT_ROLES.ARCHITECT,
    d3Type: D3_TYPES.SUNBURST,
    description: "40-year financial life planning",
    kafkaTopics: ["dept.2.events", "dept.2.metrics", "dept.2.agents"],
    agents: [
      "life_cycle_modeler",
      "tax_location_optimizer",
      "inheritance_logic_agent",
      "inflation_architect",
      "real_estate_amortizer",
      "goal_priority_arbiter"
    ],
    primaryMetric: "onTrackPercent",
    primaryMetricLabel: "On Track",
    primaryMetricUnit: "%",
    workflows: [
      { id: 'modeller', label: 'Life-Cycle Modeler', icon: 'activity', action: 'invoke_agent', agentId: 'life_cycle_modeler' },
      { id: 'goal_slider', label: 'Goal Priority Slider', icon: 'sliders', action: 'invoke_agent', agentId: 'goal_priority_arbiter' }
    ],
    subModules: [
      { path: "/architect/goals", label: "Goal Setting & Milestones", description: "4D timeline for major financial lifecycle flags." },
      { path: "/architect/allocation", label: "Asset Allocation Modeler", description: "Target-state builder for portfolio distribution." },
      { path: "/architect/blueprints", label: "Master Blueprints", description: "Mapping long-term financial goals to agent task graphs." },
      { path: "/architect/vault", label: "Insurance & Protection", description: "Centralized UI for policy limits and digital keys." },
      { path: "/architect/vault", label: "Insurance & Protection", description: "Centralized UI for policy limits and digital keys." },
      { path: "/architect/legacy", label: "Estate & Legacy Planner", description: "Mapping asset distribution and ICE checklists." },
      { path: "/architect/liability", label: "Liability Structuralist", description: "Deep-dive interface for debt interest snowballs." },
      { path: "/architect/tax", label: "Tax Efficiency Blueprint", description: "Account-level asset placement for max growth." },
      { path: "/architect/inflation", label: "Inflation Adjuster", description: "Global toggle to see future values in today's dollars." },
      { path: "/architect/retirement", label: "Retirement Drawdown", description: "Year-by-year plan for account depletion sequences." },
      { path: "/architect/capex", label: "CapEx Planner", description: "Planning for big hits like roofs, weddings, and cars." }
    ]
  },
  3: {
    id: 3,
    name: "The Data Scientist",
    shortName: "Data Scientist",
    slug: "data-scientist",
    route: "/dept/data-scientist",
    menuCategory: "Data Scientist",
    icon: "brain",
    color: "#8b5cf6",
    quadrant: QUADRANTS.ATTACK,
    parentRole: PARENT_ROLES.DATA_SCIENTIST,
    d3Type: D3_TYPES.FORCE_GRAPH,
    description: "Market intelligence and statistical analysis",
    kafkaTopics: ["dept.3.events", "dept.3.metrics", "dept.3.agents"],
    agents: [
      "scraper_general",
      "backtest_autopilot",
      "correlation_detective",
      "anomaly_scout",
      "yield_optimizer",
      "macro_correlation_engine"
    ],
    primaryMetric: "modelConfidence",
    primaryMetricLabel: "Model Confidence",
    primaryMetricUnit: "%",
    workflows: [
      { id: 'backtest', label: 'Backtest Autopilot', icon: 'play-circle', action: 'invoke_agent', agentId: 'backtest_autopilot' },
      { id: 'anomaly', label: 'Anomaly Toggle', icon: 'eye', action: 'invoke_agent', agentId: 'anomaly_scout' }
    ],
    subModules: [
      { path: "/data-scientist/research", label: "Data Research & Scraping", description: "Monitoring macro-economic indicators and holdings impact." },
      { path: "/data-scientist/debate-arena", label: "Debate Arena", description: "Agent-to-agent conflict resolution and consensus building." },
      { path: "/data-scientist/debate-history", label: "Debate History", description: "Audit trail of historical agent debates and transcripts." },
      { path: "/data-scientist/forced-sellers", label: "Forced Seller Monitor", description: "Identifying institutional liquidation pressure points." },
      { path: "/data-scientist/whale-flow", label: "Whale Flow Terminal", description: "Tracking large block trades and institutional accumulation." },
      { path: "/data-scientist/indicators", label: "Technical Indicators", description: "Advanced quant metrics and signal oscillators." },
      { path: "/data-scientist/backtest", label: "Backtest Lab", description: "Sandbox for running historical replay on strategies." },
      { path: "/data-scientist/correlation", label: "Correlation Matrix", description: "Heatmap showing hidden asset movement clusters." },
      { path: "/data-scientist/sentiment", label: "Sentiment Engine", description: "Visualization of social and news heat around sectors." },
      { path: "/data-scientist/social-sentiment-radar", label: "Social Sentiment Radar", description: "Real-time heatmaps for social media alpha." },
      { path: "/data-scientist/anomaly", label: "Anomaly Detection", description: "Highlighting spending spikes or standard deviation breaks." },
      { path: "/data-scientist/yield", label: "Yield Curve Analysis", description: "Tracking risk-free rates for market timing." },
      { path: "/data-scientist/arbitrage", label: "Stat-Arb Finder", description: "Searching for discrepancies in related assets." },
      { path: "/data-scientist/factor-analysis-suite", label: "Factor Analysis Suite", description: "Decomposing returns into growth, value, and momentum." },
      { path: "/data-scientist/fundamental-scanner", label: "Fundamental Scanner", description: "Screening assets based on balance sheet health." },
      { path: "/data-scientist/quant-backtest-lab", label: "Quant Backtest Lab", description: "High-precision simulation for algorithmic models." },
      { path: "/data-scientist/integrator", label: "External Data Integrator", description: "UI to import non-standard CSV/JSON financial sources." }
    ]
  },
  4: {
    id: 4,
    name: "The Strategist",
    shortName: "Strategist",
    slug: "strategist",
    route: "/dept/strategist",
    menuCategory: "Strategist",
    icon: "target",
    color: "#06b6d4",
    quadrant: QUADRANTS.ATTACK,
    parentRole: PARENT_ROLES.STRATEGIST,
    d3Type: D3_TYPES.FLOWCHART,
    description: "Trading logic and playbook management",
    kafkaTopics: ["dept.4.events", "dept.4.metrics", "dept.4.agents"],
    agents: [
      "logic_architect",
      "stress_tester",
      "rebalance_bot",
      "opportunity_screener",
      "edge_decay_monitor",
      "playbook_evolutionist"
    ],
    primaryMetric: "strategySuccessRate",
    primaryMetricLabel: "Success Rate",
    primaryMetricUnit: "%",
    workflows: [
      { id: 'stress_test', label: 'Stress-Tester', icon: 'zap', action: 'invoke_agent', agentId: 'stress_tester' },
      { id: 'rebalance', label: 'Rebalance Bot', icon: 'refresh-ccw', action: 'invoke_agent', agentId: 'rebalance_bot' }
    ],
    subModules: [
      { path: "/strategist/builder", label: "Strategy Builder", description: "Logic-flow UI (Visual Programming) to define entry/exit rules." },
      { path: "/strategist/risk", label: "Risk Management", description: "Hard Limit center for daily loss and stop-losses." },
      { path: "/strategist/screener", label: "Opportunity Screener", description: "Real-time filter for assets meeting strategy criteria." },
      { path: "/strategist/stress-test", label: "Scenario Stress Test", description: "What-If simulator for market drops or volatility spikes." },
      { path: "/strategist/rebalance", label: "Rebalancing Engine", description: "Compare target allocation to reality and fix drift." },
      { path: "/strategist/alpha-beta", label: "Alpha/Beta Decomposition", description: "Source analysis: Skill Gains vs. Market Lift." },
      { path: "/strategist/hub", label: "Signal Confirmation Hub", description: "Green/Red checklist before execution is unlocked." },
      { path: "/strategist/decay", label: "Strategy Decay Monitor", description: "Tracking if an old strategy is losing its edge." },
      { path: "/strategist/library", label: "Playbook Library", description: "Wiki of past strategies and retirement reasoning." }
    ]
  },
  5: {
    id: 5,
    name: "The Trader",
    shortName: "Trader",
    slug: "trader",
    route: "/dept/trader",
    menuCategory: "Trader",
    icon: "trending-up",
    color: "#22c55e",
    quadrant: QUADRANTS.ATTACK,
    parentRole: PARENT_ROLES.TRADER,
    d3Type: D3_TYPES.BUBBLE_CHART,
    description: "Order execution and position management",
    kafkaTopics: ["dept.5.events", "dept.5.metrics", "dept.5.agents"],
    agents: [
      "sniper",
      "exit_manager",
      "arbitrageur",
      "liquidity_scout",
      "position_sizer",
      "flash_crash_circuit_breaker"
    ],
    primaryMetric: "executionLatency",
    primaryMetricLabel: "Execution Latency",
    primaryMetricUnit: "ms",
    workflows: [
      { id: 'sniper', label: 'Sniper', icon: 'crosshair', action: 'invoke_agent', agentId: 'sniper' },
      { id: 'exit_mgr', label: 'Exit Manager', icon: 'log-out', action: 'invoke_agent', agentId: 'exit_manager' },
      { id: 'pos_sizer', label: 'Position Sizer', icon: 'maximize', action: 'invoke_agent', agentId: 'position_sizer' }
    ],
    subModules: [
      { path: "/trader/execution", label: "Manual Execution Hub", description: "Manual order entry terminal with direct-to-exchange routing." },
      { path: "/trader/monitor", label: "Market Monitor", description: "High-refresh multi-charting with technical overlays." },
      { path: "/trader/monitor", label: "Market Monitor", description: "High-refresh multi-charting with technical overlays." },
      { path: "/trader/options", label: "Options Chain (Adv)", description: "Advanced UI for 2, 3, and 4-leg derivatives strategies." },
      { path: "/trader/depth", label: "Market Depth & L2", description: "Visual representation of the institutional limit order book." },
      { path: "/trader/pad", label: "Execution Pad", description: "Hot-Key driven system for ultra-fast order placement." },
      { path: "/trader/tape", label: "Trade Tape", description: "Live, scrolling feed of every executed trade and status." },
      { path: "/trader/zen", label: "Zen Mode", description: "Distraction-free UI showing only price and at-risk P&L." },
      { path: "/trader/ladder", label: "Ladder Interface", description: "Vertical price-ladder for precise futures order placement." },
      { path: "/trader/slippage", label: "Slippage Estimator", description: "Real-time cost calculator for bid-ask spreads." },
      { path: "/trader/routing", label: "Multi-Route Gateway", description: "Broker-agnostic execution path selector for best fills." }
    ]
  },
  6: {
    id: 6,
    name: "The Physicist",
    shortName: "Physicist",
    slug: "physicist",
    route: "/dept/physicist",
    menuCategory: "Strategist",
    icon: "atom",
    color: "#a855f7",
    quadrant: QUADRANTS.ATTACK,
    parentRole: PARENT_ROLES.PHYSICIST,
    d3Type: D3_TYPES.THREE_D_SURFACE,
    description: "Options Greeks and derivatives math",
    kafkaTopics: ["dept.6.events", "dept.6.metrics", "dept.6.agents"],
    agents: [
      "theta_collector",
      "volatility_surface_mapper",
      "gamma_warning_system",
      "delta_hedger",
      "probability_modeler",
      "black_swan_insurance_agent"
    ],
    primaryMetric: "thetaDecayPerHour",
    primaryMetricLabel: "Theta Decay",
    primaryMetricUnit: "$/hr",
    workflows: [
      { id: 'theta', label: 'Theta Collector', icon: 'clock', action: 'invoke_agent', agentId: 'theta_collector' },
      { id: 'delta', label: 'Delta Hedger', icon: 'shield', action: 'invoke_agent', agentId: 'delta_hedger' }
    ],
    subModules: [
      { path: "/physicist/margin", label: "Margin Compression", description: "Monitoring volatility expansion impacts on capital." },
      { path: "/physicist/morphing", label: "Strategy Morphing", description: "Morphing losing spreads into different complex structures." },
      { path: "/physicist/expected-move", label: "Expected Move", description: "Standard deviation cones for 30-day price projections." }
    ]
  },
  7: {
    id: 7,
    name: "The Hunter",
    shortName: "Hunter",
    slug: "hunter",
    route: "/dept/hunter",
    menuCategory: "Trader",
    icon: "crosshair",
    color: "#f97316",
    quadrant: QUADRANTS.ATTACK,
    parentRole: PARENT_ROLES.HUNTER,
    d3Type: D3_TYPES.BUBBLE_CHART,
    description: "Alpha discovery and moonshot tracking",
    kafkaTopics: ["dept.7.events", "dept.7.metrics", "dept.7.agents"],
    agents: [
      "deal_flow_scraper",
      "cap_table_modeler",
      "exit_catalyst_monitor",
      "lotto_risk_manager",
      "whitepaper_summarizer",
      "asset_hunter"
    ],
    primaryMetric: "signalHitRate",
    primaryMetricLabel: "Hit Rate",
    primaryMetricUnit: "%",
    workflows: [
      { id: 'whale', label: 'Whale Watcher', icon: 'eye', action: 'invoke_agent', agentId: 'asset_hunter' },
      { id: 'sentiment', label: 'Sentiment Engine', icon: 'bar-chart-2', action: 'invoke_agent', agentId: 'deal_flow_scraper' }
    ],
    subModules: [
      { path: "/hunter/pipeline", label: "Venture Pipeline", description: "Tracking Pre-seed or Private Equity ops before market hit." },
      { path: "/hunter/cap-tables", label: "Early Stage Cap Tables", description: "Visualizing ownership percentage and dilution in private startups." },
      { path: "/hunter/pulse", label: "Market Pulse", description: "Global heatmap of liquidity and volatility clusters." },
      { path: "/hunter/unusual-options", label: "Whale Radar", description: "Scanning for massive block trades and unusual IV spikes." },
      { path: "/hunter/news-aggregator", label: "News Aggregator", description: "Live terminal of financial breaking news and agency feeds." },
      { path: "/hunter/social-trading-feed", label: "Social Trading Feed", description: "Monitoring top-performing social traders and copy-wallets." },
      { path: "/hunter/rumor-mill", label: "Rumor Mill", description: "Natural language processing of social rumors and forum chatter." },
      { path: "/hunter/moonshots", label: "Moonshot Tracker", description: "High-volatility P&L for Lotto Ticket trades (Crypto/Pennies)." },
      { path: "/hunter/ipo-monitor", label: "Waitlist/IPO Monitor", description: "Tracking companies before Day 0 public entries." },
      { path: "/hunter/collectibles", label: "Collectibles Exchange", description: "Tracking fractional ownership in Art, Wine, or Luxury assets." },
      { path: "/hunter/crowdfunding", label: "Crowdfunding Ledger", description: "Managing investments across Republic/Wefunder platforms." },
      { path: "/hunter/exits", label: "Exit Strategy Modeler", description: "Defining Success Milestones for 10x winners." },
      { path: "/hunter/rumors", label: "Speculative News", description: "Aggregator for rumors, FDA approvals, and earnings leaks." },
      { path: "/hunter/mining", label: "Resource Mining", description: "Tracking physical/digital gold, silver, and commodities." }
    ]
  },
  8: {
    id: 8,
    name: "The Sentry",
    shortName: "Sentry",
    slug: "sentry",
    route: "/dept/sentry",
    menuCategory: "Guardian",
    icon: "shield",
    color: "#ef4444",
    quadrant: QUADRANTS.DEFENSE,
    parentRole: PARENT_ROLES.SENTRY,
    d3Type: D3_TYPES.GLOBE_MESH,
    description: "Cybersecurity and perimeter defense",
    kafkaTopics: ["dept.8.events", "dept.8.metrics", "dept.8.agents"],
    agents: [
      "breach_sentinel",
      "api_key_rotator",
      "travel_mode_guard",
      "cold_storage_auditor",
      "permission_auditor",
      "recovery_path_builder"
    ],
    primaryMetric: "threatLevel",
    primaryMetricLabel: "Threat Level",
    primaryMetricUnit: "",
    workflows: [
      { id: 'blackout', label: 'Visual Blackout', icon: 'eye-off', action: 'invoke_agent', agentId: 'breach_sentinel', variant: 'danger' },
      { id: 'rotate', label: 'Credential Rotator', icon: 'key', action: 'invoke_agent', agentId: 'api_key_rotator' }
    ],
    subModules: [
      { path: "/sentry/vault", label: "Credential Vault", description: "MFA management and hardware key status for all institutions." },
      { path: "/sentry/encryption", label: "Encryption Status", description: "Encryption health of Postgres and Neo4j databases." },
      { path: "/sentry/firewall", label: "Logical Firewall", description: "Monitoring port activity and unknown request patterns." },
      { path: "/sentry/dark-web", label: "Dark Web Monitor", description: "Checking for email/account numbers in known data breaches." },
      { path: "/sentry/dark-web", label: "Dark Web Monitor", description: "Checking for email/account numbers in known data breaches." },
      { path: "/sentry/devices", label: "Device Authorization", description: "List of computers/phones with Key access to the app." },
      { path: "/sentry/geo-logs", label: "IP Access Logs", description: "Geographical map of login attempts for bank/brokerages." },
      { path: "/sentry/kill-switch", label: "Emergency Kill Protocol", description: "One-click revocation of all API tokens and handshakes." },
      { path: "/sentry/backups", label: "Backup Integrity", description: "Monitoring the health and age of offline data backups." },
      { path: "/sentry/hardware", label: "Hardware Wallet Bridge", description: "Connecting cold storage devices for View-only modes." },
      { path: "/sentry/audit", label: "Perimeter Audit", description: "Checking health of environment running the GUI." }
    ]
  },
  9: {
    id: 9,
    name: "The Steward",
    shortName: "Steward",
    slug: "steward",
    route: "/dept/steward",
    menuCategory: "Guardian",
    icon: "home",
    color: "#84cc16",
    quadrant: QUADRANTS.HOUSEHOLD,
    parentRole: PARENT_ROLES.STEWARD,
    d3Type: D3_TYPES.SUNBURST,
    description: "Physical assets and lifestyle management",
    kafkaTopics: ["dept.9.events", "dept.9.metrics", "dept.9.agents"],
    agents: [
      "property_manager",
      "vehicle_fleet_ledger",
      "inventory_agent",
      "procurement_bot",
      "wellness_sync",
      "maintenance_scheduler"
    ],
    primaryMetric: "costOfLiving",
    primaryMetricLabel: "Cost of Living",
    primaryMetricUnit: "$/mo",
    workflows: [
      { id: 'inventory', label: 'Inventory Agent', icon: 'package', action: 'invoke_agent', agentId: 'inventory_agent' },
      { id: 'wellness', label: 'Wellness Sync', icon: 'heart', action: 'invoke_agent', agentId: 'wellness_sync' }
    ],
    subModules: [
      { path: "/steward/maintenance", label: "Maintenance Reserve", description: "Sunken Fund calculator for home and car repairs." },
      { path: "/steward/kill-list", label: "Subscription Kill-List", description: "Monthly report on unused services and tools." },
      { path: "/steward/liquidity", label: "Net Worth vs Liquid", description: "Visualizing the gap between wealth and spendable cash." }
    ]
  },
  10: {
    id: 10,
    name: "The Guardian",
    shortName: "Guardian",
    slug: "guardian",
    route: "/dept/guardian",
    menuCategory: "Guardian",
    icon: "shield-check",
    color: "#14b8a6",
    quadrant: QUADRANTS.DEFENSE,
    parentRole: PARENT_ROLES.GUARDIAN,
    d3Type: D3_TYPES.SANKEY,
    description: "Banking solvency and liquidity fortress",
    kafkaTopics: ["dept.10.events", "dept.10.metrics", "dept.10.agents"],
    agents: [
      "bill_automator",
      "flow_master",
      "budget_enforcer",
      "fraud_watchman",
      "subscription_assassin",
      "credit_score_sentinel"
    ],
    primaryMetric: "liquidityDays",
    primaryMetricLabel: "Days of Runway",
    primaryMetricUnit: "days",
    workflows: [
      { id: 'bill_pay', label: 'Bill Automator', icon: 'credit-card', action: 'invoke_agent', agentId: 'bill_automator' },
      { id: 'sweep', label: 'Sweep Bot', icon: 'navigation', action: 'invoke_agent', agentId: 'flow_master' }
    ],
    subModules: [
      { path: "/guardian/bills", label: "Bill Payment Center", description: "Managing institutional liabilities and automated outflows." },
      { path: "/guardian/loom", label: "The Loom (Transfers)", description: "Visual interface for node-to-node fund movements." },
      { path: "/guardian/loom", label: "The Loom (Transfers)", description: "Visual interface for node-to-node fund movements." },
      { path: "/guardian/budgeting", label: "Personal Budgeting", description: "Granular breakdown of Needs, Wants, and Investments." },
      { path: "/guardian/forecast", label: "Cash Flow Projection", description: "90-day weather forecast of institutional balances." },
      { path: "/guardian/fraud", label: "Security & Fraud", description: "Monitoring credit scores, card locks, and suspicious flags." },
      { path: "/guardian/emergency", label: "Emergency Fund", description: "Progress bar UI for funded months of safety net." },
      { path: "/guardian/ladder", label: "Liquidity Ladder", description: "Visualizing cash in tiers: Physical, Check, HYS, T-Bills." },
      { path: "/guardian/tax-buffer", label: "Tax-Safe Buffer", description: "Dedicated bucket for money belonging to the IRS." },
      { path: "/guardian/sweep", label: "Automated Sweep", description: "Rules to sweep checking excess into high-yield accounts." }
    ]
  },
  11: {
    id: 11,
    name: "The Lawyer",
    shortName: "Lawyer",
    slug: "lawyer",
    route: "/dept/lawyer",
    menuCategory: "Lawyer",
    icon: "scale",
    color: "#6b7280",
    quadrant: QUADRANTS.DEFENSE,
    parentRole: PARENT_ROLES.LAWYER,
    d3Type: D3_TYPES.RADIAL_TREE,
    description: "Legal entities and compliance",
    kafkaTopics: ["dept.11.events", "dept.11.metrics", "dept.11.agents"],
    agents: [
      "wash_sale_watchdog",
      "document_notary",
      "kyc_aml_compliance_agent",
      "tax_loss_harvester",
      "regulatory_news_ticker",
      "audit_trail_reconstructor"
    ],
    primaryMetric: "taxLiability",
    primaryMetricLabel: "Tax Liability",
    primaryMetricUnit: "$",
    workflows: [
      { id: 'tax_loss', label: 'Tax-Loss Harvester', icon: 'scissors', action: 'invoke_agent', agentId: 'tax_loss_harvester' },
      { id: 'wash_sale', label: 'Wash-Sale Monitor', icon: 'alert-triangle', action: 'invoke_agent', agentId: 'wash_sale_watchdog' }
    ],
    subModules: [
      { path: "/lawyer/logs", label: "Audit Logs", description: "Forensic, searchable timeline of every intent-based action." },
      { path: "/lawyer/library", label: "Precedent Library", description: "Database of past legal outcomes and relevant SEC filings." },
      { path: "/legal/144a-compliance", label: "SEC Rule 144A Compliance", description: "Tracking restricted securities and holding periods." },
      { path: "/lawyer/journal", label: "Trade Journaling", description: "Mandatory tagging for mental state and reasoning." },
      { path: "/lawyer/vault", label: "Document Vault", description: "Storage for loans, deeds, and terms of service PDFs." },
      { path: "/lawyer/harvest", label: "Tax Harvest Center", description: "Real-time view of unrealized losses for tax offsets." },
      { path: "/lawyer/wash-sale", label: "Wash Sale Monitor", description: "Prevention system for accidental early buy-backs." },
      { path: "/lawyer/regulation", label: "Regulatory Feed", description: "Legislation tracker for new tax or SEC rule impacts." },
      { path: "/lawyer/beneficiaries", label: "Beneficiary Sync", description: "Ensuring 401k/IRA/Life beneficiaries match the Will." },
      { path: "/lawyer/signatures", label: "Digital Signatures", description: "PDF generator for family contracts and agreements." },
      { path: "/lawyer/compliance", label: "Compliance Score", description: "0-100 rating of institutional audit readiness." }
    ]
  },
  12: {
    id: 12,
    name: "The Auditor",
    shortName: "Auditor",
    slug: "auditor",
    route: "/dept/auditor",
    menuCategory: "Lawyer",
    icon: "search",
    color: "#fbbf24",
    quadrant: QUADRANTS.DEFENSE,
    parentRole: PARENT_ROLES.AUDITOR,
    d3Type: D3_TYPES.SUNBURST,
    description: "Forensic analysis and truth-telling",
    kafkaTopics: ["dept.12.events", "dept.12.metrics", "dept.12.agents"],
    agents: [
      "slippage_sleuth",
      "behavioral_analyst",
      "benchmarker",
      "fee_forensic_agent",
      "reconciliation_bot",
      "mistake_classifier"
    ],
    primaryMetric: "feeLeakage",
    primaryMetricLabel: "Fee Leakage",
    primaryMetricUnit: "$",
    workflows: [
      { id: 'slippage', label: 'Slippage Sleuth', icon: 'search', action: 'invoke_agent', agentId: 'slippage_sleuth' },
      { id: 'benchmarker', label: 'Benchmarker', icon: 'trending-up', action: 'invoke_agent', agentId: 'benchmarker' }
    ],
    subModules: [
      { path: "/auditor/equity", label: "Equity Reconciliation", description: "Comparing internal ledgers against broker statements." },
      { path: "/auditor/fees", label: "Fee Leakage Auditor", description: "Identifying hidden costs or incorrect commission tiering." },
      { path: "/auditor/ledger", label: "Immutable Ledger", description: "Audit-ready view of all blockchain and internal entries." },
      { path: "/auditor/equity-curve", label: "Equity Curve Analytics", description: "Deep dive into net worth growth and trend lines." },
      { path: "/auditor/equity-curve", label: "Equity Curve Analytics", description: "Deep dive into net worth growth and trend lines." },
      { path: "/auditor/psychology", label: "Psychology Scorecard", description: "Grading rule adherence vs emotional 'Rogue' trading." },
      { path: "/auditor/attribution", label: "Performance Attribution", description: "Breakdown of profit sources (e.g. Tech vs Options)." },
      { path: "/auditor/mistakes", label: "Mistake Logger", description: "Wall of Learning for analyzed failure patterns." },
      { path: "/auditor/benchmarks", label: "The Benchmarker", description: "Comparative analysis against NASDAQ, Gold, or BTC." },
      { path: "/auditor/time-weighted", label: "Time-Weighted Returns", description: "Analyzing returns isolated from capital additions." },
      { path: "/auditor/recovery", label: "Fee Recovery", description: "Identifying bank fees that can be disputed or reversed." }
    ]
  },
  13: {
    id: 13,
    name: "The Envoy",
    shortName: "Envoy",
    slug: "envoy",
    route: "/dept/envoy",
    menuCategory: "Hunter",
    icon: "users",
    color: "#ec4899",
    quadrant: QUADRANTS.HOUSEHOLD,
    parentRole: PARENT_ROLES.ENVOY,
    d3Type: D3_TYPES.RADIAL_TREE,
    description: "Professional network and philanthropy",
    kafkaTopics: ["dept.13.events", "dept.13.metrics", "dept.13.agents"],
    agents: [
      "advisor_liaison",
      "subscription_negotiator",
      "family_office_coordinator",
      "philanthropy_scout",
      "professional_crm",
      "pitch_deck_generator"
    ],
    primaryMetric: "networkHealth",
    primaryMetricLabel: "Network Health",
    primaryMetricUnit: "%",
    workflows: [
      { id: 'philanthropy', label: 'Philanthropy Scout', icon: 'globe', action: 'invoke_agent', agentId: 'philanthropy_scout' },
      { id: 'crm', label: 'Professional CRM', icon: 'users', action: 'invoke_agent', agentId: 'professional_crm' }
    ],
    subModules: [
      { path: "/envoy/advisor", label: "Advisor Portal", description: "Read-Only view for sharing with CPA or Financial Advisor." },
      { path: "/envoy/pitch", label: "Public Pitch/Portfolio", description: "Clean view of successes for partners (hiding amounts)." },
      { path: "/envoy/inbox", label: "Strategic Inbox", description: "Centralized feed for high-level partner communications." },
      { path: "/envoy/contacts", label: "Professional Contacts", description: "CRM for Money Team: lawyers, accountants, brokers." },
      { path: "/envoy/contacts", label: "Professional Contacts", description: "CRM for Money Team: lawyers, accountants, brokers." },
      { path: "/envoy/subscriptions", label: "Subscription Manager", description: "Managing and firing unused tools and data feeds." },
      { path: "/envoy/family", label: "Family Office Hub", description: "Collaborative view for household budgets and goals." },
      { path: "/envoy/education", label: "Financial Education", description: "Curated library of books, videos, and influential notes." },
      { path: "/envoy/daf", label: "DAF Manager", description: "Managing Donor Advised Funds and tax-free growth." },
      { path: "/envoy/share", label: "External API Share", description: "Generating secret links for specific partner graph views." },
      { path: "/envoy/crm", label: "Professional CRM", description: "Tracking every interaction with the Money Team." }
    ]
  },
  14: {
    id: 14,
    name: "The Front Office",
    shortName: "Front Office",
    slug: "front-office",
    route: "/dept/front-office",
    menuCategory: "Hunter",
    icon: "briefcase",
    color: "#0ea5e9",
    quadrant: QUADRANTS.HOUSEHOLD,
    parentRole: PARENT_ROLES.ENVOY,
    d3Type: D3_TYPES.FORCE_GRAPH,
    description: "Admin support and HR functions",
    kafkaTopics: ["dept.14.events", "dept.14.metrics", "dept.14.agents"],
    agents: [
      "inbox_gatekeeper",
      "calendar_concierge",
      "voice_advocate",
      "logistics_researcher",
      "document_courier",
      "executive_buffer"
    ],
    primaryMetric: "pendingTasks",
    primaryMetricLabel: "Pending Tasks",
    primaryMetricUnit: "",
    workflows: [
      { id: 'voice', label: 'Voice Advocate', icon: 'phone', action: 'invoke_agent', agentId: 'voice_advocate' },
      { id: 'calendar', label: 'Calendar Concierge', icon: 'calendar', action: 'invoke_agent', agentId: 'calendar_concierge' }
    ],
    subModules: [
      { path: "/orchestrator/terminal", label: "Terminal Workspace", description: "Access the unified command line interface." },
      { path: "/orchestrator/mission-control", label: "Mission Control", description: "View the operational status of all systems." }
    ]
  },
  15: {
    id: 15,
    name: "The Historian",
    shortName: "Historian",
    slug: "historian",
    route: "/dept/historian",
    menuCategory: "Data Scientist",
    icon: "clock",
    color: "#78716c",
    quadrant: QUADRANTS.META,
    parentRole: PARENT_ROLES.DATA_SCIENTIST,
    d3Type: D3_TYPES.TIMELINE,
    description: "Decision quality and pattern analysis",
    kafkaTopics: ["dept.15.events", "dept.15.metrics", "dept.15.agents"],
    agents: [
      "journal_entry_agent",
      "regime_classifier",
      "ghost_decision_overlay",
      "pattern_recognition_bot",
      "decision_replay_engine",
      "timeline_curator"
    ],
    primaryMetric: "logicScore",
    primaryMetricLabel: "Logic Score",
    primaryMetricUnit: "%",
    workflows: [
      { id: 'journal', label: 'Journal Entry', icon: 'book', action: 'invoke_agent', agentId: 'journal_entry_agent' },
      { id: 'regime', label: 'Regime Classifier', icon: 'layers', action: 'invoke_agent', agentId: 'regime_classifier' }
    ],
    subModules: [
      { path: "/historian/replay", label: "Decision Replay", description: "Historical re-analysis of mental state vs reality." },
      { path: "/historian/regime", label: "Regime Matrix", description: "Classifying market environments and decision quality." },
      { path: "/historian/patterns", label: "Pattern Recognition", description: "Identifying recurring success/failure clusters." }
    ]
  },
  16: {
    id: 16,
    name: "The Stress-Tester",
    shortName: "Stress-Tester",
    slug: "stress-tester",
    route: "/dept/stress-tester",
    menuCategory: "Data Scientist",
    icon: "zap",
    color: "#dc2626",
    quadrant: QUADRANTS.META,
    parentRole: PARENT_ROLES.DATA_SCIENTIST,
    d3Type: D3_TYPES.FRACTAL,
    description: "Chaos simulation and robustness testing",
    kafkaTopics: ["dept.16.events", "dept.16.metrics", "dept.16.agents"],
    agents: [
      "war_game_simulator",
      "black_swan_randomizer",
      "liquidation_optimizer",
      "cascade_failure_detector",
      "recovery_path_planner",
      "robustness_scorer"
    ],
    primaryMetric: "robustnessPercent",
    primaryMetricLabel: "Robustness",
    primaryMetricUnit: "%",
    workflows: [
      { id: 'wargame', label: 'War Game Mode', icon: 'swords', action: 'invoke_agent', agentId: 'war_game_simulator', variant: 'danger' },
      { id: 'blackswan', label: 'Black Swan Randomizer', icon: 'shuffle', action: 'invoke_agent', agentId: 'black_swan_randomizer' }
    ],
    subModules: [
      { path: "/stress-tester/wargame", label: "War Game Simulator", description: "Extreme black swan simulations and cascade analysis." },
      { path: "/stress-tester/liquidation", label: "Liquidation Optimizer", description: "Planning exit paths for market-wide failures." },
      { path: "/stress-tester/robustness", label: "Robustness Scorecard", description: "FRACTAL analysis of portfolio survivability." }
    ]
  },
  17: {
    id: 17,
    name: "The Refiner",
    shortName: "Refiner",
    slug: "refiner",
    route: "/dept/refiner",
    menuCategory: "Architect",
    icon: "settings",
    color: "#7c3aed",
    quadrant: QUADRANTS.META,
    parentRole: PARENT_ROLES.ORCHESTRATOR,
    d3Type: D3_TYPES.FORCE_GRAPH,
    description: "Agent meta-optimization",
    kafkaTopics: ["dept.17.events", "dept.17.metrics", "dept.17.agents"],
    agents: [
      "hallucination_sentinel",
      "token_efficiency_reaper",
      "agent_performance_reviewer",
      "prompt_optimizer",
      "model_router",
      "context_window_manager"
    ],
    primaryMetric: "agentEfficiency",
    primaryMetricLabel: "Agent Efficiency",
    primaryMetricUnit: "%",
    workflows: [
      { id: 'tuning', label: 'Agent Tuning', icon: 'sliders', action: 'invoke_agent', agentId: 'prompt_optimizer' },
      { id: 'hallucination', label: 'Hallucination Sentinel', icon: 'shield-alert', action: 'invoke_agent', agentId: 'hallucination_sentinel' }
    ],
    subModules: [
      { path: "/refiner/efficiency", label: "Token Efficiency", description: "Monitoring reaper performance and context usage." },
      { path: "/refiner/hallucination", label: "Hallucination Monitor", description: "Sentinel status for LLM drift and fact-checking." },
      { path: "/refiner/prompts", label: "Prompt Evolution", description: "Optimization of agent baseline instructions." }
    ]
  },
  18: {
    id: 18,
    name: "The Banker",
    shortName: "Banker",
    slug: "banker",
    route: "/dept/banker",
    menuCategory: "Guardian",
    icon: "landmark",
    color: "#059669",
    quadrant: QUADRANTS.HOUSEHOLD,
    parentRole: PARENT_ROLES.GUARDIAN,
    d3Type: D3_TYPES.SANKEY,
    description: "Treasury and cash movement",
    kafkaTopics: ["dept.18.events", "dept.18.metrics", "dept.18.agents"],
    agents: [
      "transaction_categorizer",
      "ach_wire_tracker",
      "envelope_budget_manager",
      "recurring_payment_agent",
      "tax_reserve_calculator",
      "interest_arbitrage_scout"
    ],
    primaryMetric: "burnRatePerDay",
    primaryMetricLabel: "Burn Rate",
    primaryMetricUnit: "$/day",
    workflows: [
      { id: 'ledger', label: 'Transaction Ledger', icon: 'file-text', action: 'invoke_agent', agentId: 'transaction_categorizer' },
      { id: 'burn', label: 'Category Burn', icon: 'pie-chart', action: 'invoke_agent', agentId: 'envelope_budget_manager' }
    ],
    subModules: [
      { path: "/banker/ledger", label: "Ledger Reconciliation", description: "Verifying the graph against external bank records." },
      { path: "/banker/recovery", label: "Fee Recovery Tracker", description: "Identifying bank fees that can be disputed or reversed." },
      { path: "/banker/sweep", label: "Sweep Logic", description: "Configuring automated transfers between institutional nodes." }
    ]
  },
  19: {
    id: 19,
    name: "System Administration",
    shortName: "Admin",
    slug: "admin",
    route: "/dept/admin",
    menuCategory: "Admin",
    icon: "shield-check",
    color: "#ff0000",
    quadrant: QUADRANTS.META,
    parentRole: PARENT_ROLES.ORCHESTRATOR,
    minRole: "admin",
    d3Type: D3_TYPES.SUNBURST,
    description: "System-wide administrative controls and oversight",
    kafkaTopics: ["sys.admin.events", "sys.admin.metrics"],
    agents: ["admin_overseer"],
    primaryMetric: "uptime",
    primaryMetricLabel: "Sys Uptime",
    primaryMetricUnit: "%",
    subModules: [
      { path: "/dept/admin", label: "Admin Dashboard", description: "Centralized administrative control center." },
      { path: "/admin/logs", label: "System Logs Viewer", description: "Forensic logs and audit trail for all system events." },
      { path: "/admin/event-bus", label: "Event Bus Monitor", description: "Real-time visualization of Kafka/Redis message traffic." },
      { path: "/admin/storage", label: "Storage Manager", description: "Managing IDB, LocalStorage, and Cloud Sync states." },
      { path: "/admin/health", label: "Service Health Grid", description: "Live status of all microservices and background workers." },
      { path: "/admin/deployments", label: "Deployment Controller", description: "Hot-swap management for agent logic and UI updates." },
      { path: "/admin/fleet", label: "Agent Fleet Overview", description: "Status and lifecycle management for all active agents." },
      { path: "/admin/autocoder", label: "Auto-Coder Dashboard", description: "Self-improving logic and automated code generation." },
      { path: "/admin/system-health", label: "System Health Dashboard", description: "CPU, Memory, and Disk usage metrics for the OS." },
      { path: "/admin/executive-summary", label: "Executive Summary", description: "High-level overview of institutional health and alpha." },
      { path: "/admin/order-management", label: "Order Management System", description: "Live status of all active, pending, and filled orders." },
      { path: "/admin/portfolio-overview", label: "Portfolio Overview", description: "Consolidated view of all assets, exposures, and heat." },
      { path: "/admin/security-center", label: "Security Center", description: "Consolidated view of system vulnerabilities and threats." },
      { path: "/admin/treasury", label: "Treasury Dashboard", description: "Master view of all bank balances, yields, and liquidity." },
      { path: "/admin/reconciliation", label: "Reconciliation Dashboard", description: "Unified view of cash and position breaks." },
      { path: "/admin/transaction-ledger", label: "Transaction Ledger", description: "Master record of all system-wide financial movements." },
      { path: "/admin/deployments", label: "Red/Green/Blue Deploy", description: "Zero-downtime deployment controller." },
      { path: "/admin/features", label: "Feature Flag Management", description: "Hot-toggling system features and research modes." }
    ]
  }
};

// Helper exports
export const getDepartmentById = (id) => DEPT_REGISTRY[id];
export const getDepartmentBySlug = (slug) => 
  Object.values(DEPT_REGISTRY).find(d => d.route.includes(slug));
export const getDepartmentsByQuadrant = (quadrant) => 
  Object.values(DEPT_REGISTRY).filter(d => d.quadrant === quadrant);
export const getDepartmentsByMenuCategory = (category) => 
  Object.values(DEPT_REGISTRY).filter(d => d.menuCategory === category);
export const getDepartmentsByParentRole = (role) => 
  Object.values(DEPT_REGISTRY).filter(d => d.parentRole === role);
export const getAllDepartments = () => Object.values(DEPT_REGISTRY);
export const getAllAgentIds = () => 
  Object.values(DEPT_REGISTRY).flatMap(d => d.agents);

export default DEPT_REGISTRY;
