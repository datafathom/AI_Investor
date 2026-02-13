import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Share2, Lock, History } from 'lucide-react';

const InvestorPortal = () => {
    const [link, setLink] = useState(null);
    const [logs, setLogs] = useState([]);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/reporting/access-logs');
            if (res.data.success) setLogs(res.data.data);
        };
        load();
    }, []);

    const createLink = async () => {
        const res = await apiClient.post('/reporting/share', null, { params: { expiry_hours: 24, password: true } });
        if (res.data.success) setLink(res.data.data);
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Share2 className="text-cyan-500" /> Investor Portal & Sharing
                </h1>
                <p className="text-slate-500">Secure Access Management & Audit Logs</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-6">Create Secure Link</h3>
                    <div className="space-y-4">
                        <button 
                            onClick={createLink}
                            className="w-full bg-cyan-600 hover:bg-cyan-500 text-white font-bold py-3 rounded flex justify-center items-center gap-2"
                        >
                            <Lock size={18} /> GENERATE 24H LINK
                        </button>
                        
                        {link && (
                            <div className="p-4 bg-emerald-900/20 border border-emerald-900/50 rounded mt-4">
                                <div className="text-xs uppercase text-emerald-400 font-bold mb-1">Active Link</div>
                                <div className="text-white bg-slate-950 p-2 rounded text-sm font-mono break-all">{link.link}</div>
                                <div className="text-xs text-slate-500 mt-2">Expires in: {link.expiry}</div>
                            </div>
                        )}
                        
                        <div className="pt-4 border-t border-slate-800">
                            <label className="flex items-center gap-2 text-slate-400 text-sm cursor-pointer">
                                <input type="checkbox" className="rounded bg-slate-950 border-slate-700" defaultChecked />
                                Require Password Protection
                            </label>
                            <label className="flex items-center gap-2 text-slate-400 text-sm cursor-pointer mt-2">
                                <input type="checkbox" className="rounded bg-slate-950 border-slate-700" defaultChecked />
                                Hide Tax Sensitive Data
                            </label>
                        </div>
                    </div>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                        <History size={18} className="text-slate-400" /> Access Logs
                    </h3>
                    <div className="space-y-3">
                        {logs.map((l, i) => (
                            <div key={i} className="text-sm p-3 bg-slate-950 rounded border border-slate-800">
                                <div className="flex justify-between font-bold text-white">
                                    <span>{l.viewer}</span>
                                    <span className="text-slate-500 font-normal">{l.time}</span>
                                </div>
                                <div className="text-slate-400 mt-1">Viewed: {l.report}</div>
                                <div className="text-xs text-slate-600 mt-1">IP: {l.ip}</div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default InvestorPortal;
