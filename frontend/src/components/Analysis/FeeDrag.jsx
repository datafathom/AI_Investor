import React from 'react';

const FeeDrag = () => {
  return (
    <div className="p-4 bg-gray-900 rounded-lg">
      <h3 className="text-white font-bold mb-4 italic">Compounding alpha via fee elimination</h3>
      <div className="space-y-6">
        <div>
            <div className="flex justify-between text-[10px] mb-1">
                <span className="text-red-400">Institutional Fund (2/20 Fee)</span>
                <span className="text-white">$452k</span>
            </div>
            <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                <div className="h-full bg-red-500 w-1/2"></div>
            </div>
        </div>

        <div>
            <div className="flex justify-between text-[10px] mb-1">
                <span className="text-green-400">Factor Clone (0.05% Expense)</span>
                <span className="text-white">$1.2M</span>
            </div>
            <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                <div className="h-full bg-green-500 w-full"></div>
            </div>
        </div>
      </div>
      <p className="mt-4 text-[8px] text-gray-600 uppercase text-center">20 Year compounding projection at 10% gross return</p>
    </div>
  );
};

export default FeeDrag;
