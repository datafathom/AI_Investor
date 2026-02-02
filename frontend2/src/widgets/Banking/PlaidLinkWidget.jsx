import React, { useState, useEffect } from 'react';
import { Landmark, CreditCard, Plus, CheckCircle, AlertTriangle, RefreshCcw } from 'lucide-react';
import apiClient from '../../services/apiClient';
import './PlaidLinkWidget.css';

const PlaidLinkWidget = () => {
    const [accounts, setAccounts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [linking, setLinking] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchAccounts();
    }, []);

    const fetchAccounts = async () => {
        try {
            const res = await apiClient.get('/banking/accounts');
            setAccounts(res.data);
        } catch (err) {
            console.error("Failed to fetch bank accounts", err);
            setError("Could not load accounts.");
        } finally {
            setLoading(false);
        }
    };

    const handleLinkBank = async () => {
        setLinking(true);
        setError(null);
        
        try {
            // Step 1: Create Link Token
            const tokenRes = await apiClient.post('/banking/plaid/create-link-token');
            const linkToken = tokenRes.data.link_token;
            
            // Step 2: Simulate Plaid Link Popup (since we are in simulation mode)
            setTimeout(async () => {
                try {
                    // Step 3: Exchange Public Token (Simulated)
                    await apiClient.post('/banking/plaid/exchange-public-token', {
                        public_token: `mock_public_token_${Math.random().toString(36).substr(2, 9)}`
                    });
                    
                    await fetchAccounts();
                    setLinking(false);
                } catch (e) {
                    setError("Failed to link account.");
                    setLinking(false);
                }
            }, 2000);
            
        } catch (err) {
            setError("Failed to initialize Link.");
            setLinking(false);
        }
    };

    if (loading) return <div className="plaid-link-widget loading">Fetching Accounts...</div>;

    return (
        <div className="plaid-link-widget">
            <div className="widget-header">
                <h3><Landmark size={18} className="text-blue-400" /> Linked Banking</h3>
                <button 
                    className="btn-link" 
                    onClick={handleLinkBank}
                    disabled={linking}
                >
                    {linking ? <RefreshCcw size={14} className="animate-spin" /> : <Plus size={14} />}
                    {linking ? "Linking..." : "Connect Bank"}
                </button>
            </div>

            <div className="accounts-list">
                {accounts.length === 0 ? (
                    <div className="empty-state">
                        <CreditCard size={32} className="text-gray-600 mb-2" />
                        <p>No institutional accounts linked.</p>
                    </div>
                ) : (
                    accounts.map(acc => (
                        <div key={acc.id} className="account-item">
                            <div className="acc-info">
                                <span className="acc-name">{acc.name}</span>
                                <span className="acc-type">{acc.type}</span>
                            </div>
                            <div className="acc-balance">
                                <span className={`val ${acc.balance < 0 ? 'text-red-400' : 'text-green-400'}`}>
                                    ${acc.balance.toLocaleString(undefined, { minimumFractionDigits: 2 })}
                                </span>
                            </div>
                        </div>
                    ))
                )}
            </div>

            {error && (
                <div className="widget-error">
                    <AlertTriangle size={12} /> {error}
                </div>
            )}

            <div className="widget-footer">
                <span className="security-tag"><CheckCircle size={10} /> AES-256 Encrypted</span>
                <span className="power-tag">Powered by Plaid (Simulated)</span>
            </div>
        </div>
    );
};

export default PlaidLinkWidget;
