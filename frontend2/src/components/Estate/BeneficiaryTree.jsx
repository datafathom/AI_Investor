import React from 'react';

const BeneficiaryTree = () => {
  return (
    <div className="p-6 bg-gray-900 min-h-[400px] border border-dashed border-gray-700 rounded-2xl">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-white">Beneficiary Allocation</h2>
        <p className="text-gray-500 text-sm">Drag and drop to shard your legacy</p>
      </div>
      
      <div className="flex flex-col items-center gap-12">
        <div className="w-32 py-4 bg-blue-600 rounded-lg font-bold text-center">PRIMARY WARDEN</div>
        
        <div className="flex gap-16">
            <div className="group relative">
                <div className="w-24 py-3 bg-gray-800 border-2 border-green-500/50 rounded-lg text-center text-xs">SPOUSE (50%)</div>
            </div>
            <div className="group relative">
                <div className="w-24 py-3 bg-gray-800 border-2 border-blue-500/50 rounded-lg text-center text-xs">KIDS (50%)</div>
            </div>
        </div>
      </div>
    </div>
  );
};

export default BeneficiaryTree;
