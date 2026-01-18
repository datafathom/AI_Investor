import React from 'react';

const CodeDiffViewer = () => {
    // Mock diff
    const lines = [
        { type: 'same', content: 'def process_market_data(df):', num: 42 },
        { type: 'same', content: '    """Normalizes volumes"""', num: 43 },
        { type: 'remove', content: '    df["vol_norm"] = df["volume"] / df["volume"].rolling(20).mean()', num: 44 },
        { type: 'add', content: '    # Use exponential moving average for faster reaction', num: 44 },
        { type: 'add', content: '    df["vol_norm"] = df["volume"] / df["volume"].ewm(span=20).mean()', num: 45 },
        { type: 'same', content: '    return df.dropna()', num: 46 },
    ];

    return (
        <div className="h-full flex flex-col font-mono text-xs">
            <div className="flex justify-between items-center px-4 py-2 bg-slate-900 border-b border-slate-800">
                <span className="text-slate-400">Proposed Changes: <span className="text-yellow-400 font-bold">RiskMetrics.py</span></span>
                <div className="flex gap-2">
                    <span className="text-red-400">-1 line</span>
                    <span className="text-green-400">+2 lines</span>
                </div>
            </div>
            <div className="flex-1 overflow-y-auto bg-[#0a0a0a] p-2">
                {lines.map((line, i) => (
                    <div key={i} className={`flex ${line.type === 'add' ? 'bg-green-900/10' : line.type === 'remove' ? 'bg-red-900/10' : ''}`}>
                        <div className="w-8 text-right pr-2 text-slate-600 select-none border-r border-slate-800 mr-2">{line.num}</div>
                        <div className="w-4 text-center select-none text-slate-500">
                            {line.type === 'add' ? '+' : line.type === 'remove' ? '-' : ''}
                        </div>
                        <div className={`flex-1 whitespace-pre ${line.type === 'add' ? 'text-green-300' : line.type === 'remove' ? 'text-red-400 line-through opacity-60' : 'text-slate-300'}`}>
                            {line.content}
                        </div>
                    </div>
                ))}
            </div>
            <div className="p-2 border-t border-slate-800 flex justify-end gap-2 bg-slate-900">
                <button className="px-3 py-1 bg-slate-800 hover:bg-slate-700 border border-slate-600 rounded text-slate-300 transition-colors">Reject</button>
                <button className="px-3 py-1 bg-green-700/50 hover:bg-green-600/50 border border-green-500/50 text-green-200 rounded transition-colors">Apply Fix</button>
            </div>
        </div>
    );
};

export default CodeDiffViewer;
