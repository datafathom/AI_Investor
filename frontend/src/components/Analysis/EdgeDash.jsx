import React, { useEffect, useState } from 'react';
import ExpectancyCurve from './ExpectancyCurve';

const EdgeDash = () => {
  const [stats, setStats] = useState({ expectancy: 0.6, winRate: 0.4, rr: 3.0 });

  return (
    <div className="p-6 bg-gray-900 min-h-screen text-white">
      <h1 className="text-3xl font-bold mb-6">Edge Verification Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <ExpectancyCurve data={stats} />
        
        <div className="p-4 bg-gray-800 rounded-lg">
          <h3 className="text-xl font-bold text-blue-400 mb-4">Core Metrics</h3>
          <ul className="space-y-2">
            <li>Win Rate: {(stats.winRate * 100).toFixed(1)}%</li>
            <li>Avg Risk/Reward: 1:{stats.rr}</li>
            <li>Projected Alpha: +{(stats.expectancy * 100).toFixed(0)} bps</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default EdgeDash;
