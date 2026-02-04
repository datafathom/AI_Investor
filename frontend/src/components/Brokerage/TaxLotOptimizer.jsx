import React from 'react';
import { ArrowLeftRight, Trash2 } from 'lucide-react';

const TaxLotOptimizer = () => {
    const lots = [
        { id: 'L102', date: '2023-11-04', symbol: 'TSLA', qty: 50, price: 210.50, current: 245.00, pnl: 1725, term: 'Long' },
        { id: 'L105', date: '2024-02-15', symbol: 'AMD', qty: 100, price: 180.20, current: 165.40, pnl: -1480, term: 'Short' },
        { id: 'L108', date: '2024-03-01', symbol: 'NVDA', qty: 10, price: 850.00, current: 920.00, pnl: 700, term: 'Short' },
    ];

    return (
        <div className="h-full flex flex-col">
            <h3 className="text-xs font-bold text-slate-500 uppercase px-2 mb-2 flex justify-between items-center">
                <span>Tax Lot Harvester</span>
                <span className="text-[10px] text-green-400 bg-green-900/20 px-1 rounded">YTD Realized: $2,450</span>
            </h3>

            <div className="overflow-x-auto">
                <table className="w-full text-left text-xs text-slate-400">
                    <thead className="bg-slate-800/50 uppercase text-[10px]">
                        <tr>
                            <th className="p-2">Date</th>
                            <th className="p-2">Sym</th>
                            <th className="p-2">Term</th>
                            <th className="p-2 text-right">P/L</th>
                            <th className="p-2 text-center">Action</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800">
                        {lots.map(lot => (
                            <tr key={lot.id} className="hover:bg-slate-800/30">
                                <td className="p-2 font-mono">{lot.date}</td>
                                <td className="p-2 font-bold text-slate-300">{lot.symbol}</td>
                                <td className="p-2"><span className={`px-1 rounded text-[10px] ${lot.term === 'Long' ? 'bg-indigo-900/30 text-indigo-400' : 'bg-orange-900/30 text-orange-400'}`}>{lot.term}</span></td>
                                <td className={`p-2 text-right font-mono font-bold ${lot.pnl > 0 ? 'text-green-400' : 'text-red-400'}`}>
                                    {lot.pnl > 0 ? '+' : ''}{lot.pnl}
                                </td>
                                <td className="p-2 text-center">
                                    {lot.pnl < 0 ? (
                                        <button className="text-red-400 hover:text-red-300 hover:bg-red-900/20 p-1 rounded" title="Harvest Loss">
                                            <Trash2 size={14} />
                                        </button>
                                    ) : (
                                        <button className="text-slate-500 hover:text-white hover:bg-slate-700 p-1 rounded" title="Swap">
                                            <ArrowLeftRight size={14} />
                                        </button>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="mt-auto pt-4 flex gap-2 justify-end">
                <button className="px-3 py-1 bg-red-900/30 border border-red-500/30 text-red-400 text-xs rounded hover:bg-red-900/50">
                    Auto-Harvest All Losses
                </button>
            </div>
        </div>
    );
};

export default TaxLotOptimizer;
