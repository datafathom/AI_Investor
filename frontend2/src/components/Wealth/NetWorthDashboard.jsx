import React from 'react';

const NetWorthDashboard = ({ netWorth, breakdown }) => {
  return (
    <div className="p-6 bg-gray-900 min-h-screen text-white">
      <h1 className="text-3xl font-bold mb-4">Total Wealth</h1>
      <div className="text-5xl font-mono text-green-400 mb-8">
        ${netWorth?.toLocaleString()}
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {Object.entries(breakdown || {}).map(([source, amount]) => (
          <div key={source} className="p-4 bg-gray-800 rounded border border-gray-700">
            <h3 className="text-gray-400 uppercase text-xs">{source}</h3>
            <div className="text-xl font-bold">${amount.toLocaleString()}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default NetWorthDashboard;
