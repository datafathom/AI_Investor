import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Key, Plus, Trash2, Copy } from 'lucide-react';

const ApiKeyManager = () => {
    const [keys, setKeys] = useState([]);
    const [newKey, setNewKey] = useState(null);

    useEffect(() => {
        loadKeys();
    }, []);

    const loadKeys = async () => {
        const res = await apiClient.get('/auth/api-keys');
        if (res.data.success) setKeys(res.data.data);
    };

    const createKey = async () => {
        const name = prompt("Enter key name (e.g., Trading Bot):");
        if (!name) return;
        
        const res = await apiClient.post('/auth/api-keys', { name, scopes: ['trade:read', 'trade:write'] });
        if (res.data.success) {
            setNewKey(res.data.data);
            loadKeys();
        }
    };

    const revokeKey = async (id) => {
        if (!confirm("Are you sure? This action cannot be undone.")) return;
        await apiClient.delete(`/auth/api-keys/${id}`);
        loadKeys();
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <Key className="text-yellow-500" /> API Key Manager
                    </h1>
                    <p className="text-slate-500">Programmatic Access Control</p>
                </div>
                <button 
                    onClick={createKey}
                    className="bg-yellow-600 hover:bg-yellow-500 text-black px-4 py-2 rounded font-bold flex items-center gap-2"
                >
                    <Plus size={18} /> CREATE KEY
                </button>
            </header>

            {newKey && (
                <div className="mb-8 bg-green-900/20 border border-green-900/50 p-6 rounded-xl">
                    <h3 className="text-green-400 font-bold mb-2">New API Key Created</h3>
                    <p className="text-sm text-slate-400 mb-4">
                        Please copy this key immediately. It will not be shown again.
                    </p>
                    <div className="flex gap-2">
                        <input 
                            readOnly 
                            value={newKey.key} 
                            className="bg-black/50 border border-green-900/50 rounded p-3 text-green-300 font-mono text-lg flex-1"
                        />
                        <button className="bg-green-700 hover:bg-green-600 text-white px-4 rounded">
                            <Copy size={20} />
                        </button>
                    </div>
                </div>
            )}

            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <table className="w-full text-left">
                    <thead className="text-slate-500 text-xs uppercase bg-slate-950">
                        <tr>
                            <th className="p-4">Name</th>
                            <th className="p-4">Key Prefix</th>
                            <th className="p-4">Created</th>
                            <th className="p-4">Last Used</th>
                            <th className="p-4">Action</th>
                        </tr>
                    </thead>
                    <tbody className="text-sm">
                        {keys.map(k => (
                            <tr key={k.id} className="border-b border-slate-800 hover:bg-slate-800/50">
                                <td className="p-4 font-bold text-white">{k.name}</td>
                                <td className="p-4 font-mono text-slate-400">{k.prefix}</td>
                                <td className="p-4 text-slate-500">{k.created}</td>
                                <td className="p-4 text-slate-300">{k.last_used}</td>
                                <td className="p-4">
                                    <button 
                                        onClick={() => revokeKey(k.id)}
                                        className="text-slate-500 hover:text-red-400 transition-colors"
                                        title="Revoke Key"
                                    >
                                        <Trash2 size={18} />
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default ApiKeyManager;
