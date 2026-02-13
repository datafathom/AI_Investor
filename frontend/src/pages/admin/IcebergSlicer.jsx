import React, { useState } from 'react';
import apiClient from '../../services/apiClient';
import { Layers, EyeOff } from 'lucide-react';

const IcebergSlicer = () => {
    const [formData, setFormData] = useState({ symbol: '', total: '', visible: '' });

    const submit = async (e) => {
        e.preventDefault();
        await apiClient.post('/orders/iceberg', null, { 
            params: { symbol: formData.symbol, total_qty: formData.total, visible_qty: formData.visible } 
        });
        alert("Iceberg Order Live");
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Layers className="text-blue-300" /> Iceberg Slicer
                </h1>
                <p className="text-slate-500">Large Order fragmentation & Hidden Size</p>
            </header>

            <div className="max-w-xl mx-auto bg-slate-900 border border-slate-800 rounded-xl p-8">
                <div className="flex justify-center mb-6">
                    <div className="bg-blue-900/20 p-4 rounded-full">
                        <EyeOff size={48} className="text-blue-400" />
                    </div>
                </div>
                
                <form onSubmit={submit} className="space-y-6">
                    <div>
                        <label className="block text-xs uppercase text-slate-500 mb-1">Symbol</label>
                        <input 
                            className="w-full bg-slate-950 border border-slate-700 rounded p-3 text-white text-lg font-bold uppercase outline-none"
                            placeholder="AAPL"
                            value={formData.symbol}
                            onChange={e => setFormData({...formData, symbol: e.target.value.toUpperCase()})}
                        />
                    </div>
                    
                    <div className="grid grid-cols-2 gap-6">
                        <div>
                            <label className="block text-xs uppercase text-slate-500 mb-1">Total Quantity</label>
                            <input 
                                type="number"
                                className="w-full bg-slate-950 border border-slate-700 rounded p-3 text-white outline-none"
                                placeholder="10000"
                                value={formData.total}
                                onChange={e => setFormData({...formData, total: e.target.value})}
                            />
                        </div>
                        <div>
                            <label className="block text-xs uppercase text-slate-500 mb-1">Visible Tip</label>
                            <input 
                                type="number"
                                className="w-full bg-slate-950 border border-slate-700 rounded p-3 text-white outline-none"
                                placeholder="100"
                                value={formData.visible}
                                onChange={e => setFormData({...formData, visible: e.target.value})}
                            />
                        </div>
                    </div>

                    <div className="p-4 bg-slate-950 rounded border border-slate-800">
                        <div className="text-xs uppercase text-slate-500 mb-2 font-bold">Projected Slices</div>
                        <div className="text-2xl font-mono text-white">
                            {formData.total && formData.visible ? Math.ceil(formData.total / formData.visible) : 0} <span className="text-sm text-slate-500">Child Orders</span>
                        </div>
                    </div>

                    <button className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 rounded text-lg">
                        LAUNCH ICEBERG
                    </button>
                </form>
            </div>
        </div>
    );
};

export default IcebergSlicer;
