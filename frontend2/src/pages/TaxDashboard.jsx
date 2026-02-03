import React from 'react';
import { StorageService } from '../utils/storageService';
import { Responsive, WidthProvider } from 'react-grid-layout';
import TaxLossHarvesting from '../widgets/Tax/TaxLossHarvesting';
import HarvestingToggle from '../widgets/Tax/HarvestingToggle';
import GainsForecaster from '../widgets/Tax/GainsForecaster';
import '../widgets/Tax/TaxHarvesting.css';

// New UI/UX Components
import { StatCard, ProgressBar, Badge } from '../components/DataViz';
import { GlassCard } from '../components/Common';

const ResponsiveGridLayout = WidthProvider(Responsive);

const TaxDashboard = () => {
    const DEFAULT_LAYOUT = {
        lg: [
            { i: 'stats', x: 0, y: 0, w: 12, h: 2 },
            { i: 'harvest', x: 0, y: 2, w: 7, h: 4 },
            { i: 'toggle', x: 7, y: 2, w: 5, h: 1 },
            { i: 'forecast', x: 7, y: 3, w: 5, h: 3 }
        ]
    };
    const STORAGE_KEY = 'layout_tax_dashboard';

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

    // Tax stats
    const taxStats = [
        { label: 'YTD Realized Gains', value: 28450, prefix: '$', status: 'negative', sparklineData: [20, 22, 25, 28, 28.5] },
        { label: 'Harvested Losses', value: 12800, prefix: '$', change: 3200, status: 'positive' },
        { label: 'Tax Savings Est.', value: 4860, prefix: '$', status: 'positive' },
        { label: 'Wash Sale Risk', value: 2, suffix: ' positions', status: 'warning' }
    ];

    return (
        <div className="full-bleed-page tax-dashboard-page">
            <header className="mb-6">
                <div className="flex items-center gap-4">
                    <h1 className="text-3xl font-black text-white tracking-tight uppercase">
                        Tax-Advantaged Strategy
                    </h1>
                    <Badge count="Auto-Harvest ON" variant="success" />
                </div>
                <p className="text-zinc-500 mt-1">Loss harvesting, wash sale monitoring, and capital gains forecasting.</p>
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
                    draggableHandle=".glass-card-drag-handle, h3"
                >
                    {/* Stats Row */}
                    <div key="stats" style={{ display: 'flex', gap: '16px' }}>
                        {taxStats.map((stat, idx) => (
                            <div key={idx} style={{ flex: 1 }}>
                                <StatCard {...stat} formatValue={v => v.toLocaleString()} />
                            </div>
                        ))}
                    </div>

                    <div key="harvest" style={{ borderRadius: '12px', overflow: 'hidden' }} data-tour-id="harvest-candidates">
                        <GlassCard variant="elevated" hoverable={false} className="h-full">
                            <div className="flex justify-between items-center mb-3">
                                <h3 className="font-bold text-white">Harvest Candidates</h3>
                                <Badge count="8 Opportunities" variant="success" />
                            </div>
                            <TaxLossHarvesting />
                        </GlassCard>
                    </div>
                    <div key="toggle" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                        <GlassCard variant="default" status="success" hoverable={false} className="h-full">
                            <HarvestingToggle />
                        </GlassCard>
                    </div>
                    <div key="forecast" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                        <GlassCard variant="default" hoverable={false} className="h-full">
                            <h3 className="font-bold text-white mb-4">Capital Gains Forecast</h3>
                            <GainsForecaster />
                        </GlassCard>
                    </div>
                </ResponsiveGridLayout>
                
                {/* Bottom Buffer */}
                <div className="scroll-buffer-100" />
            </div>
        </div>
    );
};

export default TaxDashboard;
