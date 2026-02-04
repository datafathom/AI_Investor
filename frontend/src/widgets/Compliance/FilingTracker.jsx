import React, { useState, useEffect } from 'react';
import { Calendar, Check, X, Clock, Download, AlertTriangle, FileText } from 'lucide-react';
import useKYCStore from '../../stores/kycStore';
import './FilingTracker.css';

/**
 * Regulatory Filing Tracker
 * 
 * Tracks SEC filings, deadlines, and compliance status.
 * Connected to KYCService via kycStore.
 */
const FilingTracker = () => {
    const [selectedQuarter, setSelectedQuarter] = useState('Q4 2025');
    const { filingDeadlines, fetchFilingDeadlines, export13F, isLoading } = useKYCStore();

    useEffect(() => {
        fetchFilingDeadlines();
    }, []);

    // Transform store data or use fallback
    const filings = filingDeadlines.length > 0 ? filingDeadlines.map((f, i) => ({
        id: i + 1,
        type: f.filingType || '13F',
        quarter: selectedQuarter,
        deadline: f.dueDate || f.due_date,
        daysRemaining: f.daysRemaining || f.days_remaining || 0,
        status: f.status === 'due_soon' || f.status === 'upcoming' ? 'in_progress' : f.status === 'overdue' ? 'overdue' : 'filed',
        completeness: f.status === 'upcoming' ? 85 : 100
    })) : [
        { id: 1, type: '13F', quarter: 'Q4 2025', deadline: '2026-02-14', daysRemaining: 27, status: 'in_progress', completeness: 85 },
        { id: 2, type: '13F', quarter: 'Q3 2025', deadline: '2025-11-14', daysRemaining: 0, status: 'filed', completeness: 100 },
        { id: 3, type: '13F', quarter: 'Q2 2025', deadline: '2025-08-14', daysRemaining: 0, status: 'filed', completeness: 100 },
    ];

    const dataRequirements = [
        { item: 'Portfolio Holdings Snapshot', complete: true },
        { item: 'Position Sizes (Share Count)', complete: true },
        { item: 'Market Value Calculations', complete: true },
        { item: 'Options Disclosure', complete: false },
        { item: 'Voting Authority', complete: false },
    ];

    const currentFiling = filings.find(f => f.status === 'in_progress');
    const completedItems = dataRequirements.filter(d => d.complete).length;

    const handleExport = () => {
        export13F('default_portfolio');
    };

    return (
        <div className="filing-tracker">
            <div className="tracker-header">
                <div className="header-left">
                    <FileText size={16} />
                    <h3>13F Filing Tracker</h3>
                </div>
                {currentFiling && (
                    <div className="deadline-countdown">
                        <Clock size={14} />
                        <span>{currentFiling.daysRemaining} days until deadline</span>
                    </div>
                )}
            </div>

            {currentFiling && (
                <div className="current-filing">
                    <div className="filing-progress">
                        <div className="progress-circle">
                            <svg viewBox="0 0 36 36">
                                <path
                                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                                    fill="none"
                                    stroke="var(--border-primary)"
                                    strokeWidth="3"
                                />
                                <path
                                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                                    fill="none"
                                    stroke="var(--color-success)"
                                    strokeWidth="3"
                                    strokeDasharray={`${currentFiling.completeness}, 100`}
                                />
                            </svg>
                            <span className="progress-text">{currentFiling.completeness}%</span>
                        </div>
                        <div className="filing-info">
                            <span className="filing-type">{currentFiling.type} - {currentFiling.quarter}</span>
                            <span className="filing-deadline">Due: {currentFiling.deadline}</span>
                        </div>
                    </div>
                </div>
            )}

            <div className="requirements-section">
                <h4>Data Readiness</h4>
                <div className="requirements-list">
                    {dataRequirements.map((req, idx) => (
                        <div key={idx} className={`requirement-item ${req.complete ? 'complete' : 'incomplete'}`}>
                            {req.complete ? (
                                <Check size={14} className="check-icon" />
                            ) : (
                                <X size={14} className="x-icon" />
                            )}
                            <span>{req.item}</span>
                        </div>
                    ))}
                </div>
                <div className="readiness-summary">
                    {completedItems === dataRequirements.length ? (
                        <span className="ready-badge">Ready to File</span>
                    ) : (
                        <span className="pending-badge">
                            <AlertTriangle size={12} />
                            {dataRequirements.length - completedItems} items pending
                        </span>
                    )}
                </div>
            </div>

            <div className="filing-history">
                <h4>Filing History</h4>
                <div className="history-list">
                    {filings.filter(f => f.status === 'filed').map(filing => (
                        <div key={filing.id} className="history-item">
                            <span className="history-quarter">{filing.quarter}</span>
                            <span className="history-date">{filing.deadline}</span>
                            <button className="download-btn">
                                <Download size={12} /> XML
                            </button>
                        </div>
                    ))}
                </div>
            </div>

            <div className="tracker-actions">
                <button className="export-btn" onClick={handleExport}>
                    <Download size={14} /> Export EDGAR XML
                </button>
            </div>
        </div>
    );
};

export default FilingTracker;
