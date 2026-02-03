import React, { useEffect } from 'react';
import { StorageService } from '../utils/storageService';
import { Responsive, WidthProvider } from 'react-grid-layout';
import BondLadder from '../widgets/FixedIncome/BondLadder';
import YieldCurvePlotter from '../widgets/FixedIncome/YieldCurvePlotter';
import DurationGauges from '../widgets/FixedIncome/DurationGauges';
import '../widgets/FixedIncome/BondLadder.css';

// New UI/UX Components
import { StatCard, Badge } from '../components/DataViz';
import { GlassCard } from '../components/Common';
import { useFixedIncomeStore } from '../stores/fixedIncomeStore';

const ResponsiveGridLayout = WidthProvider(Responsive);

const FixedIncomeDashboard = () => {
    const { fetchYieldCurve, fetchHistoricalCurves } = useFixedIncomeStore();

    useEffect(() => {
        fetchYieldCurve();
        fetchHistoricalCurves();
    }, [fetchYieldCurve, fetchHistoricalCurves]);

    const DEFAULT_LAYOUT = {
        lg: [
            { i: 'stats', x: 0, y: 0, w: 12, h: 3 },
            { i: 'ladder', x: 0, y: 3, w: 5, h: 12 },
            { i: 'gauges', x: 5, y: 3, w: 7, h: 4 },
            { i: 'curve', x: 5, y: 7, w: 7, h: 8 }
        ]
    };
    const STORAGE_KEY = 'layout_fixed_income_dashboard_v2';

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

    const bondStats = [
        { label: 'Portfolio Duration', value: 4.2, suffix: ' yrs', status: 'neutral' },
        { label: 'Yield to Maturity', value: 5.4, suffix: '%', change: 0.08, status: 'positive' },
        { label: 'Credit Quality', value: 'AA-', status: 'positive' },
        { label: 'Maturities', value: 24, suffix: ' bonds', status: 'neutral' }
    ];

    return (
        <div className="full-bleed-page fixed-income-page">
            <header className="mb-6">
                <div className="flex items-center gap-4">
                    <h1 className="text-3xl font-black text-white tracking-tight uppercase">
                        Fixed Income Intelligence
                    </h1>
                    <Badge count="Live Yields" variant="success" pulse />
                </div>
                <p className="text-zinc-500 mt-1">Yield curve analysis, bond ladder, and duration management.</p>
            </header>
            
            <div className="scrollable-content-wrapper">
                <ResponsiveGridLayout
                    className="layout"
                    layouts={layouts}
                    onLayoutChange={onLayoutChange}
                    breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
                    cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
                    rowHeight={40}
                    isDraggable={true}
                    isResizable={true}
                    margin={[10, 10]}
                >
                    <div key="stats" style={{ display: 'flex', gap: '16px' }}>
                        {bondStats.map((stat, idx) => (
                            <div key={idx} style={{ flex: 1 }}>
                                <StatCard {...stat} formatValue={v => typeof v === 'number' ? v : v} />
                            </div>
                        ))}
                    </div>

                    <div key="ladder" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                        <GlassCard variant="elevated" hoverable={false} className="h-full">
                            <h3 className="font-bold text-white mb-4">Bond Ladder</h3>
                            <BondLadder />
                        </GlassCard>
                    </div>
                    <div key="gauges" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                        <GlassCard variant="elevated" hoverable={false} className="h-full">
                            <h3 className="font-bold text-white mb-3">Duration Metrics</h3>
                            <DurationGauges />
                        </GlassCard>
                    </div>
                    <div key="curve" style={{ borderRadius: '12px', overflow: 'hidden' }} data-tour-id="yield-curve-chart">
                        <GlassCard variant="default" hoverable={false} className="h-full">
                            <div className="flex justify-between items-center mb-3">
                                <h3 className="font-bold text-white">Yield Curve</h3>
                                <Badge count="Inverted" variant="warning" />
                            </div>
                            <YieldCurvePlotter />
                        </GlassCard>
                    </div>
                </ResponsiveGridLayout>
                
                {/* Bottom Buffer */}
                <div className="scroll-buffer-100" />
            </div>
        </div>
    );
};

export default FixedIncomeDashboard;
