/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Tax/TaxHarvestingDashboard.jsx
 * ROLE: Tax Dashboard
 * PURPOSE: Displays tax harvesting opportunities and estimated savings.
 * ==============================================================================
 */

import React, { useEffect } from 'react';
import useTaxStore from '../../stores/taxStore';
import './TaxHarvestingDashboard.css';

const TaxHarvestingDashboard = ({ mock = true }) => {
    const { report, fetchOpportunities, loading, error } = useTaxStore();

    useEffect(() => {
        fetchOpportunities(mock);
    }, [mock, fetchOpportunities]);

    if (error) return <div className="tax-dash error">Error: {error}</div>;

    const formatCurrency = (val) => 
        (val || 0).toLocaleString('en-US', { style: 'currency', currency: 'USD' });

    return (
        <div className="tax-dash">
            <header className="dash-header">
                <div className="title-row">
                    <h3>Tax Optimizations</h3>
                    <span className="source-badge">TaxBit AI</span>
                </div>
            </header>

            {loading && !report ? (
                <div className="loading-state">Analyzing Portfolio...</div>
            ) : (
                <>
                    <div className="savings-card">
                        <div className="savings-label">Est. Tax Savings</div>
                        <div className="savings-value">{formatCurrency(report?.summary?.estimated_tax_savings)}</div>
                        <div className="savings-sub">
                            Available Losses: {formatCurrency(report?.summary?.short_term_losses_available)}
                        </div>
                    </div>

                    <div className="opps-list">
                        <h4>Harvesting Opportunities</h4>
                        {report?.opportunities?.map((opp, idx) => (
                            <div key={idx} className="opp-row">
                                <div className="opp-info">
                                    <div className="asset">{opp.asset}</div>
                                    <div className="strategy">{opp.strategy}</div>
                                </div>
                                <div className="opp-action">
                                    <div className="loss-amt">Loss: {formatCurrency(opp.unrealized_loss)}</div>
                                    <button className="harvest-btn">{opp.recommendation}</button>
                                </div>
                            </div>
                        ))}
                    </div>
                </>
            )}
            
            <div className="footer">
                <span>TaxBit Integration {mock && '(Mock)'}</span>
            </div>
        </div>
    );
};

export default TaxHarvestingDashboard;
