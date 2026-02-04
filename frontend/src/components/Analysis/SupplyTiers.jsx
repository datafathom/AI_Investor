import React from 'react';

const SupplyTiers = () => {
  return (
    <div className="p-6 bg-gray-900 border border-blue-500/10 rounded-xl">
      <h3 className="text-blue-300 font-bold text-sm mb-6">Tier-N Dependency Tree (NVDA)</h3>
      
      <div className="space-y-4">
        <div className="flex gap-4 items-center">
            <div className="w-24 py-2 bg-blue-600 rounded text-[10px] text-center font-bold">TARGET: NVDA</div>
            <div className="flex-1 h-[1px] bg-gray-700"></div>
        </div>
        
        <div className="pl-8 space-y-2">
            <div className="flex gap-4 items-center opacity-80">
                <div className="w-20 py-2 bg-gray-800 border border-blue-500/40 rounded text-[10px] text-center">TIER 1: TSM</div>
                <div className="flex-1 h-[1px] bg-gray-800"></div>
            </div>
            <div className="pl-8 opacity-60">
                <div className="w-20 py-2 bg-gray-800 border border-gray-700 rounded text-[10px] text-center italic">TIER 2: ASML</div>
            </div>
        </div>
      </div>
      
      <p className="mt-6 text-[8px] text-gray-600">Calculated via Neo4j Centrality (Eigenvector)</p>
    </div>
  );
};

export default SupplyTiers;
