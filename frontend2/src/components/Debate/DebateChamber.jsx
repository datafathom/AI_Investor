import React from 'react';

const DebateChamber = ({ arguments_list, consensus }) => {
  return (
    <div className="p-6 bg-gray-900 rounded-lg">
      <h2 className="text-2xl font-bold text-white mb-4">Debate Chamber</h2>
      
      {/* Consensus Bar */}
      <div className="mb-6">
        <div className="flex justify-between text-sm text-gray-400 mb-1">
          <span>Bearish</span>
          <span>Bullish</span>
        </div>
        <div className="h-4 bg-gray-700 rounded-full overflow-hidden flex">
          <div className="h-full bg-red-500" style={{ width: `${consensus.bear_sentiment * 100}%` }}></div>
          <div className="h-full bg-green-500" style={{ width: `${consensus.bull_sentiment * 100}%` }}></div>
        </div>
      </div>
      
      {/* Cards */}
      <div className="space-y-4">
        {arguments_list.map((arg, i) => (
          <div key={i} className="p-4 bg-gray-800 border-l-4 border-blue-500 rounded">
            <h4 className="text-sm font-bold text-blue-300">{arg.persona}</h4>
            <p className="text-gray-200 mt-1">{arg.argument}</p>
            <span className="text-xs text-gray-500">Conf: {(arg.confidence * 100).toFixed(0)}%</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DebateChamber;
