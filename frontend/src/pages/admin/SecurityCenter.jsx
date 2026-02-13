import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { ShieldCheck, Activity, AlertOctagon, Key } from 'lucide-react';

const SecurityCenter = () => {
    const [status, setStatus] = useState(null);
    const [scanLoading, setScanLoading] = useState(false);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/security/posture');
            if (res.data.success) setStatus(res.data.data);
        };
        load();
    }, [scanLoading]);

    const runScan = async () => {
        setScanLoading(true);
        try {
            await apiClient.post('/security/scan');
            // Mock delay
            setTimeout(() => setScanLoading(false), 2000);
        } catch (e) { console.error(e); setScanLoading(false); }
    };

    if (!status) return <div>Loading Security Posture...</div>;

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <ShieldCheck className="text-emerald-500" /> Security Center
                    </h1>
                    <p className="text-slate-500">System Hardening & Vulnerability Management</p>
                </div>
                <button 
                    onClick={runScan}
                    disabled={scanLoading}
                    className="bg-emerald-600 hover:bg-emerald-500 text-white px-6 py-2 rounded font-bold flex items-center gap-2"
                >
                    {scanLoading ? 'SCANNING...' : 'RUN SECURITY SCAN'}
                </button>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 relative overflow-hidden">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Security Score</div>
                    <div className="text-5xl font-bold text-emerald-400">{status.score}</div>
                    <div className="absolute right-0 top-0 p-4 opacity-10">
                        <ShieldCheck size={80} />
                    </div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Vulnerabilities</div>
                    <div className="text-3xl font-bold text-orange-400">{status.vulnerabilities}</div>
                    <div className="text-xs text-orange-500/80 mt-1">Open Issues</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">MFA Adoption</div>
                    <div className="text-3xl font-bold text-blue-400">{status.mfa_adoption}%</div>
                    <div className="text-xs text-slate-500 mt-1">User Coverage</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">System Status</div>
                    <div className="text-lg font-bold text-green-400">{status.system_status}</div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                        <AlertOctagon className="text-red-500" /> Critical Recommendations
                    </h3>
                    <div className="space-y-4">
                        <div className="p-4 bg-slate-950 rounded border border-slate-800 flex justify-between items-center">
                            <div>
                                <div className="font-bold text-white">Rotate API Keys</div>
                                <div className="text-xs text-slate-500">Trading Bot A key is {'>'} 90 days old.</div>
                            </div>
                            <button className="text-xs bg-slate-800 hover:bg-slate-700 text-white px-3 py-1 rounded">Fix</button>
                        </div>
                        <div className="p-4 bg-slate-950 rounded border border-slate-800 flex justify-between items-center">
                            <div>
                                <div className="font-bold text-white">Enable IP Whitelist</div>
                                <div className="text-xs text-slate-500">Restrict admin access to VPN only.</div>
                            </div>
                            <button className="text-xs bg-slate-800 hover:bg-slate-700 text-white px-3 py-1 rounded">Fix</button>
                        </div>
                    </div>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                        <Activity className="text-blue-500" /> Recent Activity
                    </h3>
                    <div className="space-y-3 text-sm">
                        <div className="flex justify-between items-center text-slate-400">
                            <span>User Login (Admin)</span>
                            <span className="text-xs">2 mins ago</span>
                        </div>
                        <div className="flex justify-between items-center text-slate-400">
                            <span>Key Revocation</span>
                            <span className="text-xs">1 hour ago</span>
                        </div>
                        <div className="flex justify-between items-center text-slate-400">
                            <span>Failed Login Attempt</span>
                            <span className="text-xs text-red-400">3 hours ago</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SecurityCenter;
