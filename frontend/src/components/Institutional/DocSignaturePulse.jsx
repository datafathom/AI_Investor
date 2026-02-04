import React, { useEffect } from 'react';
import { FileText, CheckCircle2, Clock, AlertCircle } from 'lucide-react';
import useInstitutionalStore from '../../stores/institutionalStore';
import './DocSignaturePulse.css';

const DocSignaturePulse = ({ clientId }) => {
    const { signatures, fetchSignatures, loading } = useInstitutionalStore();

    useEffect(() => {
        if (clientId) fetchSignatures(clientId);
    }, [clientId, fetchSignatures]);

    const data = signatures[clientId] || {
        documents: [],
        completion_percentage: 0,
        is_fully_signed: false
    };

    if (loading && !signatures[clientId]) {
        return <div className="doc-signature-pulse-loading glass-premium">Scanning Documents...</div>;
    }

    return (
        <div className="doc-signature-pulse glass-premium p-6 rounded-3xl border border-white/5">
            <div className="flex justify-between items-start mb-6">
                <div>
                    <h3 className="text-slate-400 text-xs uppercase tracking-widest font-bold flex items-center gap-2">
                        <FileText size={14} className="text-primary" />
                        Signature Pulse
                    </h3>
                    <div className="text-2xl font-bold mt-1">
                        {data.completion_percentage}% <span className="text-xs text-slate-500 font-normal">Complete</span>
                    </div>
                </div>
                <div className="relative w-12 h-12">
                    <svg className="w-full h-full" viewBox="0 0 36 36">
                        <path
                            className="stroke-white/5"
                            strokeDasharray="100, 100"
                            d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                            fill="none"
                            strokeWidth="3"
                        />
                        <path
                            className="stroke-primary"
                            strokeDasharray={`${data.completion_percentage}, 100`}
                            d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                            fill="none"
                            strokeWidth="3"
                            strokeLinecap="round"
                        />
                    </svg>
                </div>
            </div>

            <div className="space-y-3">
                {data.documents.map((doc) => (
                    <div key={doc.id} className="flex items-center justify-between p-3 rounded-xl bg-white/5 border border-white/5 hover:border-white/10 transition-all cursor-pointer group">
                        <div className="flex items-center gap-3">
                            <div className={`p-2 rounded-lg ${doc.status === 'Signed' ? 'bg-success/20 text-success' : 'bg-warning/20 text-warning'}`}>
                                {doc.status === 'Signed' ? <CheckCircle2 size={16} /> : <Clock size={16} />}
                            </div>
                            <div>
                                <div className="text-xs font-bold text-white group-hover:text-primary transition-colors">{doc.name}</div>
                                <div className="text-[10px] text-slate-500">{doc.date}</div>
                            </div>
                        </div>
                        <div className={`text-[10px] font-bold px-2 py-1 rounded-full ${
                            doc.status === 'Signed' ? 'bg-success/10 text-success' : 'bg-warning/10 text-warning'
                        }`}>
                            {doc.status.toUpperCase()}
                        </div>
                    </div>
                ))}
            </div>

            {data.completion_percentage < 100 && (
                <button className="w-full mt-6 py-3 rounded-xl bg-primary/10 border border-primary/20 text-primary text-xs font-bold hover:bg-primary hover:text-white transition-all flex items-center justify-center gap-2">
                    <AlertCircle size={14} /> SEND REMINDERS
                </button>
            )}
        </div>
    );
};

export default DocSignaturePulse;
