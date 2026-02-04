import React from 'react';

const Drift = () => {
  return (
    <div className="p-4 bg-gray-900 rounded-lg">
      <h3 className="text-white font-bold mb-4">Portfolio Drift Tracker</h3>
      <div className="space-y-4">
        <div>
            <div className="flex justify-between text-[10px] mb-1">
                <span className="text-gray-400 uppercase">Growth (60% Target)</span>
                <span className="text-red-400 font-bold">+5.2% OVER</span>
            </div>
            <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                <div className="h-full bg-red-500 w-2/3"></div>
            </div>
        </div>
        <div>
            <div className="flex justify-between text-[10px] mb-1">
                <span className="text-gray-400 uppercase">Stability (40% Target)</span>
                <span className="text-green-400 font-bold">-5.2% UNDER</span>
            </div>
            <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                <div className="h-full bg-green-500 w-1/3"></div>
            </div>
        </div>
      </div>
    </div>
  );
};

export default Drift;
