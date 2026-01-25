import React from 'react';
import { Responsive, WidthProvider } from 'react-grid-layout';
import WorldMap from '../widgets/Macro/GlobalMacroMap';
import FuturesCurve from '../widgets/Macro/FuturesCurve';
import InflationMatrix from '../widgets/Macro/InflationMatrix';
import PageHeader from '../components/Navigation/PageHeader';
import { Globe } from 'lucide-react';
import '../widgets/Macro/GlobalMacro.css';

// New UI/UX Components
import { StatCard, Badge } from '../components/DataViz';
import { GlassCard } from '../components/Common';

const ResponsiveGridLayout = WidthProvider(Responsive);

const MacroDashboard = () => {
    const layout = [
        { i: 'stats', x: 0, y: 0, w: 12, h: 2 },
        { i: 'map', x: 0, y: 2, w: 8, h: 4 },
        { i: 'matrix', x: 8, y: 2, w: 4, h: 4 },
        { i: 'futures', x: 0, y: 6, w: 12, h: 3 }
    ];

    // Macro stats
    const macroStats = [
        { label: 'US 10Y Yield', value: 4.28, suffix: '%', change: 0.05, status: 'negative' },
        { label: 'DXY Index', value: 103.42, change: -0.32, status: 'positive' },
        { label: 'WTI Crude', value: 72.84, prefix: '$', change: 1.2, status: 'neutral' },
        { label: 'Gold', value: 2024.50, prefix: '$', change: 8.40, status: 'positive' }
    ];

    return (
        <div className="macro-dashboard-page p-6">
            <header className="mb-6">
                <div className="flex items-center gap-4">
                    <h1 className="text-3xl font-black text-white tracking-tight uppercase">
                        Global Macro & Commodities
                    </h1>
                    <Badge count="Live" variant="success" pulse />
                </div>
                <p className="text-zinc-500 mt-1">Central bank policy, rates, and commodity curves.</p>
            </header>
            
            <ResponsiveGridLayout
                className="layout"
                layouts={{ lg: layout }}
                breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
                cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
                rowHeight={80}
                isDraggable={true}
                isResizable={true}
            >
                {/* Stats Row */}
                <div key="stats" style={{ display: 'flex', gap: '16px' }}>
                    {macroStats.map((stat, idx) => (
                        <div key={idx} style={{ flex: 1 }}>
                            <StatCard {...stat} formatValue={v => v.toLocaleString()} />
                        </div>
                    ))}
                </div>

                <div key="map" style={{ borderRadius: '12px', overflow: 'hidden' }} data-tour-id="world-map">
                    <GlassCard variant="elevated" hoverable={false} className="h-full">
                        <h3 className="font-bold text-white mb-4">Global Economic Map</h3>
                        <WorldMap />
                    </GlassCard>
                </div>
                <div key="matrix" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                    <GlassCard variant="elevated" status="warning" hoverable={false} className="h-full">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="font-bold text-white">Inflation Matrix</h3>
                            <Badge count="4 Central Banks" variant="warning" />
                        </div>
                        <InflationMatrix />
                    </GlassCard>
                </div>
                <div key="futures" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                    <GlassCard variant="default" hoverable={false} className="h-full">
                        <h3 className="font-bold text-white mb-4">Futures Curve Analysis</h3>
                        <FuturesCurve />
                    </GlassCard>
                </div>
            </ResponsiveGridLayout>
        </div>
    );
};

export default MacroDashboard;
