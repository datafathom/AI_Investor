import React, { useState } from 'react';
import { X, Download, Calendar } from 'lucide-react';
import apiClient from '../../services/apiClient';

const AuditExporterModal = ({ isOpen, onClose }) => {
    const [dates, setDates] = useState({ start: '', end: '' });
    const [loading, setLoading] = useState(false);

    if (!isOpen) return null;

    const handleExport = async () => {
        setLoading(true);
        try {
            await apiClient.post('/compliance/audit/export', null, { params: dates });
            onClose();
        } catch (e) { console.error(e); }
        finally { setLoading(false); }
    };

    return (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50">
            <div className="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-md p-6">
                <div className="flex justify-between items-center mb-6">
                    <h3 className="text-xl font-bold text-white flex items-center gap-2">
                        <Download size={20} className="text-emerald-500" /> Export Audit Trail
                    </h3>
                    <button onClick={onClose} className="text-slate-500 hover:text-white"><X size={20} /></button>
                </div>

                <div className="space-y-4 mb-6">
                    <div>
                        <label className="block text-xs uppercase text-slate-500 mb-2">Start Date</label>
                        <div className="flex items-center bg-slate-950 border border-slate-700 rounded p-2">
                            <Calendar size={16} className="text-slate-400 mr-2" />
                            <input 
                                type="date" 
                                className="bg-transparent text-white w-full outline-none"
                                value={dates.start}
                                onChange={e => setDates({...dates, start: e.target.value})}
                            />
                        </div>
                    </div>
                    <div>
                        <label className="block text-xs uppercase text-slate-500 mb-2">End Date</label>
                        <div className="flex items-center bg-slate-950 border border-slate-700 rounded p-2">
                            <Calendar size={16} className="text-slate-400 mr-2" />
                            <input 
                                type="date" 
                                className="bg-transparent text-white w-full outline-none"
                                value={dates.end}
                                onChange={e => setDates({...dates, end: e.target.value})}
                            />
                        </div>
                    </div>
                    <div className="p-3 bg-blue-900/20 border border-blue-900/50 rounded text-sm text-blue-200">
                        Export will include all order logs, execution records, and system modification events for the selected period in SEC-compliant CSV format.
                    </div>
                </div>

                <button 
                    onClick={handleExport}
                    disabled={loading}
                    className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3 rounded flex items-center justify-center gap-2"
                >
                    {loading ? 'GENERATING...' : 'GENERATE REPORT'}
                </button>
            </div>
        </div>
    );
};

export default AuditExporterModal;
