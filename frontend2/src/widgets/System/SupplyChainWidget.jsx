
import React, { useEffect, useState } from 'react';
import { ShieldCheck, ShieldAlert, FileText } from 'lucide-react';
import './SupplyChainWidget.css';

const SupplyChainWidget = () => {
    const [status, setStatus] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Mock fetch if backend not ready, or actual fetch
        const fetchStatus = async () => {
            try {
                // For demo, we might need a token. 
                // Assuming dev auto-login or session exists.
                const token = localStorage.getItem('widget_os_token'); 
                const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
                
                const res = await fetch('/api/v1/system/supply-chain', { headers });
                if (res.ok) {
                    const data = await res.json();
                    setStatus(data);
                } else {
                    // Fallback for demo if 401/403 or server down
                    setStatus({ status: 'Unknown', vulnerabilities: 0, last_scan: 'N/A' });
                }
            } catch (e) {
                console.error("Failed to fetch supply chain status", e);
                setStatus({ status: 'Error', vulnerabilities: -1 });
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
