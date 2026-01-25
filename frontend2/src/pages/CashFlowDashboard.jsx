import React, { useState } from 'react';
import { Responsive, WidthProvider } from 'react-grid-layout';
import PlaidLinkWidget from '../widgets/Banking/PlaidLinkWidget';
import ReconciliationReport from '../widgets/Banking/ReconciliationReport';
import 'react-grid-layout/css/styles.css';

// New UI/UX Components
import { StatCard, Badge } from '../components/DataViz';
import { GlassCard } from '../components/Common';

const ResponsiveGridLayout = WidthProvider(Responsive);

const CashFlowDashboard = () => {
    const [layouts, setLayouts] = useState({
        lg: [
            { i: 'stats', x: 0, y: 0, w: 12, h: 2 },
            { i: 'plaid-link', x: 0, y: 2, w: 6, h: 4 },
            { i: 'recon-report', x: 6, y: 2, w: 6, h: 6 },
            { i: 'cash-summary', x: 0, y: 6, w: 6, h: 2 }
        ]
    });

    const cashStats = [
        { label: 'Total Liquidity', value: 0, prefix: '$', status: 'neutral' },
        { label: 'Linked Accounts', value: 0, status: 'neutral' },
        { label: 'Pending Recon', value: 0, status: 'positive' },
        { label: 'Net Inflow', value: 0, prefix: '$', status: 'neutral' }
    ];

    return (
        <div className="full-bleed-page cash-flow-dashboard">
            <header className="mb-6">
                <div className="flex items-center gap-4">
                    <h1 className="text-3xl font-black text-white tracking-tight uppercase">
                        Cash Flow & Liquidity
                    </h1>
                    <Badge count="Plaid Ready" variant="info" />
                </div>
                <p className="text-zinc-500 mt-1">Real-capital banking connections and institutional liquidity.</p>
            </header>

            <div className="scrollable-content-wrapper">
                <ResponsiveGridLayout
                    className="layout"
                    layouts={layouts}
                    breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
                    cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
                    rowHeight={80}
                    onLayoutChange={(l, all) => setLayouts(all)}
                    isDraggable={true}
                    isResizable={true}
                    draggableHandle="h3, h4"
                >
                    <div key="stats" style={{ display: 'flex', gap: '16px' }}>
                        {cashStats.map((stat, idx) => (
                            <div key={idx} style={{ flex: 1 }}>
                                <StatCard {...stat} formatValue={v => v.toLocaleString()} />
                            </div>
                        ))}
                    </div>

                    <div key="plaid-link" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                        <GlassCard variant="elevated" hoverable={false} className="h-full">
                            <h3 className="font-bold text-white mb-4">Bank Connections</h3>
                            <PlaidLinkWidget />
                        </GlassCard>
                    </div>
                    <div key="recon-report" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                        <GlassCard variant="elevated" hoverable={false} className="h-full">
                            <div className="flex justify-between items-center mb-3">
                                <h3 className="font-bold text-white">Reconciliation Report</h3>
                                <Badge count="Synced" variant="success" />
                            </div>
                            <ReconciliationReport />
                        </GlassCard>
                    </div>
                    <div key="cash-summary" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                        <GlassCard variant="default" hoverable={false} className="h-full flex items-center justify-center">
                            <div className="text-center">
                                <h4 className="text-zinc-500 uppercase text-xs font-bold tracking-widest mb-2">Total Managed Liquidity</h4>
                                <span className="text-4xl font-mono text-cyan-400">$0.00</span>
                            </div>
                        </GlassCard>
                    </div>
                </ResponsiveGridLayout>
                
                {/* Bottom Buffer */}
                <div className="scroll-buffer-100" />
            </div>
        </div>
    );
};

export default CashFlowDashboard;
