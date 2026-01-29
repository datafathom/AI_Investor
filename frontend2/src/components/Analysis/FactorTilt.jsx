import React from 'react';

const FactorTilt = () => {
  const factors = [
    { name: 'Beta', val: 1.15, status: 'HIGH' },
    { name: 'Size (SMB)', val: 0.45, status: 'MED' },
    { name: 'Value (HML)', val: -0.12, status: 'LOW' },
    { name: 'Quality (RMW)', val: 0.35, status: 'MED' },
  ];

  return (
    <div className="p-4 bg-gray-900 rounded-lg">
      <h3 className="text-blue-400 font-bold text-xs uppercase mb-4 tracking-tighter">Systematic Factor Tilt</h3>
      <div className="grid grid-cols-2 gap-4">
        {factors.map(f => (
            <div key={f.name} className="p-3 bg-black/40 rounded border border-gray-800">
                <div className="text-[10px] text-gray-500">{f.name}</div>
                <div className="text-lg font-mono text-white">{f.val > 0 ? '+' : ''}{f.val}</div>
            </div>
        ))}
      </div>
    </div>
  );
};

export default FactorTilt;
