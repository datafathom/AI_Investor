import React from 'react';

const SeqRisk = () => {
  return (
    <div className="p-4 bg-gray-900 rounded-lg">
      <h3 className="text-red-400 font-bold mb-4">Sequence of Returns: Danger Zone</h3>
      <div className="h-32 bg-black/40 border border-red-500/20 rounded relative p-4 flex flex-col justify-center">
        <div className="text-xs text-gray-500 mb-1">RETIREMENT YEAR 0 -> YEAR 5</div>
        <div className="text-xl font-bold text-white uppercase italic">Impact of -20% Drawdown:</div>
        <div className="text-sm text-red-500 font-bold">REDUCES SUCCESS RATE FROM 98% TO 62%</div>
        <div className="absolute top-0 right-0 p-2 text-red-500/20 text-4xl">⚠️</div>
      </div>
    </div>
  );
};

export default SeqRisk;
