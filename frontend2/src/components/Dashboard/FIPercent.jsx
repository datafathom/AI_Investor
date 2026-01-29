import React from 'react';

const FIPercent = ({ currentPercentage }) => {
  return (
    <div className="p-8 bg-gray-900 rounded-3xl border border-blue-500/20 text-center shadow-neon-blue">
      <h3 className="text-gray-500 uppercase text-[10px] tracking-[4px] mb-4">Financial Independence</h3>
      <div className="text-7xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-green-400">
        {currentPercentage}%
      </div>
      <div className="mt-4 h-2 bg-gray-800 rounded-full mx-auto w-48 overflow-hidden">
        <div className="h-full bg-gradient-to-r from-blue-500 to-green-500" style={{ width: `${currentPercentage}%` }}></div>
      </div>
      <p className="mt-4 text-xs text-gray-400 italic">"Freedom is the ability to walk away from anything that doesn't respect you."</p>
    </div>
  );
};

export default FIPercent;
