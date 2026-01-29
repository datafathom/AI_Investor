import React, { useEffect } from 'react';
import { Responsive, WidthProvider } from 'react-grid-layout';
import useSystemHealthStore from '../stores/systemHealthStore';
import KafkaHealth from '../widgets/System/KafkaHealth';
import DatabaseGauges from '../widgets/System/DatabaseGauges';
import AgentLoadBalancer from '../widgets/System/AgentLoadBalancer';
import SecretsStatus from '../widgets/System/SecretsStatus';
import SupplyChainWidget from '../widgets/System/SupplyChainWidget';
import '../widgets/System/KafkaHealth.css';

// New UI/UX Components
import { StatCard, Badge } from '../components/DataViz';
import { GlassCard } from '../components/Common';

const ResponsiveGridLayout = WidthProvider(Responsive);

const SystemHealthDashboard = () => {
    const { 
        kafkaHealth, 
        postgresHealth, 
        neo4jHealth, 
        agentLoad, 
        overallStatus, 
        refreshHealth 
    } = useSystemHealthStore();

    const DEFAULT_LAYOUT = {
        lg: [
            { i: 'stats', x: 0, y: 0, w: 12, h: 2 },
            { i: 'kafka', x: 0, y: 2, w: 4, h: 5 },
            { i: 'db', x: 4, y: 2, w: 4, h: 5 },
            { i: 'secrets', x: 8, y: 2, w: 4, h: 5 },
            { i: 'agent', x: 0, y: 7, w: 12, h: 4 },
            { i: 'supply', x: 0, y: 11, w: 12, h: 4 }
        ]
    };
    const STORAGE_KEY = 'layout_system_health_dashboard';

    const [layouts, setLayouts] = React.useState(() => {
        try {
            const saved = localStorage.getItem(STORAGE_KEY);
            return saved ? JSON.parse(saved) : DEFAULT_LAYOUT;
        } catch (e) {
            return DEFAULT_LAYOUT;
        }
    });

    useEffect(() => {
        refreshHealth();
        const interval = setInterval(refreshHealth, 10000);
        return () => clearInterval(interval);
    }, [refreshHealth]);

    const onLayoutChange = (currentLayout, allLayouts) => {
        setLayouts(allLayouts);
        localStorage.setItem(STORAGE_KEY, JSON.stringify(allLayouts));
    };

    // System health stats derived from store
    const systemStats = [
        { label: 'Kafka Lag', value: kafkaHealth.lag, suffix: ' msgs', status: kafkaHealth.lag > 5000 ? 'negative' : 'positive' },
        { label: 'PG Latency', value: postgresHealth.queryTime, suffix: ' ms', status: postgresHealth.queryTime > 100 ? 'negative' : 'positive' },
        { label: 'Neo4j Nodes', value: neo4jHealth.nodes, change: 0, status: 'neutral' },
        { label: 'Active Agents', value: agentLoad.length, change: 0, status: 'positive' }
    ];

    return (
        <div className="full-bleed-page system-dashboard-page">
            <header className="mb-6">
                <div className="flex items-center gap-4">
                    <h1 className="text-3xl font-black text-white tracking-tight uppercase">
                        System Health & Telemetry
                    </h1>
                    <Badge 
                        count={overallStatus.toUpperCase()} 
                        variant={overallStatus === 'healthy' ? 'success' : 'danger'} 
                        pulse={overallStatus === 'healthy'} 
                    />
                </div>
                <p className="text-zinc-500 mt-1">Infrastructure monitoring, agent status, and security posture.</p>
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
                >
                {/* Stats Row */}
                <div key="stats" style={{ display: 'flex', gap: '16px' }}>
                    {systemStats.map((stat, idx) => (
                        <div key={idx} style={{ flex: 1 }}>
                            <StatCard {...stat} formatValue={v => typeof v === 'number' && v > 100 ? v.toLocaleString() : v} />
                        </div>
                    ))}
                </div>

                <div key="kafka" style={{ borderRadius: '12px', overflow: 'hidden' }} data-tour-id="kafka-health-widget">
                    <GlassCard variant="elevated" status="success" hoverable={false} className="h-full">
                        <div className="flex justify-between items-center mb-3">
                            <h4 className="font-bold text-white text-sm uppercase">Kafka Health</h4>
                            <Badge count="Healthy" variant="success" />
                        </div>
                        <KafkaHealth />
                    </GlassCard>
                </div>
                <div key="db" style={{ borderRadius: '12px', overflow: 'hidden' }} data-tour-id="database-gauges-widget">
                    <GlassCard variant="elevated" hoverable={false} className="h-full">
                        <div className="flex justify-between items-center mb-3">
                            <h4 className="font-bold text-white text-sm uppercase">Database Metrics</h4>
                            <Badge count="2.4K qps" variant="info" />
                        </div>
                        <DatabaseGauges />
                    </GlassCard>
                </div>
                <div key="secrets" style={{ borderRadius: '12px', overflow: 'hidden' }} data-tour-id="secrets-status-widget">
                    <GlassCard variant="elevated" status="success" hoverable={false} className="h-full">
                        <div className="flex justify-between items-center mb-3">
                            <h4 className="font-bold text-white text-sm uppercase">Secrets Vault</h4>
                            <Badge count="Sealed" variant="success" />
                        </div>
                        <SecretsStatus />
                    </GlassCard>
                </div>
                <div key="agent" style={{ borderRadius: '12px', overflow: 'hidden' }} data-tour-id="agent-load-balancer-widget">
                    <GlassCard variant="default" hoverable={false} className="h-full">
                        <div className="flex justify-between items-center mb-3">
                            <h4 className="font-bold text-white text-sm uppercase">Agent Load Balancer</h4>
                            <div className="flex gap-2">
                                <Badge count="12 Active" variant="success" />
                                <Badge count="0 Idle" variant="default" />
                            </div>
                        </div>
                        <AgentLoadBalancer />
                    </GlassCard>
                </div>
                <div key="supply" style={{ borderRadius: '12px', overflow: 'hidden' }} data-tour-id="supply-chain-widget">
                    <GlassCard variant="default" hoverable={false} className="h-full">
                        <div className="flex justify-between items-center mb-3">
                            <h4 className="font-bold text-white text-sm uppercase">Supply Chain Security</h4>
                            <Badge count="0 Vulnerabilities" variant="success" />
                        </div>
                        <SupplyChainWidget />
                    </GlassCard>
                </div>
            </ResponsiveGridLayout>
            
            {/* Bottom Buffer */}
            <div className="scroll-buffer-100" />
          </div>
        </div>
    );
};

export default SystemHealthDashboard;
