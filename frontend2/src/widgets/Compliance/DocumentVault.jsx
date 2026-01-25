import React, { useState, useEffect } from 'react';
import { Folder, FileText, Search, Lock, Clock, Eye, Download, Filter } from 'lucide-react';
import useKYCStore from '../../stores/kycStore';
import './DocumentVault.css';

/**
 * Document Vault Widget
 * 
 * Secure document management with version control and audit trail.
 * Connected to KYCService via kycStore.
 */
const DocumentVault = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('all');
    const { documents, fetchDocuments, isLoading } = useKYCStore();

    useEffect(() => {
        fetchDocuments();
    }, []);

    // Transform store documents or use fallback
    const vaultDocuments = documents.length > 0 ? documents.map(d => ({
        id: d.id,
        name: d.filename || d.type,
        category: d.document_type || 'KYC',
        date: d.uploadedAt || d.uploaded_at,
        versions: 1,
        access: 'officer'
    })) : [
        { id: 1, name: 'Operating Agreement v3.2', category: 'Corporate', date: '2026-01-10', versions: 3, access: 'admin' },
        { id: 2, name: 'Trust Deed - Family Trust', category: 'Trust', date: '2025-12-15', versions: 2, access: 'officer' },
        { id: 3, name: '2025 Q4 13F Filing', category: 'SEC', date: '2026-01-05', versions: 1, access: 'readonly' },
        { id: 4, name: 'Investment Policy Statement', category: 'Policy', date: '2025-11-20', versions: 5, access: 'admin' },
        { id: 5, name: 'Accredited Investor Cert', category: 'KYC', date: '2025-10-01', versions: 1, access: 'officer' },
    ];

    const categories = ['all', 'Corporate', 'Trust', 'SEC', 'Policy', 'KYC'];

    const filteredDocs = vaultDocuments.filter(doc => {
        const matchesSearch = doc.name.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesCategory = selectedCategory === 'all' || doc.category === selectedCategory;
        return matchesSearch && matchesCategory;
    });

    const auditLog = [
        { user: 'admin@fund.com', action: 'Viewed', doc: 'Operating Agreement v3.2', time: '5 min ago' },
        { user: 'compliance@fund.com', action: 'Downloaded', doc: '2025 Q4 13F Filing', time: '1 hour ago' },
        { user: 'analyst@fund.com', action: 'Access Denied', doc: 'Trust Deed', time: '2 hours ago' },
    ];

    return (
        <div className="document-vault">
            <div className="vault-header">
                <div className="header-left">
                    <Lock size={16} />
                    <h3>Document Vault</h3>
                </div>
                <div className="search-bar">
                    <Search size={14} />
                    <input 
                        type="text" 
                        placeholder="Search documents..." 
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
            </div>

            <div className="category-filters">
                {categories.map(cat => (
                    <button 
                        key={cat}
                        className={`filter-btn ${selectedCategory === cat ? 'active' : ''}`}
                        onClick={() => setSelectedCategory(cat)}
                    >
                        {cat === 'all' ? 'All' : cat}
                    </button>
                ))}
            </div>

            <div className="documents-grid">
                {filteredDocs.map(doc => (
                    <div key={doc.id} className="doc-card">
                        <div className="doc-icon">
                            <FileText size={24} />
                        </div>
                        <div className="doc-details">
                            <span className="doc-name">{doc.name}</span>
                            <div className="doc-meta">
                                <span><Clock size={10} /> {doc.date}</span>
                                <span>v{doc.versions}</span>
                            </div>
                        </div>
                        <div className="doc-actions">
                            <button className="action-icon"><Eye size={14} /></button>
                            <button className="action-icon"><Download size={14} /></button>
                        </div>
                    </div>
                ))}
            </div>

            <div className="audit-section">
                <h4>Recent Activity</h4>
                <div className="audit-log">
                    {auditLog.map((entry, idx) => (
                        <div key={idx} className={`audit-entry ${entry.action === 'Access Denied' ? 'denied' : ''}`}>
                            <span className="audit-user">{entry.user}</span>
                            <span className="audit-action">{entry.action}</span>
                            <span className="audit-doc">{entry.doc}</span>
                            <span className="audit-time">{entry.time}</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default DocumentVault;
