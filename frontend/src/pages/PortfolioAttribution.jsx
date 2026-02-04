import React, { useEffect } from 'react';
import { StorageService } from '../utils/storageService';
import { Responsive, WidthProvider } from 'react-grid-layout';
import SectorAttribution from '../widgets/Attribution/SectorAttribution';
import InteractionHeatmap from '../widgets/Attribution/InteractionHeatmap';
import RelativeStrength from '../widgets/Attribution/RelativeStrength';
import '../widgets/Attribution/SectorAttribution.css';

// New UI/UX Components
import { StatCard, ProgressBar } from '../components/DataViz';
import { GlassCard } from '../components/Common';
import { usePortfolioStore } from '../stores/portfolioStore';

const ResponsiveGridLayout = WidthProvider(Responsive);

const PortfolioAttribution = () => {
    const { 
        attribution, 
        fetchAttribution,
        isLoading
    } = usePortfolioStore();

    useEffect(() => {
        // Fetch initially if missing
        if (!attribution) {
            fetchAttribution('main-portfolio');
        }
    }, [attribution, fetchAttribution]);

    const DEFAULT_LAYOUT = {
        lg: [
            { i: 'stats', x: 0, y: 0, w: 12, h: 3 },
            { i: 'sector', x: 0, y: 3, w: 6, h: 9 },
            { i: 'heatmap', x: 6, y: 3, w: 6, h: 9 },
            { i: 'strength', x: 0, y: 12, w: 12, h: 10 }
        ]
    };
    const STORAGE_KEY = 'layout_attribution_dashboard_v2';

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

    // Helper to format dynamic stats
    const getStats = () => {
        if (!attribution) return [
            { label: 'Selection Effect', value: 0, suffix: 'bp', status: 'neutral' },
            { label: 'Allocation Effect', value: 0, suffix: 'bp', status: 'neutral' },
            { label: 'Interaction Effect', value: 0, suffix: 'bp', status: 'neutral' },
            { label: 'Total Active Return', value: 0, suffix: 'bp', status: 'neutral' }
        ];

        return [
            { 
                label: 'Selection Effect', 
                value: attribution.total_selection_effect, 
                suffix: 'bp', 
                status: attribution.total_selection_effect >= 0 ? 'positive' : 'negative' 
            },
            { 
                label: 'Allocation Effect', 
                value: attribution.total_allocation_effect, 
                suffix: 'bp', 
                status: attribution.total_allocation_effect >= 0 ? 'positive' : 'negative' 
            },
            { 
                label: 'Interaction Effect', 
                value: attribution.total_interaction_effect, 
                suffix: 'bp', 
                status: attribution.total_interaction_effect >= 0 ? 'positive' : 'negative' 
            },
            { 
                label: 'Total Active Return', 
                value: attribution.total_active_return, 
                suffix: 'bp', 
                status: attribution.total_active_return >= 0 ? 'positive' : 'negative' 
            }
        ];
    };

    const stats = getStats();

    return (
        <div className="full-bleed-page portfolio-attribution-page">
            <header className="mb-6">
                <h1 className="text-3xl font-black text-white tracking-tight uppercase mb-1">
                    Portfolio Attribution Analysis
                </h1>
                <p className="text-zinc-500">Brinson-Fachler decomposition of active returns.</p>
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
                    {/* Stats Row */}
                    <div key="stats" style={{ display: 'flex', gap: '16px' }}>
                        {stats.map((stat, idx) => (
                            <div key={idx} style={{ flex: 1 }}>
                                <StatCard 
                                    label={stat.label}
                                    value={stat.value}
                                    suffix={stat.suffix}
                                    status={stat.status}
                                    isLoading={isLoading}
                                />
                            </div>
                        ))}
                    </div>

                    <div key="sector" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                        <GlassCard variant="elevated" hoverable={false} className="h-full">
                            {/* Title handled inside widget for now, or we can move it out */}
                            <SectorAttribution />
                        </GlassCard>
                    </div>
                    <div key="heatmap" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                        <GlassCard variant="elevated" hoverable={false} className="h-full">
                            <h3 className="font-bold text-white mb-4">Interaction Heatmap</h3>
                            <InteractionHeatmap />
                        </GlassCard>
                    </div>
                    <div key="strength" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                        <GlassCard variant="default" hoverable={false} className="h-full">
                            <h3 className="font-bold text-white mb-4">Relative Strength Analysis</h3>
                            <RelativeStrength />
                        </GlassCard>
                    </div>
                </ResponsiveGridLayout>
                
                {/* Bottom Buffer */}
                <div className="scroll-buffer-100" />
            </div>
        </div>
    );
};

export default PortfolioAttribution;
