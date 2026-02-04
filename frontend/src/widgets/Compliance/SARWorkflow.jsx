import React, { useEffect } from 'react';
import { FileText, Clock, AlertTriangle, ShieldCheck, ArrowRight, Loader2 } from 'lucide-react';
import useComplianceStore from '../../stores/complianceStore';
import './SARWorkflow.css';

const SARWorkflow = () => {
    const { sarAlerts, fetchSarAlerts, updateSarStatus, isLoading } = useComplianceStore();

    useEffect(() => {
        fetchSarAlerts();
    }, [fetchSarAlerts]);

    const activeCase = (sarAlerts || []).find(a => a.status === 'pending') || (sarAlerts || [])[0];

    const handleStatusUpdate = async (id, status) => {
        await updateSarStatus(id, status);
    };

    if (isLoading && !activeCase) {
        return <div className="sar-workflow-widget"><Loader2 className="animate-spin m-auto" /></div>;
    }

    if (!activeCase) {
        return (
            <div className="sar-workflow-widget">
                <div className="p-8 text-center text-slate-500">
                    <ShieldCheck size={48} className="mx-auto mb-4 opacity-20" />
                    All cases cleared.
                </div>
            </div>
        );
    }

    return (
        <div className="sar-workflow-widget">
            <div className="widget-header">
                <h3><FileText size={18} /> SAR Automated Flagging (Form 111)</h3>
                <span className={`status-tag ${activeCase.status}`}>{activeCase.status.toUpperCase()}</span>
            </div>

            <div className="sar-status-tracker">
                <div className="step visited">Detected</div>
                <div className="step-line active"></div>
                <div className="step active">Review</div>
                <div className="step-line"></div>
                <div className="step">Filing</div>
            </div>

            <div className="current-case">
                <h4>Case #{activeCase.id.substring(0, 8).toUpperCase()}</h4>
                <div className="case-meta">
                    <div className="meta-item">
                        <Clock size={12} /> Due: 28 Days
                    </div>
                    <div className="meta-item warning">
                        <AlertTriangle size={12} /> Suspicion: {activeCase.type.toUpperCase()}
                    </div>
                </div>
            </div>

            <div className="draft-preview">
                <h5>Auto-Generated Narrative Draft</h5>
                <div className="text-content">
                    {activeCase.description}. Evidence score of {(activeCase.evidence_score * 100).toFixed(1)}% indicates high probability of {activeCase.type}. Agent tracking suggests immediate manual review...
                </div>
            </div>

            <div className="workflow-actions">
                <button 
                    className="primary-btn" 
                    onClick={() => handleStatusUpdate(activeCase.id, 'reviewed')}
                >
                    Mark Reviewed <ArrowRight size={14} className="ml-1" />
                </button>
                <button 
                    className="secondary-btn"
                    onClick={() => handleStatusUpdate(activeCase.id, 'filed')}
                >
                    File with Regulator
                </button>
            </div>
        </div>
    );
};

export default SARWorkflow;
