import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { FileText, Upload, Calendar } from 'lucide-react';

const FilingManager = () => {
    const [filings, setFilings] = useState([]);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/legal/filings');
            if (res.data.success) setFilings(res.data.data);
        };
        load();
    }, []);

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <FileText className="text-blue-400" /> Regulatory Filing Manager
                    </h1>
                    <p className="text-slate-500">SEC/CFTC Submission Tracking</p>
                </div>
                <button className="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded font-bold flex items-center gap-2">
                    <Upload size={18} /> UPLOAD
                </button>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                    <table className="w-full text-left">
                        <thead className="text-slate-500 text-xs uppercase bg-slate-950">
                            <tr>
                                <th className="p-4">Form Type</th>
                                <th className="p-4">Period</th>
                                <th className="p-4">Status</th>
                                <th className="p-4">Submitted</th>
                            </tr>
                        </thead>
                        <tbody className="text-sm">
                            {filings.map(f => (
                                <tr key={f.id} className="border-b border-slate-800 hover:bg-slate-800/50">
                                    <td className="p-4 font-bold text-white">{f.type}</td>
                                    <td className="p-4 text-slate-300">{f.period}</td>
                                    <td className="p-4">
                                        <span className={`px-2 py-1 rounded text-xs font-bold ${
                                            f.status === 'FILED' ? 'bg-green-500/20 text-green-400' : 'bg-slate-700 text-slate-300'
                                        }`}>
                                            {f.status}
                                        </span>
                                    </td>
                                    <td className="p-4 text-slate-400">{f.submission_date || '-'}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                        <Calendar size={18} className="text-purple-400" /> Compliance Calendar
                    </h3>
                    <div className="space-y-3 text-sm">
                        <div className="flex justify-between items-center p-2 rounded hover:bg-slate-800">
                            <span className="text-slate-300">Form 13F (Q4)</span>
                            <span className="text-red-400 font-bold">Feb 15</span>
                        </div>
                        <div className="flex justify-between items-center p-2 rounded hover:bg-slate-800">
                            <span className="text-slate-300">Form ADV Update</span>
                            <span className="text-slate-500">Mar 31</span>
                        </div>
                        <div className="flex justify-between items-center p-2 rounded hover:bg-slate-800">
                            <span className="text-slate-300">Tax Filings</span>
                            <span className="text-slate-500">Apr 15</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default FilingManager;
