import React, { useState, useEffect } from 'react';
import { StorageService } from '../utils/storageService';
import { brokerageService } from '../services/brokerageService';
import { Responsive, WidthProvider } from 'react-grid-layout';
import { TrendingUp, DollarSign, Activity, PieChart, Wallet, Zap, AlertCircle } from 'lucide-react';
import { SimpleLineChart } from '../components/Charts/SimpleCharts';
import MarginTachometer from '../components/Brokerage/MarginTachometer';
import TaxLotOptimizer from '../components/Brokerage/TaxLotOptimizer';
import PLWaterfall from '../components/Brokerage/PLWaterfall';
import InstitutionalConnectorWidget from '../widgets/Brokerage/InstitutionalConnectorWidget';
import OrderExecutionStatus from '../components/AI_Investor/Execution/OrderExecutionStatus';
import SettlementDashboard from '../widgets/Brokerage/SettlementDashboard';
import './BrokerageAccount.css';

// New UI/UX Components
import { StatCard, ProgressBar, Badge, DataTable } from '../components/DataViz';
import { GlassCard } from '../components/Common';

const BrokerageAccount = () => {
    const [summary, setSummary] = useState(brokerageService.getAccountSummary());
    const [equityData, setEquityData] = useState(generateMockEquity());

    useEffect(() => {
        const unsubscribe = brokerageService.subscribe((event) => {
            if (event.type === 'MARKET_UPDATE' || event.type === 'INIT') {
                setSummary(event.data);
            }
        });
        return () => unsubscribe();
    }, []);

    const formatCurrency = (val) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency', currency: 'USD', minimumFractionDigits: 2
        }).format(val);
    };

    // DataTable columns for positions
    const positionColumns = [
        { key: 'symbol', label: 'Symbol', sortable: true },
        { key: 'qty', label: 'Qty', sortable: true, align: 'right' },
        { key: 'avgPrice', label: 'Avg Cost', sortable: true, align: 'right', render: (v) => `$${v.toFixed(2)}` },
        { key: 'marketValue', label: 'Market Value', sortable: true, align: 'right', render: (_, row) => `$${(row.qty * row.currentPrice).toLocaleString()}` },
        { key: 'pl', label: 'P/L Open', sortable: true, align: 'right', render: (v) => (
            <span className={v >= 0 ? 'text-green' : 'text-red'}>
                {v >= 0 ? '+' : ''}{formatCurrency(v)}
            </span>
        )}
    ];

    // Stats for hero section
    const heroStats = [
        { label: 'Total Liquidity', value: summary.liquidity, prefix: '$', status: 'positive', sparklineData: equityData.slice(-10).map(d => d.Value) },
        { label: 'Day P&L', value: Math.abs(summary.dailyPL), prefix: summary.dailyPL >= 0 ? '+$' : '-$', change: summary.dailyPL >= 0 ? 2.4 : -1.8, changeLabel: 'vs yesterday', status: summary.dailyPL >= 0 ? 'positive' : 'negative' },
        { label: 'Margin Used', value: 42, suffix: '%', status: 'neutral', sparklineData: [35, 38, 42, 40, 42] },
        { label: 'Open Orders', value: 3, status: 'neutral' }
    ];

    // Advanced RGL Layout
    const ResponsiveGridLayout = WidthProvider(Responsive);
    const DEFAULT_LAYOUT = {
        lg: [
            { i: 'stats', x: 0, y: 0, w: 12, h: 2, static: true },
            { i: 'margin', x: 0, y: 2, w: 12, h: 2 },
            { i: 'chart', x: 0, y: 4, w: 8, h: 4 },
            { i: 'connector', x: 8, y: 4, w: 4, h: 4 },
            { i: 'positions', x: 0, y: 8, w: 8, h: 4 },
            { i: 'execution', x: 8, y: 8, w: 4, h: 4 },
            { i: 'settlement', x: 8, y: 12, w: 4, h: 3 },
            { i: 'tax', x: 8, y: 15, w: 4, h: 3 },
            { i: 'waterfall', x: 8, y: 18, w: 4, h: 3 }
        ]
    };
    const STORAGE_KEY = 'layout_brokerage_dashboard';

    const [layouts, setLayouts] = useState(() => {
        try {
            const saved = localStorage.getItem(STORAGE_KEY);
            return saved ? JSON.parse(saved) : DEFAULT_LAYOUT;
        } catch (e) {
            return DEFAULT_LAYOUT;
        }
    });

    const onLayoutChange = (currentLayout, allLayouts) => {
        setLayouts(allLayouts);
        StorageService.set(STORAGE_KEY, allLayouts);
    };

    return (
        <div className="full-bleed-page brokerage-container glass-panel">
            {/* Header */}
            <header className="mb-2">
                <h1 className="text-3xl font-black text-white tracking-tight uppercase mb-1">
                    Virtual Brokerage Account
                </h1>
                <p className="text-zinc-500">Real-time portfolio tracking, execution, and risk management.</p>
            </header>

            <div className="scrollable-content-wrapper">
                <ResponsiveGridLayout
                className="layout"
                layouts={layouts}
                onLayoutChange={onLayoutChange}
                breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
                cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
                rowHeight={80}
                isDraggable={true}
                isResizable={true}
                draggableHandle=".glass-card-drag-handle" 
            >
                {/* Hero Stats Row - Static */}
                <div key="stats" className="flex gap-4">
                    {heroStats.map((stat, idx) => (
                        <div key={idx} style={{ flex: 1 }}>
                            <StatCard 
                                {...stat}
                                formatValue={v => stat.prefix?.includes('$') ? v.toLocaleString() : v}
                            />
                        </div>
                    ))}
                </div>

                {/* Margin Progress Bar */}
                <div key="margin">
                    <GlassCard variant="default" hoverable={false} className="h-full">
                        <div className="glass-card-drag-handle cursor-move flex items-center justify-between mb-2">
                            <span className="text-sm font-semibold text-white uppercase tracking-wide">Margin Utilization</span>
                            <Badge count="Safe" variant="success" />
                        </div>
                        <ProgressBar value={42} max={100} variant="default" size="lg" showValue={true} animated={true} />
                        <div className="flex justify-between mt-2 text-xs text-zinc-500">
                            <span>0% (No Margin)</span>
                            <span className="text-yellow-500">50% Warning</span>
                            <span className="text-red-500">80% Critical</span>
                        </div>
                    </GlassCard>
                </div>

                {/* Performance Chart */}
                <div key="chart">
                    <GlassCard variant="elevated" hoverable={false} className="h-full">
                        <div className="glass-card-drag-handle cursor-move flex justify-between items-center mb-4">
                            <h3 className="font-bold text-lg flex items-center gap-2 text-white">
                                <TrendingUp className="text-green-400" /> Account Performance
                            </h3>
                            <Badge count="+12.4% YTD" variant="success" />
                        </div>
                        <div className="h-[280px] w-full">
                            <SimpleLineChart data={equityData} dataKey="Value" color="#4ade80" />
                        </div>
                    </GlassCard>
                </div>

                {/* Positions Table */}
                <div key="positions">
                    <GlassCard variant="default" hoverable={false} className="h-full overflow-hidden">
                        <div className="glass-card-drag-handle cursor-move flex justify-between items-center mb-4">
                            <h3 className="font-bold text-lg flex items-center gap-2 text-white" data-tour-id="positions-table">
                                <Wallet className="text-blue-400" /> Holdings
                            </h3>
                            <Badge count={summary.positions.length} variant="info" />
                        </div>
                        <div className="overflow-y-auto h-[calc(100%-40px)]">
                            <DataTable 
                                columns={positionColumns}
                                data={summary.positions}
                                onRowClick={(row) => console.log('Selected:', row.symbol)}
                            />
                        </div>
                    </GlassCard>
                </div>

                {/* Institutional Vault Gateway */}
                <div key="connector">
                    <div className="h-full glass-card-drag-handle">
                        <InstitutionalConnectorWidget />
                    </div>
                </div>

                {/* Live Execution Router */}
                <div key="execution">
                    <GlassCard variant="elevated" status="success" hoverable={false} className="h-full">
                         <div className="glass-card-drag-handle h-4 w-full bg-transparent absolute top-0 left-0 cursor-move z-10" />
                        <OrderExecutionStatus />
                    </GlassCard>
                </div>

                {/* Multi-Currency Settlement */}
                <div key="settlement">
                    <GlassCard variant="default" hoverable={false} className="h-full">
                        <div className="glass-card-drag-handle h-4 w-full bg-transparent absolute top-0 left-0 cursor-move z-10" />
                        <SettlementDashboard />
                    </GlassCard>
                </div>

                {/* Tax Optimizer */}
                <div key="tax">
                    <GlassCard variant="default" status="warning" hoverable={false} className="h-full">
                        <div className="glass-card-drag-handle h-4 w-full bg-transparent absolute top-0 left-0 cursor-move z-10" />
                        <TaxLotOptimizer />
                    </GlassCard>
                </div>

                {/* Waterfall Attribution */}
                <div key="waterfall">
                    <GlassCard variant="default" hoverable={false} className="h-full">
                        <div className="glass-card-drag-handle h-4 w-full bg-transparent absolute top-0 left-0 cursor-move z-10" />
                        <PLWaterfall />
                    </GlassCard>
                </div>

                </ResponsiveGridLayout>
                {/* Bottom Buffer */}
                <div className="scroll-buffer-100" />
            </div>
        </div>
    );
};

// Mock Helper
const generateMockEquity = () => {
    let eq = 100000;
    return Array.from({ length: 50 }, (_, i) => {
        eq = eq * (1 + (Math.random() - 0.45) * 0.01);
        return { name: i, Value: eq };
    });
}

export default BrokerageAccount;
