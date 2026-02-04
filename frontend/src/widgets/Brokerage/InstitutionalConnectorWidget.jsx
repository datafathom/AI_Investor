import React, { useState, useEffect } from 'react';
import { Shield, Plus, ExternalLink, RefreshCw, CheckCircle2, AlertCircle, Search } from 'lucide-react';
import apiClient from '../../services/apiClient';
import './InstitutionalConnectorWidget.css';

const InstitutionalConnectorWidget = () => {
    const [providers, setProviders] = useState(null);
    const [status, setStatus] = useState(null);
    const [loading, setLoading] = useState(true);
    const [selectedCategory, setSelectedCategory] = useState('execution');
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [pRes, sRes] = await Promise.all([
                    apiClient.get('/brokerage/providers'),
                    apiClient.get('/brokerage/status')
                ]);
                setProviders(pRes.data);
                setStatus(sRes.data);
            } catch (err) {
                console.error("Failed to load institutional connectors", err);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    const filteredProviders = providers && providers[selectedCategory] 
        ? providers[selectedCategory].filter(p => p.toLowerCase().includes(searchTerm.toLowerCase()))
        : [];

    if (loading) return <div className="ic-widget loading">Vault Link Handshake...</div>;

    return (
        <div className="ic-widget">
            <div className="ic-header">
                <div className="title-group">
                    <h3>Institutional Vault</h3>
                    <p className="subtitle">{status?.summary || "No active links"}</p>
                </div>
                <div className="security-badge">
                    <Shield size={14} className="text-green-400" />
                    <span>AES-256</span>
                </div>
            </div>

            <div className="active-links-section">
                <h4>Active Secure Links</h4>
                <div className="links-grid">
                    {status?.connections?.map((conn, idx) => (
                        <div key={idx} className="link-card active">
                            <div className="link-info">
                                <span className="name">{conn.name}</span>
                                <span className="type">{conn.type}</span>
                            </div>
                            <CheckCircle2 size={16} className="text-blue-400" />
                        </div>
                    ))}
                </div>
            </div>

            <div className="add-connection-section">
                <h4>Link New Institution</h4>
                <div className="category-tabs">
                    {providers && Object.keys(providers).map(cat => (
                        <button 
                            key={cat} 
                            className={`tab ${selectedCategory === cat ? 'active' : ''}`}
                            onClick={() => setSelectedCategory(cat)}
                        >
                            {cat}
                        </button>
                    ))}
                </div>

                <div className="search-box">
                    <Search size={14} />
                    <input 
                        type="text" 
                        placeholder={`Search ${selectedCategory}...`}
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>

                <div className="provider-list">
                    {filteredProviders.map(p => (
                        <div key={p} className="provider-item">
                            <span>{p}</span>
                            <button className="btn-connect">
                                <Plus size={14} /> Link
                            </button>
                        </div>
                    ))}
                </div>
            </div>

            <div className="ic-footer">
                <p><AlertCircle size={10} /> Read-only aggregation is prioritized for security. Execution requires MFA.</p>
            </div>
        </div>
    );
};

export default InstitutionalConnectorWidget;
