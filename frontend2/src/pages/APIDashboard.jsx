import React, { useEffect } from 'react';
import { Responsive, WidthProvider } from 'react-grid-layout';
import useAPIStore from '../stores/apiStore';
import DataConnectors from '../widgets/API/DataConnectors';
import KeyVault from '../widgets/API/KeyVault';
import WebhookConfig from '../widgets/API/WebhookConfig';
import '../widgets/API/DataConnectors.css';

// New UI/UX Components
import { StatCard, Badge } from '../components/DataViz';
import { GlassCard } from '../components/Common';

const ResponsiveGridLayout = WidthProvider(Responsive);

const APIDashboard = () => {
    const { 
        connectors, 
        apiKeys, 
        webhooks, 
        fetchConnectors, 
        error 
    } = useAPIStore();

    const DEFAULT_LAYOUT = {
        lg: [
            { i: 'stats', x: 0, y: 0, w: 12, h: 2 },
            { i: 'connectors', x: 0, y: 2, w: 6, h: 5 },
            { i: 'vault', x: 6, y: 2, w: 6, h: 5 },
            { i: 'webhooks', x: 0, y: 7, w: 12, h: 4 }
        ]
    };
    const STORAGE_KEY = 'layout_api_dashboard';

    const [layouts, setLayouts] = React.useState(() => {
        try {
            const saved = localStorage.getItem(STORAGE_KEY);
            return saved ? JSON.parse(saved) : DEFAULT_LAYOUT;
        } catch (e) {
            return DEFAULT_LAYOUT;
        }
    });

    useEffect(() => {
        fetchConnectors();
    }, [fetchConnectors]);

    const onLayoutChange = (currentLayout, allLayouts) => {
        setLayouts(allLayouts);
        localStorage.setItem(STORAGE_KEY, JSON.stringify(allLayouts));
    };

    const apiStats = [
        { label: 'Active Connectors', value: connectors.filter(c => c.status === 'active' || c.status === 'healthy').length, status: 'positive' },
        { label: 'API Keys', value: apiKeys.length, status: 'neutral' },
        { label: 'Webhooks', value: webhooks.length, status: 'positive' },
        { label: 'Total Usage', value: connectors.reduce((acc, c) => acc + (c.usage || 0), 0), change: 0, status: 'positive' }
    ];

    return (
        <div className="api-dashboard-page p-6 h-full overflow-y-auto bg-slate-950">
            <header className="mb-6">
                <div className="flex items-center gap-4">
                    <h1 className="text-3xl font-black text-white tracking-tight uppercase">
                        API Marketplace
                    </h1>
                    <Badge count={`${connectors.length} Active`} variant="success" />
                </div>
                <p className="text-zinc-500 mt-1">Data connectors, API keys, and webhook configuration.</p>
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
                    {apiStats.map((stat, idx) => (
                        <div key={idx} style={{ flex: 1 }}>
                            <StatCard {...stat} formatValue={v => v.toLocaleString()} />
                        </div>
                    ))}
                </div>

                <div key="connectors" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                    <GlassCard variant="elevated" hoverable={false} className="h-full">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="font-bold text-white">Data Connectors</h3>
                            <Badge count="8 Active" variant="success" />
                        </div>
                        <DataConnectors />
                    </GlassCard>
                </div>
                <div key="vault" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                    <GlassCard variant="elevated" status="success" hoverable={false} className="h-full">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="font-bold text-white">Key Vault</h3>
                            <Badge count="Encrypted" variant="success" />
                        </div>
                        <KeyVault />
                    </GlassCard>
                </div>
                <div key="webhooks" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                    <GlassCard variant="default" hoverable={false} className="h-full">
                        <h3 className="font-bold text-white mb-4">Webhook Configuration</h3>
                        <WebhookConfig />
                    </GlassCard>
                </div>
            </ResponsiveGridLayout>
        </div>
    );
};

export default APIDashboard;
