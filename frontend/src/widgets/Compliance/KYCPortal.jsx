import React, { useState, useEffect } from 'react';
import { Shield, Upload, Check, X, Clock, AlertTriangle, FileText, User } from 'lucide-react';
import useKYCStore from '../../stores/kycStore';
import './KYCPortal.css';

/**
 * KYC Verification Portal
 * 
 * Secure portal for identity verification with AES-256 encrypted document upload.
 * Connected to KYCService via kycStore.
 */
const KYCPortal = () => {
    const { 
        documents, 
        verificationStatus,
        fetchDocuments, 
        fetchVerificationStatus,
        uploadDocument,
        isLoading 
    } = useKYCStore();

    useEffect(() => {
        fetchDocuments();
        fetchVerificationStatus();
    }, []);

    // Use store data
    const displayDocuments = documents.length > 0 ? documents.map(d => ({
        id: d.id,
        type: d.type || d.document_type || 'Document',
        status: d.status,
        encrypted: true
    })) : [];

    const getStatusIcon = (status) => {
        switch (status?.toLowerCase()) {
            case 'approved':
            case 'verified': return <Check size={14} className="status-approved" />;
            case 'rejected': return <X size={14} className="status-rejected" />;
            case 'in_review':
            case 'pending': return <Clock size={14} className="status-review" />;
            default: return <AlertTriangle size={14} className="status-pending" />;
        }
    };

    const getStatusLabel = (status) => {
        switch (status?.toLowerCase()) {
            case 'approved':
            case 'verified': return 'Verified';
            case 'rejected': return 'Rejected';
            case 'in_review': return 'In Review';
            case 'pending': return 'Pending';
            default: return 'Unknown';
        }
    };

    const handleUpload = (docType) => {
        // In a real app, this would trigger a file picker and then call uploadDocument(file, docType)
        console.log(`Triggering upload for ${docType}...`);
    };

    const overallProgress = displayDocuments.length > 0 
        ? (displayDocuments.filter(d => ['approved', 'verified'].includes(d.status?.toLowerCase())).length / displayDocuments.length * 100)
        : 0;

    return (
        <div className="kyc-portal">
            <div className="portal-header">
                <div className="header-icon">
                    <Shield size={20} />
                </div>
                <div className="header-text">
                    <h3>Identity Verification</h3>
                    <span className="subtitle">
                        {verificationStatus?.level ? `${verificationStatus.level.toUpperCase()} LEVEL` : 'AES-256 Encrypted'}
                    </span>
                </div>
            </div>

            <div className="progress-section">
                <div className="progress-bar">
                    <div className="progress-fill" style={{ width: `${overallProgress}%` }}></div>
                </div>
                <span className="progress-label">{overallProgress.toFixed(0)}% Complete</span>
            </div>

            <div className="documents-list">
                {displayDocuments.length > 0 ? displayDocuments.map((doc) => (
                    <div key={doc.id} className={`document-row ${doc.status}`}>
                        <div className="doc-icon">
                            <FileText size={16} />
                        </div>
                        <div className="doc-info">
                            <span className="doc-type">{doc.type}</span>
                            <span className="doc-status">
                                {getStatusIcon(doc.status)}
                                {getStatusLabel(doc.status)}
                            </span>
                        </div>
                        {doc.encrypted && (
                            <span className="encrypted-badge">Encrypted</span>
                        )}
                        {['pending', 'rejected'].includes(doc.status?.toLowerCase()) && (
                            <button className="upload-btn" onClick={() => handleUpload(doc.type)}>
                                <Upload size={14} /> Upload
                            </button>
                        )}
                    </div>
                )) : (
                    <div className="p-4 text-center text-zinc-500 font-mono text-[10px] uppercase">
                        No documents required or found
                    </div>
                )}
            </div>

            <div className="verification-actions">
                <button className="action-btn primary">
                    <User size={14} /> Verify Identity
                </button>
            </div>

            <div className="portal-footer">
                <span>Powered by Plaid & Jumio</span>
            </div>
        </div>
    );
};

export default KYCPortal;
