import React, { useEffect } from 'react';
import { TrendingDown, Droplet, AlertTriangle, Loader2 } from 'lucide-react';
import useWeb3Store from '../../stores/web3Store';
import './LPTracker.css';

/**
 * LP Position Tracker
 * 
 * Tracks liquidity provider positions with impermanent loss visualization.
 */
const LPPositionTracker = () => {
    const { lpPositions, fetchLPPositions, isLoading } = useWeb3Store();

    useEffect(() => {
        // Fetch LP positions for current user
        fetchLPPositions('current');
    }, [fetchLPPositions]);

    const positions = lpPositions || [];

    if (isLoading && positions.length === 0) {
        return <div className="p-4 flex items-center justify-center text-zinc-500"><Loader2 className="animate-spin mr-2"/> Loading LP Data...</div>;
    }

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
