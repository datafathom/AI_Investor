import React from 'react';
import { PenTool, Clock, CheckCircle2 } from 'lucide-react';

const DocSignaturePulse = () => {
    const docs = [
        { id: 1, name: "Engagement Alpha", client: "Family Office Alpha", status: "Signed", date: "2h ago" },
        { id: 2, name: "Risk Disclosure", client: "Endowment Beta", status: "Pending", date: "Active" },
        { id: 3, name: "AML Attestation", client: "Trust Gamma", status: "Expired", date: "2d ago" },
    ];

    return (
        <div className="glass-premium p-4 rounded-2xl border border-white/5 h-full flex flex-col">
            <h3 className="text-sm font-bold mb-4 flex items-center gap-2 text-warning-light">
                <PenTool size={16} /> DOC SIGNATURE PULSE
            </h3>
            
            <div className="flex-1 overflow-y-auto space-y-2 pr-1">
                {docs.map(doc => (
                    <div key={doc.id} className="p-3 rounded-xl bg-white/5 border border-white/5 flex items-center justify-between transition-hover hover:bg-white/10">
                        <div className="flex items-center gap-3">
                            <div className={`p-2 rounded-lg ${
                                doc.status === 'Signed' ? 'bg-success/20 text-success' : 
                                doc.status === 'Pending' ? 'bg-warning/20 text-warning' : 
                                'bg-danger/20 text-danger'
                            }`}>
                                {doc.status === 'Signed' ? <CheckCircle2 size={14} /> : <Clock size={14} />}
                            </div>
                            <div>
                                <div className="text-xs font-bold text-white uppercase tracking-tighter">{doc.name}</div>
                                <div className="text-[9px] text-slate-500">{doc.client}</div>
                            </div>
                        </div>
                        <div className="text-[8px] font-mono text-slate-500 uppercase">{doc.date}</div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default DocSignaturePulse;
