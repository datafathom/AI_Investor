import React from 'react';

const CarryHeat = () => {
  const currencies = [
    { name: 'MXN', yield: '11.2%', heat: 'HOT' },
    { name: 'BRL', yield: '10.5%', heat: 'HOT' },
    { name: 'CHF', yield: '1.7%', heat: 'COLD' },
    { name: 'JPY', yield: '-0.1%', heat: 'FROZEN' },
  ];

  return (
    <div className="p-4 bg-gray-900 rounded-xl border border-orange-500/20">
      <h3 className="text-orange-400 font-bold text-xs uppercase mb-3">Carry Trade Heatmap</h3>
      <div className="grid grid-cols-2 gap-2">
        {currencies.map(c => (
          <div key={c.name} className={`p-2 rounded text-center border ${
            c.heat === 'HOT' ? 'border-red-500/50 bg-red-900/10' : 'border-blue-500/50 bg-blue-900/10'
          }`}>
            <div className="text-lg font-bold">{c.name}</div>
            <div className="text-xs">{c.yield}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CarryHeat;
