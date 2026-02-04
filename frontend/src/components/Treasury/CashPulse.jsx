import React, { useEffect, useState } from 'react';

const CashPulse = () => {
  const [balances, setBalances] = useState({ USD: 45000, JPY: 1200000, EUR: 8500 });
  const [totalUsd, setTotalUsd] = useState(62340);

  return (
    <div className="p-4 bg-gray-900 border border-blue-500/30 rounded-xl shadow-neon-blue">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-blue-400 font-bold tracking-wider uppercase text-xs">Global Cash Pulse</h3>
        <span className="animate-pulse h-2 w-2 bg-green-500 rounded-full"></span>
      </div>
      
      <div className="space-y-3">
        {Object.entries(balances).map(([curr, amt]) => (
          <div key={curr} className="flex justify-between items-center text-sm">
            <span className="text-gray-400">{curr}</span>
            <span className="text-white font-mono">{amt.toLocaleString()}</span>
          </div>
        ))}
      </div>
      
      <div className="mt-4 pt-4 border-t border-gray-800 text-center">
        <span className="text-gray-500 text-xs">Total Liquid Value</span>
        <div className="text-2xl font-bold text-green-400">${totalUsd.toLocaleString()}</div>
      </div>
    </div>
  );
};

export default CashPulse;
