import React from 'react';

const ImpactDash = () => {
  return (
    <div className="p-6 bg-gray-900 rounded-xl border border-green-500/20">
      <h2 className="text-xl font-bold text-white mb-6">Social Impact Dashboard (DAF)</h2>
      
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="p-4 bg-gray-800 rounded">
            <span className="text-xs text-gray-500">GRANTS DISTRIBUTED</span>
            <div className="text-2xl font-bold text-green-400">$12,500</div>
        </div>
        <div className="p-4 bg-gray-800 rounded">
            <span className="text-xs text-gray-500">TAX BURDEN WIPED</span>
            <div className="text-2xl font-bold text-blue-400">$8,200</div>
        </div>
      </div>
      
      <div className="space-y-3">
        <h4 className="text-[10px] font-bold text-gray-600 uppercase">Top Beneficiaries</h4>
        <div className="flex justify-between text-sm bg-black/30 p-2 rounded">
            <span>St. Judes Children</span>
            <span className="font-bold text-white">$5,000</span>
        </div>
        <div className="flex justify-between text-sm bg-black/30 p-2 rounded">
            <span>Feeding America</span>
            <span className="font-bold text-white">$2,500</span>
        </div>
      </div>
    </div>
  );
};

export default ImpactDash;
