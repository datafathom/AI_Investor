import React from 'react';

const FXOrder = () => {
  return (
    <div className="p-6 bg-gray-900 rounded-lg">
      <h2 className="text-xl font-bold mb-4">Iceberg FX Order</h2>
      <div className="space-y-4">
        <div>
          <label className="block text-xs text-gray-400">Conversion Pair</label>
          <select className="w-full bg-gray-800 p-2 rounded">
            <option>USD / JPY</option>
            <option>USD / EUR</option>
          </select>
        </div>
        <div>
          <label className="block text-xs text-gray-400">Total Amount</label>
          <input type="number" className="w-full bg-gray-800 p-2 rounded" placeholder="1,000,000" />
        </div>
        <div className="p-3 bg-blue-900/20 border border-blue-500/30 rounded">
          <div className="text-xs font-bold text-blue-400">ICEBERG MODE ACTIVE</div>
          <div className="text-gray-400 text-[10px]">Orders will be chopped into 50,000 lots to minimize slippage.</div>
        </div>
        <button className="w-full bg-green-600 hover:bg-green-700 p-3 rounded font-bold">EXECUTE CONVERSION</button>
      </div>
    </div>
  );
};

export default FXOrder;
