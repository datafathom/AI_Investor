import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Link2, Trash2, Plus, ShieldCheck, AlertCircle } from 'lucide-react';

const BrokerConnectionManager = () => {
    const [connections, setConnections] = useState([]);
    const [showAdd, setShowAdd] = useState(false);
    const [newConn, setNewConn] = useState({ api_key: '', secret_key: '' });

    useEffect(() => {
        loadConnections();
    }, []);

    const loadConnections = async () => {
        try {
            const res = await apiClient.get('/brokerage/connections');
            if (res.data.success) setConnections(res.data.data);
        } catch (e) {
            console.error(e);
        }
    };

    const handleConnect = async () => {
        try {
            await apiClient.post('/brokerage/connections', newConn);
            setShowAdd(false);
            loadConnections();
        } catch (e) { console.error(e); }
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <Link2 className="text-blue-500" /> Broker Connections
                    </h1>
                    <p className="text-slate-500">Manage API Integrations & OAuth Sessions</p>
                </div>
                <button 
                    onClick={() => setShowAdd(!showAdd)}
                    className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-2 rounded font-bold transition-colors flex items-center gap-2"
                >
                    <Plus size={18} /> ADD CONNECTION
                </button>
            </header>

            {showAdd && (
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-8 animate-fade-in">
                    <h3 className="text-white font-bold mb-4">New Connection</h3>
                    <div className="grid grid-cols-2 gap-4 mb-4">
                        <input 
                            placeholder="API Key"
                            value={newConn.api_key}
                            onChange={e => setNewConn({...newConn, api_key: e.target.value})}
                            className="bg-slate-950 border border-slate-700 rounded p-2 text-white"
                        />
                        <input 
                            type="password"
                            placeholder="Secret Key"
                            value={newConn.secret_key}
                            onChange={e => setNewConn({...newConn, secret_key: e.target.value})}
                            className="bg-slate-950 border border-slate-700 rounded p-2 text-white"
                        />
                    </div>
                    <button onClick={handleConnect} className="bg-green-600 text-white px-4 py-2 rounded font-bold">
                        CONNECT
                    </button>
                </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {connections.map(conn => (
                    <div key={conn.id} className="bg-slate-900 border border-slate-800 rounded-xl p-6 relative group">
                        <div className="flex justify-between items-start mb-4">
                            <div className="font-bold text-xl text-white">{conn.broker}</div>
                            <div className={`px-2 py-1 rounded text-xs font-bold ${
                                conn.status === 'CONNECTED' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                            }`}>
                                {conn.status}
                            </div>
                        </div>
                        <div className="text-sm text-slate-500 mb-2">ID: <span className="font-mono text-slate-300">{conn.id}</span></div>
                        <div className="text-sm text-slate-500 mb-4 flex items-center gap-2">
                             Last Sync: <span className="text-slate-300">{conn.last_sync}</span>
                        </div>
                        
                        <div className="flex gap-2 mt-4 pt-4 border-t border-slate-800">
                             <button className="flex-1 bg-slate-800 hover:bg-slate-700 text-white py-2 rounded font-bold text-xs">
                                REFRESH TOKEN
                             </button>
                             <button className="bg-red-900/20 hover:bg-red-900/40 text-red-400 p-2 rounded border border-red-900/30">
                                <Trash2 size={16} />
                             </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default BrokerConnectionManager;
