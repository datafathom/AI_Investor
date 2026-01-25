import React from 'react';
import { Responsive, WidthProvider } from 'react-grid-layout';
import WalletDashboard from '../widgets/Crypto/CryptoWalletDashboard';
import LPTracker from '../widgets/Crypto/LPPositionTracker';
import GasPulse from '../widgets/Crypto/GasPulse';
import WalletLinkWidget from '../widgets/Crypto/WalletLinkWidget';
import '../widgets/Crypto/CryptoWallet.css';

// New UI/UX Components
import StatCard from '../components/DataViz/StatCard';
import GlassCard from '../components/Common/GlassCard';

const ResponsiveGridLayout = WidthProvider(Responsive);

const CryptoDashboard = () => {
    const DEFAULT_LAYOUT = {
        lg: [
            { i: 'stats', x: 0, y: 0, w: 12, h: 2 },
            { i: 'wallet', x: 0, y: 2, w: 6, h: 4 },
            { i: 'lp', x: 6, y: 2, w: 6, h: 4 },
            { i: 'gas', x: 0, y: 6, w: 4, h: 3 },
            { i: 'link', x: 4, y: 6, w: 8, h: 3 }
        ]
    };
    const STORAGE_KEY = 'layout_crypto_dashboard';

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

    // Mock data for StatCards
    const cryptoStats = [
        { label: 'Total Value', value: 142850, prefix: '$', change: 2840, status: 'positive', sparklineData: [140, 138, 142, 145, 141, 143] },
        { label: 'ETH Balance', value: 24.5, suffix: ' ETH', change: 0.8, status: 'positive', sparklineData: [23, 24, 23.5, 24.2, 24.5] },
        { label: 'Gas (Gwei)', value: 28, suffix: ' gwei', change: -12, status: 'positive', sparklineData: [45, 38, 32, 28, 30, 28] },
        { label: 'Active LPs', value: 6, change: 1, status: 'neutral', sparklineData: [5, 5, 5, 6, 6, 6] },
    ];

    return (
        <div className="full-bleed-page crypto-dashboard-page">
            <header className="mb-6">
                <h1 className="text-3xl font-black text-white tracking-tight uppercase mb-1">
                    Crypto & Web3 Vault
                </h1>
                <p className="text-zinc-500">DeFi positions, wallet balances, and gas tracking.</p>
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
                        {cryptoStats.map((stat, idx) => (
                            <div key={idx} style={{ flex: 1 }}>
                                <StatCard 
                                    {...stat} 
                                    formatValue={v => stat.prefix === '$' ? v.toLocaleString() : v.toFixed(stat.suffix === ' ETH' ? 1 : 0)}
                                />
                            </div>
                        ))}
                    </div>
                    
                    <div key="wallet" style={{ borderRadius: '12px', overflow: 'hidden' }} data-tour-id="wallet-balances">
                        <GlassCard variant="elevated" hoverable={false} className="h-full">
                            <WalletDashboard />
                        </GlassCard>
                    </div>
                    <div key="lp" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                        <GlassCard variant="elevated" hoverable={false} className="h-full">
                            <LPTracker />
                        </GlassCard>
                    </div>
                    <div key="gas" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                        <GlassCard variant="default" hoverable={false} className="h-full">
                            <GasPulse />
                        </GlassCard>
                    </div>
                    <div key="link" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                        <GlassCard variant="default" hoverable={false} className="h-full">
                            <WalletLinkWidget />
                        </GlassCard>
                    </div>
                </ResponsiveGridLayout>
                
                {/* Bottom Buffer */}
                <div className="scroll-buffer-100" />
            </div>
        </div>
    );
};

export default CryptoDashboard;
