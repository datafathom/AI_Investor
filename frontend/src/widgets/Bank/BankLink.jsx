/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Bank/BankLink.jsx
 * ROLE: Bank Integration Widget
 * PURPOSE: Simulates Plaid Link flow and displays connected accounts.
 * ==============================================================================
 */

import React, { useEffect, useState } from 'react';
import useBankStore from '../../stores/bankStore';
import './BankLink.css';

const BankLink = ({ mock = true }) => {
    const { linkToken, accounts, fetchLinkToken, exchangePublicToken, loading, error, isLinked } = useBankStore();
    const [showModal, setShowModal] = useState(false);

    useEffect(() => {
        fetchLinkToken(mock);
    }, [mock, fetchLinkToken]);

    const handleConnect = () => {
        if (linkToken) setShowModal(true);
    };

    const handleMockSuccess = () => {
        setShowModal(false);
        // Simulate Plaid Success Callback
        const mockPublicToken = "public-sandbox-mock-123";
        exchangePublicToken(mockPublicToken, mock);
    };

    return (
        <div className="bank-link-widget">
            <header className="widget-header">
                <h3>Bank Connections</h3>
                {isLinked ? (
                    <span className="status linked">● Linked</span>
                ) : (
                    <span className="status not-linked">○ Not Connected</span>
                )}
            </header>

            {error && <div className="error-msg">{error}</div>}

            {!isLinked && (
                <div className="connect-action">
                    <p>Connect your bank account to sync balances securely.</p>
                    <button 
                        className="plaid-btn" 
                        onClick={handleConnect}
                        disabled={loading || !linkToken}
                    >
                        {loading ? 'Connecting...' : 'Connect Bank (Plaid)'}
                    </button>
                </div>
            )}

            {isLinked && (
                <div className="accounts-list">
                    {accounts.map(acc => (
                        <div key={acc.account_id} className="account-item">
                            <div className="acc-info">
                                <div className="acc-name">{acc.name}</div>
                                <div className="acc-mask">•••• {acc.mask}</div>
                            </div>
                            <div className="acc-balance">
                                ${acc.balances.current.toLocaleString(undefined, { minimumFractionDigits: 2 })}
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* Mock Plaid Link Modal */}
            {showModal && (
                <div className="mock-modal-overlay">
                    <div className="mock-modal">
                        <div className="modal-header">
                            <h4>Select your bank</h4>
                            <button onClick={() => setShowModal(false)} className="close-btn">×</button>
                        </div>
                        <div className="institution-grid">
                            <div className="inst-card" onClick={handleMockSuccess}>
                                <div className="icon">CH</div>
                                <span>Chase</span>
                            </div>
                            <div className="inst-card" onClick={handleMockSuccess}>
                                <div className="icon">BOA</div>
                                <span>Bank of America</span>
                            </div>
                            <div className="inst-card" onClick={handleMockSuccess}>
                                <div className="icon">WF</div>
                                <span>Wells Fargo</span>
                            </div>
                        </div>
                        <p className="modal-footer">Plaid Sandbox Mode (Mock)</p>
                    </div>
                </div>
            )}
        </div>
    );
};

export default BankLink;
