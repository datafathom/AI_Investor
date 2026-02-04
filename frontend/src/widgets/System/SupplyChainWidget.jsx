
import React, { useEffect, useState } from 'react';
import apiClient from '../../services/apiClient';
import { ShieldCheck, ShieldAlert, FileText } from 'lucide-react';
import './SupplyChainWidget.css';

const SupplyChainWidget = () => {
    const [status, setStatus] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Mock fetch if backend not ready, or actual fetch
        const fetchStatus = async () => {
            try {
                // apiClient handles auth tokens automatically
                const response = await apiClient.get('/system/supply-chain');
                setStatus(response.data);
            } catch (e) {
                // Fallback for demo if 401/403 or server down
                setStatus({ status: 'Unknown', vulnerabilities: 0, last_scan: 'N/A' });
            } finally {
                setLoading(false);
            }
        };

        fetchStatus();
    }, []);

    if (loading) return <div className="sc-widget loading">Scanning Dependencies...</div>;

    const isSecure = status?.status === 'Secure';

    return (
        <div className={`sc-widget ${isSecure ? 'secure' : 'vulnerable'}`}>
            <div className="sc-header">
                <h3>Supply Chain Security</h3>
                {isSecure ? <ShieldCheck size={24} /> : <ShieldAlert size={24} />}
            </div>
            
            <div className="sc-body">
                <div className="sc-metric">
                    <span>Status</span>
                    <span className="value">{status?.status}</span>
                </div>
                <div className="sc-metric">
                    <span>Vulnerabilities</span>
                    <span className="value">{status?.vulnerabilities}</span>
                </div>
                <div className="sc-metric">
                    <span>Last Scan</span>
                    <span className="value text-xs">{status?.last_scan}</span>
                </div>
                 <div className="sc-metric">
                    <span>SBOM</span>
                    <span className="value">{status?.sbom_generated ? 'Generated' : 'Missing'}</span>
                </div>
            </div>
            
             <div className="sc-footer">
                <button className="btn-audit">
                    <FileText size={16} /> View SBOM
                </button>
            </div>
        </div>
    );
};

export default SupplyChainWidget;
