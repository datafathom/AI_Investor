import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Package, Plus } from 'lucide-react';

const AssetInventory = () => {
    const [assets, setAssets] = useState([]);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/assets/inventory');
            if (res.data.success) setAssets(res.data.data);
        };
        load();
    }, []);

    const addAsset = () => {
        alert("Add Asset Modal Placeholder");
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <Package className="text-blue-500" /> Asset Inventory
                    </h1>
                    <p className="text-slate-500">Alternative & Illiquid Asset Management</p>
                </div>
                <button onClick={addAsset} className="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded flex items-center gap-2">
                    <Plus size={18} /> Add Asset
                </button>
            </header>

            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <table className="w-full text-left">
                    <thead className="text-slate-500 text-xs uppercase bg-slate-950">
                        <tr>
                            <th className="p-4">Asset Name</th>
                            <th className="p-4">Type</th>
                            <th className="p-4">Valuation</th>
                            <th className="p-4">Acquired Date</th>
                            <th className="p-4">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="text-sm">
                        {assets.map((a, i) => (
                            <tr key={i} className="border-b border-slate-800 hover:bg-slate-800/50">
                                <td className="p-4 font-bold text-white">{a.name}</td>
                                <td className="p-4">
                                    <span className="bg-slate-800 text-slate-300 px-2 py-1 rounded text-xs uppercase">{a.type}</span>
                                </td>
                                <td className="p-4 font-mono font-bold text-emerald-400">${a.valuation.toLocaleString()}</td>
                                <td className="p-4 text-slate-400">{a.acquired}</td>
                                <td className="p-4">
                                    <button className="text-blue-400 hover:text-blue-300 text-xs font-bold">DETAILS</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default AssetInventory;
