import React from 'react';
import { Wallet } from 'lucide-react';

const PortfolioWidget = () => {
    const positions = [
        { symbol: 'TSLA', shares: 10, price: '215.42', value: '2,154.20', change: '+4.2%' },
        { symbol: 'NVDA', shares: 5, price: '480.12', value: '2,400.60', change: '+1.8%' },
        { symbol: 'BTC', shares: 0.1, price: '43,200.00', value: '4,320.00', change: '-0.5%' },
    ];

    return (
        <div className="space-y-4 p-4 h-full overflow-auto">
            <div className="glass-card border-neon-cyan shadow-[0_0_20px_rgba(0,242,255,0.1)] p-6">
                <div className="flex items-center justify-between mb-6">
                    <div>
                        <h4 className="text-dim text-xs uppercase tracking-wider">Total Account Value</h4>
                        <h2 className="text-3xl font-bold text-main mt-1">$8,874.80</h2>
                    </div>
                    <div className="p-3 bg-cyan-500/10 rounded-full border border-cyan-500/30">
                        <Wallet className="text-cyan-400" size={24} />
                    </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4 border-t border-white/5">
                    <div>
                        <p className="text-[10px] text-dim uppercase">Buying Power</p>
                        <p className="text-base text-main">$2,542.40</p>
                    </div>
                    <div>
                        <p className="text-[10px] text-dim uppercase">Day Profit</p>
                        <p className="text-base text-green-400">+$142.10</p>
                    </div>
                    <div>
                        <p className="text-[10px] text-dim uppercase">Open Positions</p>
                        <p className="text-base text-main">3</p>
                    </div>
                    <div>
                        <p className="text-[10px] text-dim uppercase">System Margin</p>
                        <p className="text-base text-purple-400">0.00</p>
                    </div>
                </div>
            </div>

            <div className="glass-card p-4">
                <h3 className="neon-text mb-4 text-sm">Asset Allocation</h3>
                <div className="overflow-x-auto">
                    <table className="w-full text-left">
                        <thead className="text-dim text-[10px] uppercase tracking-wider border-b border-white/5">
                            <tr>
                                <th className="pb-2">Asset</th>
                                <th className="pb-2">Quantity</th>
                                <th className="pb-2">Price</th>
                                <th className="pb-2">Value</th>
                                <th className="pb-2">24h Change</th>
                            </tr>
                        </thead>
                        <tbody className="text-main text-sm">
                            {positions.map((pos) => (
                                <tr key={pos.symbol} className="border-b border-white/5 hover:bg-white/5 transition-colors group">
                                    <td className="py-3 font-bold text-cyan-400">{pos.symbol}</td>
                                    <td className="py-3">{pos.shares}</td>
                                    <td className="py-3">${pos.price}</td>
                                    <td className="py-3">${pos.value}</td>
                                    <td className={`py-3 ${pos.change.includes('+') ? 'text-green-400' : 'text-red-400'}`}>
                                        {pos.change}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default PortfolioWidget;
