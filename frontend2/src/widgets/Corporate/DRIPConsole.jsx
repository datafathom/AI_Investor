import React, { useState } from 'react';
import { Repeat, TrendingUp, BarChart2 } from 'lucide-react';
import './DRIPConsole.css';

const DRIPConsole = () => {
    return (
        <div className="drip-console-widget">
             <div className="widget-header">
                <h3><Repeat size={18} className="text-green-400" /> DRIP Management Console</h3>
                <div className="income-summary">
                    <span className="lbl">Est. Annual Income</span>
                    <span className="val">$12,450</span>
                </div>
            </div>

            <div className="snowball-chart">
                {/* Simulated Chart */}
                <svg width="100%" height="100%" viewBox="0 0 300 120">
                    <rect x="0" y="0" width="300" height="120" fill="transparent" />
                    {/* Bars */}
                    <rect x="20" y="80" width="20" height="40" fill="#22c55e" opacity="0.4" />
                    <rect x="50" y="70" width="20" height="50" fill="#22c55e" opacity="0.5" />
                    <rect x="80" y="60" width="20" height="60" fill="#22c55e" opacity="0.6" />
                    <rect x="110" y="45" width="20" height="75" fill="#22c55e" opacity="0.7" />
                    <rect x="140" y="25" width="20" height="95" fill="#22c55e" opacity="0.8" />
                    <rect x="170" y="10" width="20" height="110" fill="#22c55e" opacity="0.9" />
                    
                    {/* Labels */}
                    <text x="35" y="115" fill="#aaa" fontSize="8">Yr1</text>
                    <text x="185" y="115" fill="#aaa" fontSize="8">Yr6</text>
                </svg>
                <div className="chart-overlay-text">Dividend Snowball Projection (5yr)</div>
            </div>

            <div className="holdings-list">
                <div className="holding-item header">
                    <span>Ticker</span>
                    <span>Yield</span>
                    <span>YoC</span>
                    <span>DRIP</span>
                </div>
                 <div className="holding-item">
                    <span className="ticker">NOBL</span>
                    <span className="yield">2.1%</span>
                    <span className="yoc text-green-400">4.5%</span>
                    <div className="toggle active">ON</div>
                </div>
                 <div className="holding-item">
                    <span className="ticker">O</span>
                    <span className="yield">5.2%</span>
                    <span className="yoc text-green-400">6.1%</span>
                    <div className="toggle active">ON</div>
                </div>
                 <div className="holding-item">
                    <span className="ticker">SCHD</span>
                    <span className="yield">3.4%</span>
                    <span className="yoc">3.5%</span>
                    <div className="toggle">OFF</div>
                </div>
            </div>

            <div className="bulk-actions">
                <button className="bulk-btn">Enable All</button>
            </div>
        </div>
    );
};

export default DRIPConsole;
