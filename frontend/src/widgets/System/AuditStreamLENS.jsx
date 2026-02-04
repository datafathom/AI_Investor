/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/System/AuditStreamLENS.jsx
 * ROLE: Immutable Audit Log Stream
 * PURPOSE: Real-time, transparent lens into all critical system actions,
 *          verified via cryptographic hash chaining.
 * ==============================================================================
 */

import React, { useEffect, useRef } from 'react';
import { ShieldCheck, HardDrive, Key, Globe, Layout, User } from 'lucide-react';
import useSystemHealthStore from '../../stores/systemHealthStore';
import './AuditStreamLENS.css';

const AuditStreamLENS = () => {
    const { auditStream, fetchAuditStream } = useSystemHealthStore();
    const scrollRef = useRef(null);

    useEffect(() => {
        fetchAuditStream();
        const interval = setInterval(fetchAuditStream, 3000);
        return () => clearInterval(interval);
    }, [fetchAuditStream]);

    const getTypeIcon = (type) => {
        switch (type) {
            case 'API_ACCESS': return <Globe size={12} className="text-blue-400" />;
            case 'MFA_VERIFY': return <Key size={12} className="text-purple-400" />;
            case 'TRADE_EXEC': return <Layout size={12} className="text-emerald-400" />;
            case 'VAULT_UNLOCK': return <ShieldCheck size={12} className="text-amber-400" />;
            default: return <User size={12} className="text-slate-400" />;
        }
    };

    return (
        <div className="audit-lens">
            <div className="audit-lens__header">
                <div className="flex items-center gap-2">
                    <ShieldCheck size={16} className="text-emerald-500" />
                    <h3 className="text-sm font-bold text-white uppercase tracking-wider">Audit Stream LENS</h3>
                </div>
                <div className="flex items-center gap-1.5">
                    <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                    <span className="text-[9px] font-mono text-emerald-500">LIVE FEED</span>
                </div>
            </div>

            <div className="audit-lens__stream scrollbar-hide" ref={scrollRef}>
                {auditStream.map((log) => (
                    <div key={log.id} className="audit-lens__row">
                        <div className="audit-lens__timestamp">
                            {new Date(log.timestamp).toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                        </div>
                        <div className="audit-lens__type">
                            {getTypeIcon(log.type)}
                            <span>{log.type}</span>
                        </div>
                        <div className="audit-lens__id text-slate-500">
                            ID: {log.user_id}
                        </div>
                        <div className={`audit-lens__hash ${log.hash ? 'text-emerald-500/50' : 'text-red-500/50'}`}>
                            {log.hash || 'UNVERIFIED'}
                        </div>
                    </div>
                ))}
            </div>

            <div className="audit-lens__footer">
                <div className="flex items-center gap-2 text-[9px] text-slate-500">
                    <HardDrive size={10} />
                    <span>STORAGE: Immutable (SHA-256 Chain)</span>
                </div>
            </div>
        </div>
    );
};

export default AuditStreamLENS;
