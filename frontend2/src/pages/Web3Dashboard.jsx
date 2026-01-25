import React from 'react';
import { Responsive, WidthProvider } from 'react-grid-layout';
import WalletDashboard from '../widgets/Web3/WalletDashboard';
import LPTracker from '../widgets/Web3/LPTracker';
import GasPulse from '../widgets/Web3/GasPulse';
import { GlassCard } from '../components/Common';
import { Badge } from '../components/DataViz';

const ResponsiveGridLayout = WidthProvider(Responsive);

const Web3Dashboard = () => {
    const layout = [
        { i: 'wallet', x: 0, y: 0, w: 8, h: 4 },
        { i: 'gas', x: 8, y: 0, w: 4, h: 4 },
        { i: 'lp', x: 0, y: 4, w: 12, h: 5 },
    ];

    return (
        <div className="web3-dashboard p-6 h-full overflow-y-auto bg-slate-950">
             <header className="mb-6 flex justify-between items-end">
                <div>
                    <div className="flex items-center gap-3 mb-1">
                        <h1 className="text-3xl font-black text-white tracking-tight uppercase">
                            DeFi Vault
                        </h1>
                        <Badge count="Ledger Live" variant="success" pulse />
                    </div>
                    <p className="text-zinc-500">Hardware wallet monitoring, LP positions, and Gas optimization.</p>
                </div>
            </header>

            <ResponsiveGridLayout
                className="layout"
                layouts={{ lg: layout }}
                breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
                cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
                rowHeight={100}
                isDraggable={true}
                isResizable={true}
                margin={[16, 16]}
            >
                <div key="wallet">
                    <GlassCard variant="elevated" hoverable={false} className="h-full">
                        <h3 className="font-bold text-white mb-3">Hardware Vault</h3>
                        <div className="h-[calc(100%-32px)]">
                             <WalletDashboard />
                        </div>
                    </GlassCard>
                </div>

                <div key="gas">
                    <GlassCard variant="default" hoverable={false} className="h-full">
                         <h3 className="font-bold text-white mb-3">Gas Metabolism</h3>
                         <div className="h-[calc(100%-32px)]">
                             <GasPulse />
                         </div>
                    </GlassCard>
                </div>

                <div key="lp">
                     <GlassCard variant="elevated" hoverable={false} className="h-full">
                        <h3 className="font-bold text-white mb-3">Liquidity Positions & IL Audit</h3>
                        <div className="h-[calc(100%-32px)]">
                            <LPTracker />
                        </div>
                    </GlassCard>
                </div>

            </ResponsiveGridLayout>
        </div>
    );
};

export default Web3Dashboard;
