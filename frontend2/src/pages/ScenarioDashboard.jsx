import React from 'react';
import { Responsive, WidthProvider } from 'react-grid-layout';
import StressTest from '../widgets/Scenario/StressTest';
import MonteCarloRefined from '../widgets/Scenario/MonteCarloRefined';
import ForecastChart from '../widgets/Scenario/ForecastChart';
import BankRunSim from '../widgets/Scenario/BankRunSim';
import useScenarioStore from '../stores/scenarioStore';

// New UI/UX Components
import { StatCard, Badge } from '../components/DataViz';
import { GlassCard } from '../components/Common';

const ResponsiveGridLayout = WidthProvider(Responsive);

const ScenarioDashboard = () => {
    const { impactResults, recoveryProjection } = useScenarioStore();
    
    const DEFAULT_LAYOUT = {
        lg: [
            { i: 'stats', x: 0, y: 0, w: 12, h: 2 },
            { i: 'stress', x: 0, y: 2, w: 4, h: 6 },
            { i: 'mc', x: 4, y: 2, w: 8, h: 6 },
            { i: 'bankrun', x: 0, y: 8, w: 4, h: 5 },
            { i: 'forecast', x: 4, y: 8, w: 8, h: 5 }
        ]
    };
    const STORAGE_KEY = 'layout_scenario_dashboard';

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
        localStorage.setItem(STORAGE_KEY, JSON.stringify(allLayouts));
    };

    const scenarioStats = [
        { label: 'Shock Impact', value: impactResults?.portfolio_impact_pct || 0, suffix: '%', status: impactResults?.portfolio_impact_pct < 0 ? 'warning' : 'neutral' },
        { label: 'New Value', value: impactResults?.new_value || 1000000, prefix: '$', status: 'neutral' },
        { label: 'Recovery Time', value: recoveryProjection?.days || '--', suffix: ' Days', status: 'neutral' },
        { label: 'Hedge Status', value: impactResults ? 'Partial' : 'No Shock', status: 'neutral' }
    ];

    return (
        <div className="scenario-dashboard-page p-6 h-full overflow-y-auto bg-slate-950">
            <header className="mb-6">
                <div className="flex items-center gap-4">
                    <h1 className="text-3xl font-black text-white tracking-tight uppercase">
                        Scenario Modeling
                    </h1>
                    <Badge count="3 Active" variant="warning" />
                </div>
                <p className="text-zinc-500 mt-1">What-if analysis, stress testing, and impact simulation.</p>
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
                    {scenarioStats.map((stat, idx) => (
                        <div key={idx} style={{ flex: 1 }}>
                            <StatCard {...stat} formatValue={v => typeof v === 'number' && Math.abs(v) > 100 ? v.toLocaleString() : v} />
                        </div>
                    ))}
                </div>

                <div key="stress" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                    <GlassCard variant="elevated" status="warning" hoverable={false} className="h-full">
                        <StressTest />
                    </GlassCard>
                </div>
                <div key="mc" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                    <GlassCard variant="elevated" hoverable={false} className="h-full">
                        <MonteCarloRefined />
                    </GlassCard>
                </div>
                <div key="bankrun" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                    <GlassCard variant="default" hoverable={false} className="h-full">
                        <BankRunSim />
                    </GlassCard>
                </div>
                <div key="forecast" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                    <GlassCard variant="elevated" hoverable={false} className="h-full">
                        <ForecastChart />
                    </GlassCard>
                </div>
            </ResponsiveGridLayout>
        </div>
    );
};

export default ScenarioDashboard;
