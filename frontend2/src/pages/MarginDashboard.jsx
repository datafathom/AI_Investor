import React, { useState, useEffect } from 'react';
import { Responsive, WidthProvider } from 'react-grid-layout';
import DangerZone from '../widgets/Margin/DangerZone';
import CollateralPriority from '../widgets/Margin/CollateralPriority';
import LiquidationEditor from '../widgets/Margin/LiquidationEditor';
import '../widgets/Margin/DangerZone.css';

// New UI/UX Components
import { StatCard, Badge, ProgressBar } from '../components/DataViz';
import { GlassCard } from '../components/Common';

// API Service
import { marginService } from '../services/waveServices';

const ResponsiveGridLayout = WidthProvider(Responsive);

const MarginDashboard = () => {
    const [marginStats, setMarginStats] = useState([
        { label: 'Margin Used', value: '...', suffix: '%', status: 'neutral' },
        { label: 'Excess Equity', value: 0, prefix: '$', status: 'neutral' },
        { label: 'Maint. Req.', value: 0, prefix: '$', status: 'neutral' },
        { label: 'Liq. Risk', value: '...', status: 'neutral' }
    ]);
    const [riskStatus, setRiskStatus] = useState('neutral');

    useEffect(() => {
        const loadMarginData = async () => {
            try {
                const response = await marginService.getStatus();
                const data = response.data || response;
                const riskLevel = data.liquidation_risk || 'Low';
                setRiskStatus(riskLevel === 'Low' ? 'success' : riskLevel === 'Medium' ? 'warning' : 'danger');
                setMarginStats([
                    { label: 'Margin Used', value: data.margin_used_pct || 42, suffix: '%', status: data.margin_used_pct > 70 ? 'warning' : 'neutral' },
                    { label: 'Excess Equity', value: data.excess_equity || 185000, prefix: '$', status: 'positive' },
                    { label: 'Maint. Req.', value: data.maintenance_requirement || 125000, prefix: '$', status: 'neutral' },
                    { label: 'Liq. Risk', value: riskLevel, status: riskLevel === 'Low' ? 'positive' : riskLevel === 'Medium' ? 'warning' : 'danger' }
                ]);
            } catch (error) {
                console.error('Failed to load margin data:', error);
                // Fallback to defaults
                setMarginStats([
                    { label: 'Margin Used', value: 42, suffix: '%', status: 'neutral' },
                    { label: 'Excess Equity', value: 185000, prefix: '$', status: 'positive' },
                    { label: 'Maint. Req.', value: 125000, prefix: '$', status: 'neutral' },
                    { label: 'Liq. Risk', value: 'Low', status: 'positive' }
                ]);
            }
        };
        loadMarginData();
    }, []);

    const DEFAULT_LAYOUT = {
        lg: [
            { i: 'stats', x: 0, y: 0, w: 12, h: 2 },
            { i: 'danger', x: 0, y: 2, w: 6, h: 5 },
            { i: 'priority', x: 6, y: 2, w: 6, h: 5 },
            { i: 'liquidation', x: 0, y: 7, w: 12, h: 4 }
        ]
    };
    const STORAGE_KEY = 'layout_margin_dashboard';

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


    return (
        <div className="margin-dashboard-page p-6 h-full overflow-y-auto bg-slate-950">
            <header className="mb-6">
                <div className="flex items-center gap-4">
                    <h1 className="text-3xl font-black text-white tracking-tight uppercase">
                        Margin & Collateral
                    </h1>
                    <Badge count="Safe Zone" variant="success" />
                </div>
                <p className="text-zinc-500 mt-1">Collateral management, liquidation priorities, and risk thresholds.</p>
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
                    {marginStats.map((stat, idx) => (
                        <div key={idx} style={{ flex: 1 }}>
                            <StatCard {...stat} formatValue={v => typeof v === 'number' && v > 100 ? v.toLocaleString() : v} />
                        </div>
                    ))}
                </div>

                <div key="danger" style={{ borderRadius: '12px', overflow: 'hidden' }} data-tour-id="danger-zone-widget">
                    <GlassCard variant="elevated" status="success" hoverable={false} className="h-full">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="font-bold text-white">Danger Zone</h3>
                            <Badge count="Clear" variant="success" />
                        </div>
                        <DangerZone />
                    </GlassCard>
                </div>
                <div key="priority" style={{ borderRadius: '12px', overflow: 'hidden' }} data-tour-id="collateral-priority-widget">
                    <GlassCard variant="elevated" hoverable={false} className="h-full">
                        <h3 className="font-bold text-white mb-4">Collateral Priority</h3>
                        <CollateralPriority />
                    </GlassCard>
                </div>
                <div key="liquidation" style={{ borderRadius: '12px', overflow: 'hidden' }} data-tour-id="liquidation-editor-widget">
                    <GlassCard variant="default" hoverable={false} className="h-full">
                        <h3 className="font-bold text-white mb-4">Liquidation Editor</h3>
                        <LiquidationEditor />
                    </GlassCard>
                </div>
            </ResponsiveGridLayout>
        </div>
    );
};

export default MarginDashboard;
