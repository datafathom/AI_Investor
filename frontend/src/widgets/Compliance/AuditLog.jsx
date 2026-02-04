import React, { useState, useEffect } from 'react';
import { List, Search, Lock, CheckCircle, Download, ShieldCheck, XCircle, Loader2 } from 'lucide-react';
import useComplianceStore from '../../stores/complianceStore';
import './AuditLog.css';

const AuditLog = () => {
    const { auditLogs, fetchAuditLogs, verifyIntegrity, verificationStatus, isLoading } = useComplianceStore();
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        fetchAuditLogs();
    }, [fetchAuditLogs]);

    const handleVerify = async () => {
        await verifyIntegrity();
    };

    const filteredLogs = auditLogs.filter(log => 
        log.action.toLowerCase().includes(searchTerm.toLowerCase()) ||
        log.resource.toLowerCase().includes(searchTerm.toLowerCase()) ||
        log.id.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="audit-log-widget">
            <div className="widget-header">
                <h3><List size={18} /> Immutable Activity Audit Log</h3>
                <div className="header-actions">
                    <button 
                        className={`verify-btn ${verificationStatus?.is_valid ? 'verified' : ''}`}
                        onClick={handleVerify}
                        disabled={isLoading}
                    >
                        {isLoading ? <Loader2 size={12} className="animate-spin" /> : <Lock size={12} />}
                        {verificationStatus ? (
                            verificationStatus.is_valid ? (
                                <><span className="text-green-400">Chain Verified</span> <CheckCircle size={12} className="text-green-400"/></>
                            ) : (
                                <><span className="text-red-400">Chain Corrupt</span> <XCircle size={12} className="text-red-400"/></>
                            )
                        ) : (
                            <span>Verify Integrity</span>
                        )}
                    </button>
                    <button className="icon-btn" title="Export Audit Pack"><Download size={14}/></button>
                </div>
            </div>

            <div className="log-filters">
                <div className="search-bar">
                    <Search size={14} />
                    <input 
                        type="text" 
                        placeholder="Search logs..." 
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
                <select className="filter-select">
                    <option>All Events</option>
                    <option>Orders</option>
                    <option>Decisions</option>
                    <option>Errors</option>
                </select>
            </div>

            <div className="log-table-container">
                <table className="log-table">
                    <thead>
                        <tr>
                            <th>Time (UTC)</th>
                            <th>Action</th>
                            <th>Resource</th>
                            <th>Hash (SHA-256)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredLogs.map(log => (
                            <tr key={log.id}>
                                <td className="font-mono text-xs">
                                    {new Date(log.timestamp).toISOString().split('T')[1].replace('Z', '')}
                                </td>
                                <td>
                                    <span className={`type-badge ${log.severity.toLowerCase()}`}>
                                        {log.action}
                                    </span>
                                </td>
                                <td>{log.resource}</td>
                                <td className="font-mono text-[10px] text-slate-500">
                                    {log.hash.substring(0, 16)}...
                                    <ShieldCheck size={10} className="inline ml-1 text-slate-400" />
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            
            <div className="log-footer">
                <span>Latest Block: {auditLogs[0]?.hash.substring(0, 8) || 'N/A'}</span>
                <span>{auditLogs.length} entries tracked</span>
            </div>
        </div>
    );
};

export default AuditLog;
