import React from 'react';

const VCGrid = () => {
  const startups = [
    { name: 'Neuralink', vintage: '2021', status: 'LATE_STAGE', moic: '8.4x' },
    { name: 'Helix', vintage: '2023', status: 'SEED', moic: '1.0x' },
    { name: 'Standard', vintage: '2022', status: 'SERIES_A', moic: '2.5x' },
  ];

  return (
    <div className="p-4 bg-gray-900 rounded-lg overflow-x-auto">
      <table className="w-full text-left">
        <thead>
          <tr className="text-[10px] text-gray-500 border-b border-gray-800">
            <th className="pb-2">STARTUP ENTITY</th>
            <th className="pb-2">VINTAGE</th>
            <th className="pb-2">ROUND</th>
            <th className="pb-2">MOIC</th>
          </tr>
        </thead>
        <tbody className="text-sm font-mono">
          {startups.map(s => (
            <tr key={s.name} className="border-b border-gray-800/50">
              <td className="py-3 font-bold text-blue-400">{s.name}</td>
              <td className="py-3 text-gray-400">{s.vintage}</td>
              <td className="py-3 text-gray-300">{s.status}</td>
              <td className="py-3 text-green-400 font-bold">{s.moic}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default VCGrid;
