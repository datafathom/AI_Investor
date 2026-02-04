import React from 'react';
import { StorageService } from '../utils/storageService';
import { Responsive, WidthProvider } from 'react-grid-layout';
import EarningsCalendar from '../widgets/Corporate/EarningsCalendar';
import DRIPConsole from '../widgets/Corporate/DRIPConsole';
import CorporateActions from '../widgets/Corporate/CorporateActions';
import '../widgets/Corporate/EarningsCalendar.css';

// New UI/UX Components
import { StatCard, Badge } from '../components/DataViz';
import { GlassCard } from '../components/Common';

const ResponsiveGridLayout = WidthProvider(Responsive);

const CorporateDashboard = () => {
    const layout = [
        { i: 'stats', x: 0, y: 0, w: 12, h: 2 },
        { i: 'calendar', x: 0, y: 2, w: 6, h: 5 },
        { i: 'drip', x: 6, y: 2, w: 6, h: 5 },
        { i: 'actions', x: 0, y: 7, w: 12, h: 4 }
    ];

    const corpStats = [
        { label: 'Upcoming Earnings', value: 8, status: 'neutral' },
        { label: 'DRIP Active', value: 12, suffix: ' stocks', status: 'positive' },
        { label: 'Pending Actions', value: 3, status: 'warning' },
        { label: 'Dividends YTD', value: 4850, prefix: '$', status: 'positive' }
    ];

    return (
        <div className="corporate-dashboard-page p-6 h-full overflow-y-auto bg-slate-950">
            <header className="mb-6">
                <div className="flex items-center gap-4">
                    <h1 className="text-3xl font-black text-white tracking-tight uppercase">
                        Corporate Actions
                    </h1>
                    <Badge count="3 Pending" variant="warning" />
                </div>
                <p className="text-zinc-500 mt-1">Earnings calendar, DRIP management, and corporate events.</p>
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
                    {corpStats.map((stat, idx) => (
                        <div key={idx} style={{ flex: 1 }}>
                            <StatCard {...stat} formatValue={v => v.toLocaleString()} />
                        </div>
                    ))}
                </div>

                <div key="calendar" style={{ borderRadius: '12px', overflow: 'hidden' }} data-tour-id="earnings-calendar-widget">
                    <GlassCard variant="elevated" hoverable={false} className="h-full">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="font-bold text-white">Earnings Calendar</h3>
                            <Badge count="8 This Week" variant="info" />
                        </div>
                        <EarningsCalendar />
                    </GlassCard>
                </div>
                <div key="drip" style={{ borderRadius: '12px', overflow: 'hidden' }} data-tour-id="drip-console-widget">
                    <GlassCard variant="elevated" status="success" hoverable={false} className="h-full">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="font-bold text-white">DRIP Console</h3>
                            <Badge count="12 Active" variant="success" />
                        </div>
                        <DRIPConsole />
                    </GlassCard>
                </div>
                <div key="actions" style={{ borderRadius: '12px', overflow: 'hidden' }} data-tour-id="corporate-actions-widget">
                    <GlassCard variant="default" status="warning" hoverable={false} className="h-full">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="font-bold text-white">Corporate Actions</h3>
                            <Badge count="3 Pending" variant="warning" />
                        </div>
                        <CorporateActions />
                    </GlassCard>
                </div>
            </ResponsiveGridLayout>
        </div>
    );
};

export default CorporateDashboard;
