import React from 'react';

const EquilibriumGauge = ({ maxDrift }) => {
  // Simple gauge visualization
  const rotation = Math.min(Math.max(maxDrift * 18, 0), 180); // Map 0-10% drift to 0-180 deg
  
  return (
    <div className="p-4 bg-gray-800 rounded-lg text-center">
      <h3 className="text-gray-400 text-sm mb-2">Equilibrium Drift</h3>
      <div className="relative w-32 h-16 bg-gray-700 rounded-t-full mx-auto overflow-hidden">
        <div 
          className="absolute bottom-0 left-1/2 w-1 h-14 bg-red-500 origin-bottom transform transition-transform duration-500"
          style={{ transform: `translateX(-50%) rotate(${rotation - 90}deg)` }}
        ></div>
      </div>
      <div className="mt-2 font-bold text-white">
        {maxDrift.toFixed(1)}% Drift
      </div>
    </div>
  );
};

export default EquilibriumGauge;
