import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Smartphone, Monitor, Globe, Trash2, LogOut } from 'lucide-react';

const SessionManager = () => {
    const [sessions, setSessions] = useState([]);

    useEffect(() => {
        loadSessions();
    }, []);

    const loadSessions = async () => {
        const res = await apiClient.get('/auth/sessions');
        if (res.data.success) setSessions(res.data.data);
    };

    const killSession = async (id) => {
        await apiClient.delete(`/auth/sessions/${id}`);
        loadSessions();
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <Globe className="text-blue-400" /> Session Manager
                    </h1>
                    <p className="text-slate-500">Active Devices & Logins</p>
                </div>
                <button className="bg-red-600 hover:bg-red-500 text-white px-4 py-2 rounded font-bold flex items-center gap-2 text-sm">
                    <LogOut size={16} /> LOGOUT ALL DEVICES
                </button>
            </header>

            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <table className="w-full text-left">
                    <thead className="text-slate-500 text-xs uppercase bg-slate-950">
                        <tr>
                            <th className="p-4">Device</th>
                            <th className="p-4">Location</th>
                            <th className="p-4">IP Address</th>
                            <th className="p-4">Status</th>
                            <th className="p-4">Expires</th>
                            <th className="p-4">Action</th>
                        </tr>
                    </thead>
                    <tbody className="text-sm">
                        {sessions.map(s => (
                            <tr key={s.id} className={`border-b border-slate-800 ${s.current ? 'bg-blue-900/10' : ''}`}>
                                <td className="p-4 flex items-center gap-3 font-bold text-white">
                                    {s.device.includes('Mobile') ? <Smartphone size={18} className="text-slate-400" /> : <Monitor size={18} className="text-slate-400" />}
                                    {s.device}
                                </td>
                                <td className="p-4 text-slate-300">{s.location}</td>
                                <td className="p-4 font-mono text-slate-400">{s.ip}</td>
                                <td className="p-4">
                                    {s.current ? (
                                        <span className="text-xs bg-green-500/20 text-green-400 px-2 py-1 rounded font-bold">CURRENT</span>
                                    ) : (
                                        <span className="text-xs bg-slate-700 text-slate-300 px-2 py-1 rounded">ACTIVE</span>
                                    )}
                                </td>
                                <td className="p-4 text-slate-400">{s.expires}</td>
                                <td className="p-4">
                                    {!s.current && (
                                        <button 
                                            onClick={() => killSession(s.id)}
                                            className="text-slate-500 hover:text-red-400 transition-colors"
                                            title="Revoke Session"
                                        >
                                            <Trash2 size={18} />
                                        </button>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default SessionManager;
