import React from 'react';
import { ClipboardCheck, ArrowRight, Wallet } from 'lucide-react';
import './ReconciliationReport.css';

const ReconciliationReport = () => {
    const [report, setReport] = React.useState(null);
    const [loading, setLoading] = React.useState(true);

    React.useEffect(() => {
        const fetchReport = async () => {
            try {
                const res = await fetch('/api/v1/banking/reconciliation');
                if (res.ok) {
                    const data = await res.json();
                    setReport(data);
                }
            } catch (e) {
                console.error("Failed to fetch recon report", e);
            } finally {
                setLoading(false);
            }
        };
        fetchReport();
    }, []);

    if (loading) return <div className="recon-report-widget loading">Auditing Ledger...</div>;

    const unmatched = report?.unreconciled_bank || [];

    return (
        <div className="recon-report-widget">
            <div className="widget-header">
                <h3><ClipboardCheck size={18} className="text-cyan-400" /> Reconciliation Report</h3>
                <span className="badge">Phase 11 (V0.1)</span>
            </div>

            <div className="stats-grid">
                <div className="stat-box">
                    <span className="label">Matched</span>
                    <span className="val good">{report?.accuracy?.toFixed(1)}%</span>
                </div>
                <div className="stat-box">
                    <span className="label">Unmatched (Bank)</span>
                    <span className="val warn">{report?.unreconciled_bank?.length}</span>
                </div>
                <div className="stat-box">
                    <span className="label">Unreconciled (Ledger)</span>
                    <span className="val warn">{report?.unreconciled_ledger?.length}</span>
                </div>
            </div>

            <div className="unmatched-list">
                <h4>Unmatched Transactions (Bank Side)</h4>
                {unmatched.map((u, idx) => (
                    <div key={idx} className="unmatched-item">
                        <div className="u-date">{u.date}</div>
                        <div className="u-desc">{u.desc}</div>
                        <div className="u-amount">${u.amount?.toFixed(2)}</div>
                        <button className="btn-resolve">
                            Resolve
                        </button>
                    </div>
                ))}
            </div>

            <div className="recon-actions">
                <button className="btn-primary">
                    <Wallet size={14} /> Audit Ledger vs Bank
                </button>
            </div>
        </div>
    );
};

export default ReconciliationReport;
