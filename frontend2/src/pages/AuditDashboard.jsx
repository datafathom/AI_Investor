import React from 'react';
import { StorageService } from '../utils/storageService';
import { Responsive, WidthProvider } from 'react-grid-layout';
import AbuseMonitor from '../widgets/Compliance/AbuseMonitor';
import AuditLog from '../widgets/Compliance/AuditLog';
import SARWorkflow from '../widgets/Compliance/SARWorkflow';
import '../widgets/Compliance/AbuseMonitor.css';
import '../widgets/Compliance/AuditLog.css';
import '../widgets/Compliance/SARWorkflow.css';

// New UI/UX Components
import { StatCard, Badge } from '../components/DataViz';
import { GlassCard } from '../components/Common';

const ResponsiveGridLayout = WidthProvider(Responsive);

const AuditDashboard = () => {
    const layout = [
        { i: 'stats', x: 0, y: 0, w: 12, h: 2 },
        { i: 'abuse', x: 0, y: 2, w: 12, h: 4 },
        { i: 'audit', x: 0, y: 6, w: 8, h: 5 },
        { i: 'sar', x: 8, y: 6, w: 4, h: 5 }
    ];

    const auditStats = [
        { label: 'Events Today', value: 1248, change: 124, status: 'neutral' },
        { label: 'Flagged', value: 3, status: 'warning' },
        { label: 'SARs Pending', value: 0, status: 'positive' },
        { label: 'Compliance Score', value: 98, suffix: '%', status: 'positive' }
    ];

    return (
        <div className="audit-dashboard-page p-6 h-full overflow-y-auto bg-slate-950">
            <header className="mb-6">
                <div className="flex items-center gap-4">
                    <h1 className="text-3xl font-black text-white tracking-tight uppercase">
                        Regulatory Audit
                    </h1>
                    <Badge count="0 SARs" variant="success" />
                </div>
                <p className="text-zinc-500 mt-1">Compliance monitoring, audit logs, and SAR workflows.</p>
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
                <div key="stats" style={{ display: 'flex', gap: '16px' }}>
                    {auditStats.map((stat, idx) => (
                        <div key={idx} style={{ flex: 1 }}>
                            <StatCard {...stat} formatValue={v => v.toLocaleString()} />
                        </div>
                    ))}
                </div>

                <div key="abuse" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                    <GlassCard variant="elevated" hoverable={false} className="h-full">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="font-bold text-white">Abuse Monitor</h3>
                            <Badge count="3 Flagged" variant="warning" />
                        </div>
                        <AbuseMonitor />
                    </GlassCard>
                </div>
                <div key="audit" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                    <GlassCard variant="default" hoverable={false} className="h-full">
                        <h3 className="font-bold text-white mb-4">Audit Log Explorer</h3>
                        <AuditLog />
                    </GlassCard>
                </div>
                <div key="sar" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                    <GlassCard variant="default" status="success" hoverable={false} className="h-full">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="font-bold text-white">SAR Workflow</h3>
                            <Badge count="Clear" variant="success" />
                        </div>
                        <SARWorkflow />
                    </GlassCard>
                </div>
            </ResponsiveGridLayout>
        </div>
    );
};

export default AuditDashboard;
