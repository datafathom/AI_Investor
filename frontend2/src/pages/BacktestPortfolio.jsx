import React, { useState } from 'react';
import { Responsive, WidthProvider } from 'react-grid-layout';
import MonteCarlo from '../widgets/Backtest/MonteCarlo';
import DrawdownTimeline from '../widgets/Backtest/DrawdownTimeline';
import OverfitWarning from '../widgets/Backtest/OverfitWarning';
import '../widgets/Backtest/MonteCarlo.css';
import '../widgets/Backtest/DrawdownTimeline.css';
import '../widgets/Backtest/OverfitWarning.css';

const ResponsiveGridLayout = WidthProvider(Responsive);
import PageHeader from '../components/Navigation/PageHeader';
import { Zap } from 'lucide-react';

const BacktestPortfolio = () => {
    // Advanced V2 Layout
    const DEFAULT_LAYOUT = {
        lg: [
            { i: 'monte_carlo', x: 0, y: 0, w: 8, h: 5 },
            { i: 'overfit', x: 8, y: 0, w: 4, h: 5 },
            { i: 'drawdown', x: 0, y: 5, w: 12, h: 4 }
        ]
    };
    const STORAGE_KEY = 'layout_backtest_dashboard';

    const [layouts, setLayouts] = useState(() => {
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
        <div className="backtest-dashboard-page" style={{ padding: '20px' }}>
            <h2 style={{ color: 'var(--text-primary)', marginBottom: '20px' }}>Advanced Backtest Explorer</h2>
            
            <ResponsiveGridLayout
                className="layout"
                layouts={layouts}
                onLayoutChange={onLayoutChange}
                breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
                cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
                rowHeight={100}
                isDraggable={true}
                isResizable={true}
            >
                <div key="monte_carlo" style={{ background: 'var(--bg-secondary)', borderRadius: '8px', overflow: 'hidden' }} data-tour-id="monte-carlo-widget">
                    <MonteCarlo />
                </div>
                <div key="overfit" style={{ background: 'var(--bg-secondary)', borderRadius: '8px', overflow: 'hidden' }} data-tour-id="overfit-warning-widget">
                    <OverfitWarning />
                </div>
                <div key="drawdown" style={{ background: 'var(--bg-secondary)', borderRadius: '8px', overflow: 'hidden' }} data-tour-id="drawdown-timeline-widget">
                    <DrawdownTimeline />
                </div>
            </ResponsiveGridLayout>
        </div>
    );
};

export default BacktestPortfolio;
