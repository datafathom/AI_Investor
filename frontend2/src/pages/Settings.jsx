
import React, { useState, useEffect } from 'react';
import BillingDashboard from '../widgets/Billing/BillingDashboard'; 
import IdentityProfileCard from '../components/Identity/IdentityProfileCard';
import { Settings as SettingsIcon, CreditCard, Palette, User, ShieldCheck } from 'lucide-react';
import './Settings.css';

function Settings() {
  const [activeTab, setActiveTab] = useState('billing');
  const [identityData, setIdentityData] = useState(null);
  const [loadingIdentity, setLoadingIdentity] = useState(false);

  // Fetch Identity Profile when tab is active
  useEffect(() => {
    if (activeTab === 'identity' && !identityData) {
        fetchIdentity();
    }
  }, [activeTab]);

  const fetchIdentity = async () => {
    setLoadingIdentity(true);
    try {
        const token = localStorage.getItem('widget_os_token');
        const res = await fetch('/api/v1/identity/profile', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
            const data = await res.json();
            setIdentityData(data);
        }
    } catch (e) {
        console.error("Failed to fetch identity", e);
    } finally {
        setLoadingIdentity(false);
    }
  };

  const handleReconcile = async () => {
      // Optimistic update or show loading
      const token = localStorage.getItem('token');
      try {
          const res = await fetch('/api/v1/identity/reconcile', {
              method: 'POST',
              headers: { 'Authorization': `Bearer ${token}` }
          });
          if (res.ok) {
              const result = await res.json();
              setIdentityData(result.data);
          }
      } catch (e) {
          console.error("Reconciliation failed", e);
      }
  };

  const tabs = [
    { id: 'general', label: 'General', icon: <SettingsIcon size={18} /> },
    { id: 'billing', label: 'Billing', icon: <CreditCard size={18} /> },
    { id: 'identity', label: 'Identity & Compliance', icon: <ShieldCheck size={18} /> },
    { id: 'theme', label: 'Theme (Beta)', icon: <Palette size={18} /> },
    { id: 'profile', label: 'Profile', icon: <User size={18} /> },
  ];

  return (
    <div className="settings-page p-6">
      <div className="settings-header mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Workspace Settings</h1>
        <p className="text-gray-400">Manage your account, preferences, and billing.</p>
      </div>

      <div className="settings-layout">
        <aside className="settings-sidebar">
          {tabs.map(tab => (
            <button
              key={tab.id}
              className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              {tab.icon}
              {tab.label}
            </button>
          ))}
        </aside>

        <main className="settings-content">
          {activeTab === 'general' && (
            <div className="glass card p-8 text-center text-gray-400">
              General configuration coming soon...
            </div>
          )}
          
          {activeTab === 'billing' && <BillingDashboard />}

          {activeTab === 'identity' && (
            <div className="animate-fade-in">
                {loadingIdentity ? (
                    <div className="p-8 text-center text-white/50">Loading Identity Profile...</div>
                ) : (
                    <IdentityProfileCard 
                        profile={identityData?.profile} 
                        trustScore={identityData?.trust_score}
                        onRefresh={handleReconcile}
                    />
                )}
            </div>
          )}

          {activeTab === 'theme' && (
            <div className="glass card p-8 text-center text-gray-400">
              Interactive Theme Builder coming in Phase Group D.
            </div>
          )}

          {activeTab === 'profile' && (
            <div className="glass card p-8 text-center text-gray-400">
              User profile management coming soon...
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default Settings;
