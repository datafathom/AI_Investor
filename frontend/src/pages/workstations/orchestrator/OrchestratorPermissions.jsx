import React from 'react';
import '../Workstation.css';

const OrchestratorPermissions = () => {
    // Mock Permissions Matrix
    const PERMISSIONS_MATRIX = [
        { role: 'Admin',        canEdit: true,  canDelete: true,  canDeploy: true,  maxBudget: 'Unlimited' },
        { role: 'Strategist',   canEdit: true,  canDelete: false, canDeploy: true,  maxBudget: '$5M' },
        { role: 'Analyst',      canEdit: true,  canDelete: false, canDeploy: false, maxBudget: '$100k' },
        { role: 'Auditor',      canEdit: false, canDelete: false, canDeploy: false, maxBudget: 'None' },
        { role: 'Trader',       canEdit: false, canDelete: false, canDeploy: true,  maxBudget: '$1M' },
    ];

    return (
        <div className="workstation-container">
            <header className="workstation-header">
                <div className="status-dot pulse"></div>
                <h1>Role Permissions <span className="text-slate-500">//</span> WORKSTATION</h1>
                <div className="flex-1"></div>
                <div className="security-badge">SECURE_CHANNEL_v1.2</div>
            </header>

            <div className="workstation-grid">
                <div className="workstation-main bg-slate-900/50 border border-slate-800 rounded-lg p-6">
                    <div className="flex justify-between items-center mb-6">
                        <div>
                            <h2 className="text-cyan-400 font-mono text-xs uppercase tracking-widest mb-1">Functional Module: Role Permissions</h2>
                            <p className="text-slate-400 font-mono text-sm">Defining action boundaries for system personas.</p>
                        </div>
                        <button className="px-4 py-2 bg-cyan-900/30 border border-cyan-500/30 text-cyan-400 text-xs font-mono rounded hover:bg-cyan-900/50 transition-colors">
                            SYNC GRAPH PERMISSIONS
                        </button>
                    </div>
                    
                    <div className="overflow-x-auto">
                        <table className="w-full text-left border-collapse">
                            <thead>
                                <tr className="border-b border-slate-700">
                                    <th className="p-3 text-slate-400 font-mono text-xs uppercase">Role</th>
                                    <th className="p-3 text-slate-400 font-mono text-xs uppercase text-center">Write Access</th>
                                    <th className="p-3 text-slate-400 font-mono text-xs uppercase text-center">Delete Access</th>
                                    <th className="p-3 text-slate-400 font-mono text-xs uppercase text-center">Deploy</th>
                                    <th className="p-3 text-slate-400 font-mono text-xs uppercase text-right">Max Budget</th>
                                </tr>
                            </thead>
                            <tbody>
                                {PERMISSIONS_MATRIX.map((perm, idx) => (
                                    <tr key={idx} className="border-b border-slate-800/50 hover:bg-slate-800/30 transition-colors">
                                        <td className="p-3 font-mono text-sm text-cyan-300">{perm.role}</td>
                                        <td className="p-3 text-center">
                                            <span className={`inline-block w-2 h-2 rounded-full ${perm.canEdit ? 'bg-green-500 shadow-[0_0_5px_rgba(34,197,94,0.5)]' : 'bg-red-900/50'}`}></span>
                                        </td>
                                        <td className="p-3 text-center">
                                            <span className={`inline-block w-2 h-2 rounded-full ${perm.canDelete ? 'bg-green-500 shadow-[0_0_5px_rgba(34,197,94,0.5)]' : 'bg-red-900/50'}`}></span>
                                        </td>
                                        <td className="p-3 text-center">
                                            <span className={`inline-block w-2 h-2 rounded-full ${perm.canDeploy ? 'bg-green-500 shadow-[0_0_5px_rgba(34,197,94,0.5)]' : 'bg-red-900/50'}`}></span>
                                        </td>
                                        <td className="p-3 text-right font-mono text-sm text-slate-300">{perm.maxBudget}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>

                <div className="workstation-sidebar flex flex-col gap-4">
                    <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
                        <h3 className="text-slate-500 font-mono text-[10px] uppercase mb-4">Security Audit Log</h3>
                        <div className="space-y-3 font-mono text-[10px]">
                            <div className="flex justify-between items-start border-l-2 border-green-500 pl-2">
                                <span className="text-slate-400">ADMIN changed policy P-992</span>
                                <span className="text-slate-600">10:42AM</span>
                            </div>
                            <div className="flex justify-between items-start border-l-2 border-red-500 pl-2">
                                <span className="text-slate-400">TRADER denied excess leverage</span>
                                <span className="text-slate-600">09:15AM</span>
                            </div>
                            <div className="flex justify-between items-start border-l-2 border-cyan-500 pl-2">
                                <span className="text-slate-400">Analyst deployment sync</span>
                                <span className="text-slate-600">08:30AM</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default OrchestratorPermissions;
