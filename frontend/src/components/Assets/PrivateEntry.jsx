import React from 'react';

const PrivateEntry = () => {
  return (
    <div className="p-6 bg-gray-900 rounded-lg border border-gray-700">
      <h2 className="text-xl font-bold mb-4">Manual Asset Induction</h2>
      <div className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
            <div>
                <label className="text-xs text-gray-500 uppercase">Asset Name</label>
                <input type="text" className="w-full bg-gray-800 p-2 rounded" placeholder="e.g. Stripe Series B" />
            </div>
            <div>
                <label className="text-xs text-gray-500 uppercase">Category</label>
                <select className="w-full bg-gray-800 p-2 rounded">
                    <option>Private Equity</option>
                    <option>Real Estate</option>
                    <option>Alternative</option>
                </select>
            </div>
        </div>
        <div className="p-4 bg-blue-900/10 border border-blue-500/20 rounded">
            <h4 className="text-xs font-bold text-blue-400 mb-2">COMMITMENT TRACKING</h4>
            <div className="flex gap-4">
                <input type="number" className="flex-1 bg-gray-800 p-2 rounded text-xs" placeholder="Total Committed ($)" />
                <input type="number" className="flex-1 bg-gray-800 p-2 rounded text-xs" placeholder="Initial Call ($)" />
            </div>
        </div>
        <button className="w-full py-3 bg-green-600 rounded font-bold">ADD TO BOOK OF RECORD</button>
      </div>
    </div>
  );
};

export default PrivateEntry;
