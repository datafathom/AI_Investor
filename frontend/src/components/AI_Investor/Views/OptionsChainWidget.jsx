import React, { useState, useEffect } from 'react';
import { Target } from 'lucide-react';
import { useSymbolLinking } from '../../../hooks/useSymbolLinking';
import { useTradingStore } from '../../../store/tradingStore';

const OptionsChainWidget = ({ linkingGroup = 'none' }) => {
    const { optionsChain, setOptionsExpiration, updateOptionsStrikes } = useTradingStore();
    const { groups, setGroupTicker } = useSymbolLinking();
    const [view, setView] = useState('calls');

    // Get current ticker from linking group or default
    const currentTicker = linkingGroup !== 'none' ? groups[linkingGroup] : optionsChain.ticker;

    useEffect(() => {
        const generateMockStrikes = () => {
            // Seed base price from ticker name for variety
            const charSum = currentTicker.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
            const centerStrike = 100 + (charSum % 800);
            
            const newStrikes = Array.from({ length: 15 }, (_, i) => {
                const strike = centerStrike - 15 + i * 2;
                const distance = Math.abs(strike - centerStrike);
                return {
                    strike,
                    bid: (20 - distance * 0.5 + Math.random()).toFixed(2),
                    ask: (20.5 - distance * 0.5 + Math.random()).toFixed(2),
                    delta: (0.9 - (i * 0.08) + Math.random() * 0.05).toFixed(2),
                    gamma: (0.01 + Math.random() * 0.005).toFixed(3),
                    theta: (-0.5 - Math.random() * 0.1).toFixed(2),
                    vega: (0.15 + Math.random() * 0.05).toFixed(2),
                    iv: (18 + Math.random() * 2).toFixed(1)
                };
            });
            updateOptionsStrikes(newStrikes);
        };

        generateMockStrikes();
        const interval = setInterval(generateMockStrikes, 2000);
        return () => clearInterval(interval);
    }, [updateOptionsStrikes, currentTicker]);

    return (
        <div className="options-chain-widget glass">
            <div className="options-toolbar">
                <div
                    className={`ticker-badge group-${linkingGroup}`}
                    onClick={() => {
                        const newTicker = prompt('Enter new symbol:', currentTicker);
                        if (newTicker) {
                            if (linkingGroup !== 'none') {
                                setGroupTicker(linkingGroup, newTicker.toUpperCase());
                            } else {
                                // Update local only (if store supported per-widget ticker)
                            }
                        }
                    }}
                >
                    <Target size={16} />
                    <span>{currentTicker}</span>
                </div>
                <div className="expiration-selector">
                    <label>Exp:</label>
                    <select
                        value={optionsChain.selectedExpiration}
                        onChange={(e) => setOptionsExpiration(e.target.value)}
                    >
                        {optionsChain.expirations.map(exp => (
                            <option key={exp} value={exp}>{exp}</option>
                        ))}
                    </select>
                </div>
                <div className="view-switcher">
                    <button
                        className={view === 'calls' ? 'active' : ''}
                        onClick={() => setView('calls')}
                    >Calls</button>
                    <button
                        className={view === 'puts' ? 'active' : ''}
                        onClick={() => setView('puts')}
                    >Puts</button>
                </div>
            </div>

            <div className="chain-table-container">
                <table className="options-table">
                    <thead>
                        <tr>
                            <th>Delta</th>
                            <th>Theta</th>
                            <th>IV %</th>
                            <th className="strike-col">Strike</th>
                            <th>Bid</th>
                            <th>Ask</th>
                            <th>Gamma</th>
                            <th>Vega</th>
                        </tr>
                    </thead>
                    <tbody>
                        {optionsChain.strikes.map((s) => (
                            <tr key={s.strike} className={s.strike === 480 ? 'at-the-money' : ''}>
                                <td className="greek-val">{s.delta}</td>
                                <td className="greek-val">{s.theta}</td>
                                <td className="iv-val">{s.iv}</td>
                                <td className="strike-val">{s.strike}</td>
                                <td className="bid-val">{s.bid}</td>
                                <td className="ask-val">{s.ask}</td>
                                <td className="greek-val">{s.gamma}</td>
                                <td className="greek-val">{s.vega}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default OptionsChainWidget;
