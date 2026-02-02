import React from 'react';
import apiClient from '../../services/apiClient';
import { Landmark, CreditCard, Wallet, Facebook, Github } from 'lucide-react';
import './SocialLoginButtons.css';

const SocialLoginButtons = ({ onAuthSuccess }) => {
    const providers = [
        { id: 'google', name: 'Google', icon: <Github size={18} />, color: '#ea4335' },
        { id: 'paypal', name: 'PayPal', icon: <Wallet size={18} />, color: '#003087' },
        { id: 'venmo', name: 'Venmo', icon: <Wallet size={18} />, color: '#3d95ce' },
        { id: 'facebook', name: 'Facebook', icon: <Facebook size={18} />, color: '#1877F2' },
        { id: 'plaid', name: 'Plaid', icon: <Landmark size={18} />, color: '#000000' },
        { id: 'stripe', name: 'Stripe', icon: <CreditCard size={18} />, color: '#6366f1' },
        { id: 'square', name: 'Square', icon: <Landmark size={18} />, color: '#22c55e' }
    ];

    const handleSocialAuth = async (providerId) => {
        console.log(`Starting social auth for ${providerId}`);
        
        // Google OAuth uses proper OAuth flow
        if (providerId === 'google') {
            try {
                const response = await apiClient.get('/auth/google/login?redirect=true');
                const data = response.data;
                // Redirect to Google OAuth page
                window.location.href = data.authorization_url;
                return;
            } catch (err) {
                console.error("Google Auth Initiation Failed", err);
            }
        }
        
        // Other providers use mock flow for now
        setTimeout(async () => {
            try {
                const response = await apiClient.post(`/auth/social/callback/${providerId}`, { 
                    code: `mock_code_${Math.random().toString(36).substr(2, 5)}`
                });
                
                const data = response.data;
                onAuthSuccess(data);
            } catch (err) {
                console.error("Social Auth Failed", err);
            }
        }, 1500);
    };

    return (
        <div className="social-login-container">
            <div className="divider">
                <span>Or continue with</span>
            </div>
            
            <div className="social-buttons-grid">
                {providers.map(p => (
                    <button 
                        key={p.id} 
                        className="social-btn" 
                        style={{ '--hover-color': p.color }}
                        onClick={() => handleSocialAuth(p.id)}
                    >
                        {p.icon}
                        <span>{p.name}</span>
                    </button>
                ))}
            </div>
        </div>
    );
};

export default SocialLoginButtons;
