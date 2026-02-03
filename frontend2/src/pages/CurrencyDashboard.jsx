import React from 'react';
import { StorageService } from '../utils/storageService';
import { Responsive, WidthProvider } from 'react-grid-layout';
import CashPulse from '../widgets/Currency/CashPulse';
import FXConversion from '../widgets/Currency/FXConversion';
import CashOptimizer from '../widgets/Currency/CashOptimizer';
import '../widgets/Currency/CashPulse.css';

// New UI/UX Components
import { StatCard, Badge } from '../components/DataViz';
import { GlassCard } from '../components/Common';

const ResponsiveGridLayout = WidthProvider(Responsive);

const CurrencyDashboard = () => {
    const DEFAULT_LAYOUT = {
        lg: [
            { i: 'stats', x: 0, y: 0, w: 12, h: 2 },
            { i: 'pulse', x: 0, y: 2, w: 8, h: 4 },
            { i: 'optimizer', x: 8, y: 2, w: 4, h: 4 },
            { i: 'fx', x: 0, y: 6, w: 12, h: 3 }
        ]
    };
    const STORAGE_KEY = 'layout_currency_dashboard';

    const [layouts, setLayouts] = React.useState(() => {
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

    const currencyStats = [
        { label: 'USD Balance', value: 1245000, prefix: '$', change: 12400, status: 'positive' },
        { label: 'EUR Balance', value: 485000, prefix: '€', change: -2100, status: 'neutral' },
        { label: 'Active Hedges', value: 4, status: 'positive' },
        { label: 'FX Exposure', value: 18, suffix: '%', status: 'neutral' }
    ];

    return (
        <div className="currency-dashboard-page p-6 h-full overflow-y-auto bg-slate-950">
            <header className="mb-6">
                <div className="flex items-center gap-4">
                    <h1 className="text-3xl font-black text-white tracking-tight uppercase">
                        Multi-Currency Management
                    </h1>
                    <Badge count="5 Currencies" variant="info" />
                </div>
                <p className="text-zinc-500 mt-1">FX exposure, cash optimization, and currency conversion.</p>
            </header>
            
            <ResponsiveGridLayout
                className="layout"
                layouts={layouts}
                onLayoutChange={onLayoutChange}
                breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
                cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
                rowHeight={80}
                isDraggable={true}
                isResizable={true}
            >
                <div key="stats" style={{ display: 'flex', gap: '16px' }}>
                    {currencyStats.map((stat, idx) => (
                        <div key={idx} style={{ flex: 1 }}>
                            <StatCard {...stat} formatValue={v => typeof v === 'number' ? v.toLocaleString() : v} />
                        </div>
                    ))}
                </div>

                <div key="pulse" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                    <GlassCard variant="elevated" hoverable={false} className="h-full">
                        <h3 className="font-bold text-white mb-4">Cash Pulse</h3>
                        <CashPulse />
                    </GlassCard>
                </div>
                <div key="optimizer" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                    <GlassCard variant="elevated" status="success" hoverable={false} className="h-full">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="font-bold text-white">Cash Optimizer</h3>
                            <Badge count="Active" variant="success" />
                        </div>
                        <CashOptimizer />
                    </GlassCard>
                </div>
                <div key="fx" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                    <GlassCard variant="default" hoverable={false} className="h-full">
                        <h3 className="font-bold text-white mb-4">FX Conversion</h3>
                        <FXConversion />
                    </GlassCard>
                </div>
            </ResponsiveGridLayout>
        </div>
    );
};

export default CurrencyDashboard;
