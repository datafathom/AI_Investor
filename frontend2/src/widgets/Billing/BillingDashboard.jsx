
import React, { useState, useEffect } from 'react';
import { CreditCard, Zap, Crown, Check, ArrowRight, Clock, ShieldCheck } from 'lucide-react';
import './BillingDashboard.css';

const BillingDashboard = () => {
    const [status, setStatus] = useState(null);
    const [loading, setLoading] = useState(false);

    const fetchStatus = async () => {
        setLoading(true);
        try {
            const token = localStorage.getItem('token');
            const res = await fetch('/api/v1/billing/subscription-status', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const data = await res.json();
            setStatus(data);
        } catch (e) {
            console.error("Failed to fetch billing status", e);
        } finally {
            setLoading(false);
        }
    };

    const handleUpgrade = async (tier) => {
        try {
            const token = localStorage.getItem('token');
            const res = await fetch('/api/v1/billing/create-checkout-session', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}` 
                },
                body: JSON.stringify({ tier })
            });
            const data = await res.json();
            if (data.url) {
                // In a real app, window.location.href = data.url;
                // For demo, we just alert
                alert(`Redirecting to Stripe Checkout for ${tier.toUpperCase()} tier...\n(Simulated URL: ${data.url})`);
            }
        } catch (e) {
            console.error("Checkout failed", e);
        }
    };

    useEffect(() => {
        fetchStatus();
    }, []);

    const tiers = [
        {
            name: 'Free',
            price: '$0',
            icon: <Clock size={24} className="text-gray-400" />,
            features: ['Basic Market Scanner', 'Tutorial Mode', 'Community Support'],
            button: 'Current Plan',
            current: status?.tier === 'FREE'
        },
        {
            name: 'Pro',
            price: '$49',
            icon: <Zap size={24} className="text-amber-400" />,
            features: ['Live Execution Router', 'Sentiment Analysis', 'Custom Risk Models', 'Priority Support'],
            button: 'Upgrade to Pro',
            current: status?.tier === 'PRO',
            highlight: true
        },
        {
            name: 'Institutional',
            price: '$499',
            icon: <Crown size={24} className="text-purple-400" />,
            features: ['FIX Protocol Adapter', 'Multi-user Workspaces', 'On-prem Deployment', '24/7 Concierge'],
            button: 'Contact Sales',
            current: status?.tier === 'INSTITUTIONAL'
        }
    ];

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
                    <span>No payment method on file</span>
                </div>
                <button className="manage-btn">Manage Portal</button>
            </div>
        </div>
    );
};

export default BillingDashboard;
