import React from 'react';
import { TrendingDown, Droplet, AlertTriangle } from 'lucide-react';
import './LPTracker.css';

/**
 * LP Position Tracker
 * 
 * Tracks liquidity provider positions with impermanent loss visualization.
 */
const LPPositionTracker = () => {
    const positions = [
        {
            id: 1,
            pool: 'ETH/USDC',
            protocol: 'Uniswap V3',
            liquidity: 15000,
            depositValue: 14200,
            currentValue: 13850,
            impermanentLoss: -2.46,
            fees: 320,
            apr: 18.5,
        },
        {
            id: 2,
            pool: 'SOL/USDT',
            protocol: 'Raydium',
            liquidity: 8500,
            depositValue: 8000,
            currentValue: 8200,
            impermanentLoss: -1.12,
            fees: 180,
            apr: 24.2,
        },
        {
            id: 3,
            pool: 'WBTC/ETH',
            protocol: 'Curve',
            liquidity: 25000,
            depositValue: 24500,
            currentValue: 23800,
            impermanentLoss: -3.85,
            fees: 520,
            apr: 12.8,
        },
    ];

    const totalLiquidity = positions.reduce((sum, p) => sum + p.liquidity, 0);
    const totalFees = positions.reduce((sum, p) => sum + p.fees, 0);
    const totalPnL = positions.reduce((sum, p) => sum + (p.currentValue - p.depositValue + p.fees), 0);

    return (
        <div className="lp-tracker">
            <div className="tracker-header">
                <h3>LP Position Tracker</h3>
                <div className="summary-stats">
                    <div className="stat">
                        <span className="label">Total Liquidity</span>
                        <span className="value">${totalLiquidity.toLocaleString()}</span>
                    </div>
                    <div className="stat">
                        <span className="label">Fees Earned</span>
                        <span className="value positive">+${totalFees.toLocaleString()}</span>
                    </div>
                    <div className="stat">
                        <span className="label">Net P&L</span>
                        <span className={`value ${totalPnL >= 0 ? 'positive' : 'negative'}`}>
                            {totalPnL >= 0 ? '+' : ''}${totalPnL.toLocaleString()}
                        </span>
                    </div>
                </div>
            </div>

            <div className="positions-list">
                {positions.map((pos) => (
                    <div key={pos.id} className="position-card">
                        <div className="position-header">
                            <div className="pool-info">
                                <span className="pool-name">{pos.pool}</span>
                                <span className="protocol">{pos.protocol}</span>
                            </div>
                            <span className="apr-badge">{pos.apr}% APR</span>
                        </div>

                        <div className="position-values">
                            <div className="value-item">
                                <span className="label">Deposited</span>
                                <span className="value">${pos.depositValue.toLocaleString()}</span>
                            </div>
                            <div className="value-item">
                                <span className="label">Current</span>
                                <span className="value">${pos.currentValue.toLocaleString()}</span>
                            </div>
                            <div className="value-item">
                                <span className="label">Fees</span>
                                <span className="value positive">+${pos.fees}</span>
                            </div>
                        </div>

                        <div className="il-indicator">
                            <div className="il-bar">
                                <div 
                                    className="il-fill" 
                                    style={{ width: `${Math.min(Math.abs(pos.impermanentLoss) * 10, 100)}%` }}
                                ></div>
                            </div>
                            <div className="il-label">
                                <TrendingDown size={12} />
                                <span>IL: {pos.impermanentLoss}%</span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            <div className="tracker-footer">
                <AlertTriangle size={12} />
                <span>IL represents the opportunity cost vs. simply holding the assets</span>
            </div>
        </div>
    );
};

export default LPPositionTracker;
