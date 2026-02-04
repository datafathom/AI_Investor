import React, { useState } from 'react';
import { Plus, X, Filter } from 'lucide-react';

const FilterBuilder = () => {
    const [filters, setFilters] = useState([
        { metric: 'Market Cap', op: '>', val: '10B' },
        { metric: 'P/E Ratio', op: '<', val: '25' },
    ]);

    const addFilter = () => {
        setFilters([...filters, { metric: 'Volume', op: '>', val: '1M' }]);
    };

    const removeFilter = (idx) => {
        setFilters(filters.filter((_, i) => i !== idx));
    };

    return (
        <div className="h-full flex flex-col">
            <h3 className="text-xs font-bold text-slate-500 uppercase mb-4 flex items-center gap-2">
                <Filter size={12} /> Scan Logic
            </h3>

            <div className="space-y-2 flex-1 overflow-y-auto">
                {filters.map((f, i) => (
                    <div key={i} className="flex items-center gap-2 bg-slate-800 p-2 rounded text-xs border border-slate-700">
                        <span className="font-bold text-indigo-400 bg-indigo-900/20 px-1 rounded">{f.metric}</span>
                        <span className="text-slate-400">{f.op}</span>
                        <span className="font-mono text-white bg-slate-900 px-1 rounded border border-slate-600 min-w-[40px] text-center">{f.val}</span>
                        <button onClick={() => removeFilter(i)} className="ml-auto text-slate-500 hover:text-red-400">
                            <X size={12} />
                        </button>
                    </div>
                ))}

                <button
                    onClick={addFilter}
                    className="w-full py-2 border-2 border-dashed border-slate-700 rounded text-slate-500 hover:text-white hover:border-slate-500 text-xs font-bold transition-all flex items-center justify-center gap-2"
                >
                    <Plus size={12} /> ADD CONDITION
                </button>
            </div>

            <button className="mt-4 w-full bg-indigo-600 hover:bg-indigo-500 py-2 rounded font-bold text-xs text-white transition-colors">
                Run Scan
            </button>
        </div>
    );
};

export default FilterBuilder;
