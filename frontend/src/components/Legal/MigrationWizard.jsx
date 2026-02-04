import React from 'react';

const MigrationWizard = () => {
  const steps = ["ENTITY_LEGAL", "TAX_FILE_NV", "ASSET_TRANSFER", "CLOSURE_OLD_STATE"];
  
  return (
    <div className="p-8 bg-gray-900 border border-blue-500/20 rounded-2xl shadow-xl">
      <h2 className="text-2xl font-bold text-white mb-8">Redomicile Wizard: CA -> NV</h2>
      
      <div className="flex justify-between mb-12 relative">
        <div className="absolute top-1/2 left-0 w-full h-1 bg-gray-800 -translate-y-1/2"></div>
        {steps.map((s, i) => (
          <div key={s} className="relative z-10 flex flex-col items-center gap-2">
            <div className={`h-8 w-8 rounded-full border-2 flex items-center justify-center font-bold ${
              i === 0 ? 'bg-blue-600 border-blue-400' : 'bg-gray-800 border-gray-600 text-gray-500'
            }`}>
              {i + 1}
            </div>
            <span className="text-[10px] uppercase font-mono text-gray-400">{s.split('_')[0]}</span>
          </div>
        ))}
      </div>
      
      <div className="p-6 bg-gray-800/50 rounded-lg border border-gray-700">
        <h3 className="font-bold text-blue-400 mb-2">STEP 1: Articles of Organization (Nevada)</h3>
        <p className="text-gray-400 text-sm">Drafting legal documents... Estimated savings: $45,000/yr.</p>
        <button className="mt-6 w-full py-3 bg-blue-600 hover:bg-blue-700 rounded font-bold">START FILING</button>
      </div>
    </div>
  );
};

export default MigrationWizard;
