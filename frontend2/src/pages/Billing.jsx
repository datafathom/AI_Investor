/**
 * ==============================================================================
 * FILE: frontend2/src/pages/Billing.jsx
 * ROLE: Settings Page
 * PURPOSE: Subscription management and upgrade dashboard.
 * ==============================================================================
 */

import React, { useEffect } from 'react';
import PropTypes from 'prop-types';
import useBillingStore from '../stores/billingStore';
import PayPalButton from '../components/Checkout/PayPalButton';
import VenmoButton from '../components/Checkout/VenmoButton';
import './Billing.css';

const Billing = ({ mock = true }) => {
    const { subscription, fetchSubscription, createCheckout, loading, error } = useBillingStore();

    useEffect(() => {
        fetchSubscription(mock);
    }, [mock, fetchSubscription]);

    const handleUpgrade = async (planId) => {
        const url = await createCheckout(planId, mock);
        if (url) {
            alert(`Redirecting to Stripe Mock: ${url}`);
        }
    };

    if (loading && !subscription) return <div className="billing-page loading">Loading billing info...</div>;
    if (error) return <div className="billing-page error">Error: {error}</div>;

    const currentPlanId = subscription?.plan?.id || 'price_free_tier';

    return (
        <div className="billing-page">
            <header className="billing-header">
                <h1>Subscription & Billing</h1>
                <p>Manage your account tier and payment method.</p>
            </header>

            <section className="current-subs">
                <h2>Current Subscription</h2>
                <div className="subs-card">
                    <div className="status">
                        <span className={`badge ${subscription?.status}`}>
                            {subscription?.status.toUpperCase() || 'UNKNOWN'}
                        </span>
                    </div>
                    <div className="details">
                        <h3>{subscription?.plan?.name || 'Free Tier'}</h3>
                        <p className="price">
                            ${(subscription?.plan?.amount || 0) / 100} / {subscription?.plan?.interval || 'mo'}
                        </p>
                        <p className="renewal">
                            Renews on: {subscription?.current_period_end ? new Date(subscription.current_period_end).toLocaleDateString() : 'N/A'}
                        </p>
                    </div>
                </div>
            </section>

            <section className="plans-grid">
                <h2>Available Plans</h2>
                <div className="grid">
                    {/* Free Plan */}
                    <div className={`plan-card ${currentPlanId === 'price_free_tier' ? 'active' : ''}`}>
                        <h3>Free Tier</h3>
                        <p className="price">$0/mo</p>
                        <ul>
                            <li>✓ Basic Market Data</li>
                            <li>✓ 5 AI Briefings / mo</li>
                            <li>✓ Community Access</li>
                        </ul>
                        <button disabled={currentPlanId === 'price_free_tier'}>
                            {currentPlanId === 'price_free_tier' ? 'Current Plan' : 'Downgrade'}
                        </button>
                    </div>

                    {/* Pro Plan */}
                    <div className={`plan-card pro ${currentPlanId === 'price_pro_monthly' ? 'active' : ''}`}>
                        <div className="recommended">RECOMMENDED</div>
                        <h3>Pro Investor</h3>
                        <p className="price">$29/mo</p>
                        <ul>
                            <li>✓ Real-time Alpha Vantage Data</li>
                            <li>✓ Unlimited AI Briefings (Gemini)</li>
                            <li>✓ Deep Research (Perplexity)</li>
                            <li>✓ Advanced Portfolio Analytics</li>
                        </ul>
                        <button 
                            className="primary-btn"
                            disabled={currentPlanId === 'price_pro_monthly'}
                            onClick={() => handleUpgrade('price_pro_monthly')}
                        >
                            {currentPlanId === 'price_pro_monthly' ? 'Current Plan' : 'Upgrade to Pro'}
                        </button>
                        
                        {currentPlanId !== 'price_pro_monthly' && (
                             <div className="alternative-payment">
                                 <div className="divider"><span>OR</span></div>
                                 <PayPalButton 
                                     amount={29.00} 
                                     onSuccess={(data) => alert(`PayPal Success! TXN: ${data.purchase_units[0].payments.captures[0].id}`)}
                                     mock={mock}
                                 />
                                 <VenmoButton 
                                     amount={29.00} 
                                     onSuccess={(data) => alert(`Venmo Success! ID: ${data.id}`)}
                                     mock={mock}
                                 />
                             </div>
                        )}
                    </div>

                    {/* Enterprise Plan */}
                    <div className={`plan-card ent ${currentPlanId === 'price_ent_monthly' ? 'active' : ''}`}>
                        <h3>Enterprise</h3>
                        <p className="price">$99/mo</p>
                        <ul>
                            <li>✓ All Pro Features</li>
                            <li>✓ Institutional Data (IBKR)</li>
                            <li>✓ API Access Key</li>
                            <li>✓ Priority Support</li>
                        </ul>
                        <button 
                             disabled={currentPlanId === 'price_ent_monthly'}
                             onClick={() => handleUpgrade('price_ent_monthly')}
                        >
                            {currentPlanId === 'price_ent_monthly' ? 'Current Plan' : 'Contact Sales'}
                        </button>
                    </div>
                </div>
            </section>
            
            {mock && <div className="mock-banner">STRIPE BILLING SIMULATON (MOCK)</div>}
        </div>
    );
};

Billing.propTypes = {
    mock: PropTypes.bool
};

export default Billing;
