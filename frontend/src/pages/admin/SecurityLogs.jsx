import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { List, Filter } from 'lucide-react';

const SecurityLogs = () => {
    const [logs, setLogs] = useState([]);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/security/audit-logs');
            if (res.data.success) setLogs(res.data.data);
        };
        load();
    }, []);

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <List className="text-slate-400" /> Security Audit Logs
                    </h1>
                    <p className="text-slate-500">Immutable Record of System Actions</p>
                </div>
                <button className="bg-slate-800 hover:bg-slate-700 text-white px-4 py-2 rounded flex items-center gap-2 text-sm">
                    <Filter size={16} /> FILTER
                </button>
            </header>

            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <table className="w-full text-left">
                    <thead className="text-slate-500 text-xs uppercase bg-slate-950">
                        <tr>
                            <th className="p-4">Timestamp</th>
                            <th className="p-4">Action</th>
                            <th className="p-4">User</th>
                            <th className="p-4">IP Address</th>
                            <th className="p-4">Severity</th>
                        </tr>
                    </thead>
                    <tbody className="text-sm">
                        {logs.map(log => (
                            <tr key={log.id} className="border-b border-slate-800 hover:bg-slate-800/50 font-mono">
                                <td className="p-4 text-slate-400">{new Date(log.timestamp).toLocaleString()}</td>
                                <td className="p-4 font-bold text-white">{log.action}</td>
                                <td className="p-4 text-cyan-400">{log.user}</td>
                                <td className="p-4 text-slate-500">{log.ip}</td>
                                <td className="p-4">
                                    <span className={`px-2 py-1 rounded text-xs font-bold ${
                                        log.severity === 'CRITICAL' ? 'bg-red-500/20 text-red-500' :
                                        log.severity === 'WARN' ? 'bg-yellow-500/20 text-yellow-500' :
                                        'bg-blue-500/20 text-blue-400'
                                    }`}>
                                        {log.severity}
                                    </span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default SecurityLogs;
