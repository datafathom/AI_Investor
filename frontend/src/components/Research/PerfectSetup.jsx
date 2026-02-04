import React from 'react';

const PerfectSetup = () => {
  return (
    <div className="p-6 bg-gray-900 rounded-xl border border-blue-500/30 shadow-neon-blue">
      <h2 className="text-xl font-bold text-white mb-6 italic">Quantamental Confluence</h2>
      
      <div className="space-y-4">
        {[
            { ticker: 'PLTR', score: 96, tech: 'BULLISH', macro: 'EXPANSION', fund: 'VALUE' },
            { ticker: 'DKNG', score: 92, tech: 'BREAKOUT', macro: 'EXPANSION', fund: 'GROWTH' }
        ].map(s => (
            <div key={s.ticker} className="p-4 bg-black/40 rounded border-l-4 border-blue-500 flex justify-between items-center">
                <div>
                    <div className="text-xl font-bold text-white">{s.ticker}</div>
                    <div className="text-[10px] text-gray-500 font-mono">{s.tech} / {s.macro} / {s.fund}</div>
                </div>
                <div className="text-3xl font-bold text-blue-400">{s.score}</div>
            </div>
        ))}
      </div>
    </div>
  );
};

export default PerfectSetup;
