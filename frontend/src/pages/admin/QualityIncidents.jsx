import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { ClipboardList, PlusCircle, AlertTriangle } from 'lucide-react';

const QualityIncidents = () => {
    const [incidents, setIncidents] = useState([]);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/validation/incidents');
            if (res.data.success) setIncidents(res.data.data);
        };
        load();
    }, []);

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <ClipboardList className="text-red-400" /> Quality Incident Log
                    </h1>
                    <p className="text-slate-500">Data Integrity Failures & Resolution Tracking</p>
                </div>
                <button className="bg-red-600 hover:bg-red-500 text-white px-4 py-2 rounded font-bold flex items-center gap-2">
                    <PlusCircle size={18} /> LOG INCIDENT
                </button>
            </header>

            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <table className="w-full text-left">
                    <thead className="text-slate-500 text-xs uppercase bg-slate-950">
                        <tr>
                            <th className="p-4">Dataset</th>
                            <th className="p-4">Issue</th>
                            <th className="p-4">Severity</th>
                            <th className="p-4">Status</th>
                            <th className="p-4">Reported</th>
                        </tr>
                    </thead>
                    <tbody className="text-sm">
                        {incidents.map(inc => (
                            <tr key={inc.id} className="border-b border-slate-800 hover:bg-slate-800/50">
                                <td className="p-4 font-bold text-white">{inc.dataset}</td>
                                <td className="p-4 text-slate-300">{inc.issue}</td>
                                <td className="p-4">
                                    <span className={`px-2 py-1 rounded text-xs font-bold ${
                                        inc.severity === 'HIGH' ? 'bg-red-500/20 text-red-500' : 
                                        inc.severity === 'MEDIUM' ? 'bg-orange-500/20 text-orange-400' : 
                                        'bg-blue-500/20 text-blue-400'
                                    }`}>
                                        {inc.severity}
                                    </span>
                                </td>
                                <td className="p-4">
                                    <span className={`px-2 py-1 rounded text-xs font-bold ${
                                        inc.status === 'RESOLVED' ? 'bg-green-500/20 text-green-400' : 'bg-slate-700 text-slate-300'
                                    }`}>
                                        {inc.status}
                                    </span>
                                </td>
                                <td className="p-4 text-slate-500">{new Date(inc.created).toLocaleString()}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="mt-8 bg-slate-900 border border-slate-800 rounded-xl p-6 flex gap-4 items-center">
                <AlertTriangle className="text-yellow-500" size={24} />
                <div className="text-sm text-slate-400">
                    <strong>Pro Tip:</strong> Link incidents to specific models in the Model Validator to automatically adjust trust scores.
                </div>
            </div>
        </div>
    );
};

export default QualityIncidents;
