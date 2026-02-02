/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Web3/LiquidityLattice.jsx
 * ROLE: Real-time Liquidity Depth & Slippage Visualizer
 * PURPOSE: Visualizes pool depth and projected slippage for Web3 assets.
 * ==============================================================================
 */

import React, { useEffect, useMemo } from 'react';
import { Layers, Droplets, Info, AlertTriangle, TrendingUp } from 'lucide-react';
import useWeb3Store from '../../stores/web3Store';
import './LiquidityLattice.css';

const LiquidityLattice = ({ poolAddress = '0xUniV3-ETH-USDC' }) => {
    const { liquidityDepth, fetchLiquidityDepth } = useWeb3Store();

    useEffect(() => {
        if (poolAddress) {
            fetchLiquidityDepth(poolAddress);
            const interval = setInterval(() => fetchLiquidityDepth(poolAddress), 30000);
            return () => clearInterval(interval);
        }
    }, [poolAddress, fetchLiquidityDepth]);

    const data = useMemo(() => liquidityDepth[poolAddress], [liquidityDepth, poolAddress]);

    if (!data) {
        return (
            <div className="liquidity-lattice flex items-center justify-center">
                <div className="animate-pulse text-slate-500 text-[10px] uppercase font-bold">Scanning Pool depth...</div>
            </div>
        );
    }

    const maxLiq = Math.max(...data.levels.map(l => l.liquidity));

    return (
        <div className="liquidity-lattice">
            <div className="liquidity-lattice__header">
                <div className="flex items-center gap-2">
                    <Droplets size={16} className="text-blue-400" />
                    <h3 className="text-sm font-bold text-white uppercase tracking-wider">Liquidity Lattice</h3>
                </div>
                <div className="text-[10px] font-mono text-blue-400">
                    Slippage: <span className="text-white font-bold">{(data.slippage_100k * 100).toFixed(3)}%</span>
                </div>
            </div>

            <div className="liquidity-lattice__chart">
                {data.levels.map((level, idx) => (
                    <div key={idx} className="liquidity-lattice__row">
                        <div 
                            className={`liquidity-lattice__label ${level.is_current ? 'text-white font-bold' : 'text-slate-500'}`}
                        >
                            {level.price.toFixed(2)}
                        </div>
                        <div className="liquidity-lattice__bar-container">
                            <div 
                                className={`liquidity-lattice__bar ${level.is_current ? 'bg-blue-400' : 'bg-blue-400/20'}`}
                                style={{ 
                                    width: `${(level.liquidity / maxLiq) * 100}%`,
                                    opacity: level.is_current ? 1 : 0.6
                                }}
                            />
                        </div>
                        <div className="text-[9px] text-slate-600 font-mono text-right w-8">
                            {level.liquidity.toFixed(1)}k
                        </div>
                    </div>
                ))}
            </div>

            <div className="liquidity-lattice__overlay">
                <div className="text-[10px] text-white/50 mb-1">Total Pool Depth</div>
                <div className="text-lg font-black text-white">${(data.total_liquidity_usd / 1000000).toFixed(2)}M</div>
            </div>

            <div className="liquidity-lattice__footer">
                <div className="flex items-center gap-1 text-[9px] text-amber-500 bg-amber-500/10 px-2 py-0.5 rounded">
                    <AlertTriangle size={10} />
                    <span>Watch for high-slippage zones</span>
                </div>
                <div className="text-[9px] font-mono text-slate-500">
                    POOL: {poolAddress.substring(0, 10)}...
                </div>
            </div>
        </div>
    );
};

export default LiquidityLattice;
