
import React, { useEffect } from 'react';
import { CreditCard, Zap, Crown, Check, ArrowRight, Clock, ShieldCheck } from 'lucide-react';
import useBillingStore from '../../stores/billingStore';
import './BillingDashboard.css';

const BillingDashboard = () => {
    const { 
        subscription, 
        fetchSubscription, 
        createCheckout, 
        loading 
    } = useBillingStore();

    useEffect(() => {
        fetchSubscription(true); // Default to mock for now
    }, [fetchSubscription]);

    const handleUpgrade = async (tier) => {
        // Map UI tiers to backend plan IDs - based on Billing.jsx
        const planMap = {
            'free': 'price_free_tier',
            'pro': 'price_pro_monthly',
            'institutional': 'price_ent_monthly'
        };
        const planId = planMap[tier.toLowerCase()] || tier;
        const url = await createCheckout(planId, true);
        if (url) {
            alert(`Redirecting to Checkout for ${tier.toUpperCase()} tier...\n(Simulated URL: ${url})`);
        }
    };

    const currentTier = subscription?.plan?.id === 'price_ent_monthly' ? 'INSTITUTIONAL' : 
                      subscription?.plan?.id === 'price_pro_monthly' ? 'PRO' : 'FREE';

    const tiers = [
        {
            name: 'Free',
            price: '$0',
            id: 'price_free_tier',
            icon: <Clock size={24} className="text-gray-400" />,
            features: ['Basic Market Scanner', 'Tutorial Mode', 'Community Support'],
            button: 'Current Plan',
            current: currentTier === 'FREE'
        },
        {
            name: 'Pro',
            price: '$29',
            id: 'price_pro_monthly',
            icon: <Zap size={24} className="text-amber-400" />,
            features: ['Live Execution Router', 'Sentiment Analysis', 'Custom Risk Models', 'Priority Support'],
            button: 'Upgrade to Pro',
            current: currentTier === 'PRO',
            highlight: true
        },
        {
            name: 'Institutional',
            price: '$99',
            id: 'price_ent_monthly',
            icon: <Crown size={24} className="text-purple-400" />,
            features: ['FIX Protocol Adapter', 'Multi-user Workspaces', 'On-prem Deployment', '24/7 Concierge'],
            button: 'Contact Sales',
            current: currentTier === 'INSTITUTIONAL'
        }
    ];

    if (loading && !subscription) return <div className="billing-dashboard-widget p-8 text-center text-zinc-500 font-mono">LOADING BILLING ENGINE...</div>;

    return (
        <div className="billing-dashboard-widget">
            <div className="billing-header">
                <div>
                    <h2>Subscription & Billing</h2>
                    <p className="subtitle">Manage your platform entitlement and payment methods.</p>
                </div>
                <div className="secure-badge">
                    <ShieldCheck size={14} />
                    <span>Secure via Stripe</span>
                </div>
            </div>

            <div className="tiers-grid">
                {tiers.map((t, idx) => (
                    <div key={idx} className={`tier-card ${t.highlight ? 'highlight' : ''} ${t.current ? 'current' : ''}`}>
                        <div className="tier-top">
                            {t.icon}
                            <h3>{t.name}</h3>
                            <div className="price">{t.price}<span>/mo</span></div>
                        </div>
                        <ul className="feature-list">
                            {t.features.map((f, i) => (
                                <li key={i}><Check size={14} /> {f}</li>
                            ))}
                        </ul>
                        <button 
                            className={`tier-btn ${t.highlight ? 'btn-primary' : 'btn-outline'}`}
                            onClick={() => !t.current && handleUpgrade(t.name.toLowerCase())}
                            disabled={t.current}
                        >
                            {t.current ? 'Current Plan' : t.button}
                            {!t.current && <ArrowRight size={16} />}
                        </button>
                    </div>
                ))}
            </div>

            <div className="billing-footer">
                <div className="payment-method">
                    <CreditCard size={18} />
                    <span>{subscription?.status === 'active' ? 'Stripe Connected' : 'No payment method on file'}</span>
                </div>
                <button className="manage-btn" onClick={() => window.open('https://billing.stripe.com/p/session/test_123')}>Manage Portal</button>
            </div>
        </div>
    );
};

export default BillingDashboard;
