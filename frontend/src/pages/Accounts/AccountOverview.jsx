import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Shield, User, Lock, Settings, Key, Cpu, Bell, Globe, 
  Activity, Award, Eye, EyeOff, Save, RotateCcw,
  Fingerprint, ShieldAlert, Zap
} from 'lucide-react';
import { authService } from '../../utils/authService';
import './AccountOverview.css';

const AccountOverview = () => {
  const [currentUser] = useState(authService.getCurrentUser());
  const [avatar, setAvatar] = useState(currentUser?.avatar || null);
  const [isModified, setIsModified] = useState(false);
  const [showSensitive, setShowSensitive] = useState(false);
  const [flickerActive, setFlickerActive] = useState(false);

  // Mock data for high-density feel
  const [accountData, setAccountData] = useState({
    fullName: currentUser?.username || 'Institutional Manager',
    email: currentUser?.email || 'admin@ai-investor.internal',
    pgpKey: '0x7F2A...4B9D',
    mfaStatus: 'Active (TOTP + YubiKey)',
    passRotation: '2026-03-15',
    clearance: 'Tier 1 - Unrestricted',
    tradingLimit: '$10,000,000 / Day',
    kycStatus: 'Verified (L3)',
    ipAddress: '192.168.1.104',
    vpnStatus: 'Integrated (AES-256)',
    fingerprint: '3a1e...f8c2',
    notifications: {
      webhooks: true,
      sms: false,
      email: true
    }
  });

  const triggerFlicker = () => {
    setFlickerActive(true);
    setTimeout(() => setFlickerActive(false), 400);
  };

  const handleAvatarChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64 = reader.result;
        setAvatar(base64);
        
        // Sync with StorageService
        const updatedUser = { ...currentUser, avatar: base64 };
        authService.setSession(authService.getToken(), updatedUser);
        
        // Trigger a global event or refresh to update MenuBar
        window.dispatchEvent(new Event('user-profile-update'));
        triggerFlicker();
        setIsModified(true);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleChange = (field, value) => {
    setAccountData(prev => ({ ...prev, [field]: value }));
    setIsModified(true);
    triggerFlicker();
  };

  const handleToggleNotify = (key) => {
    setAccountData(prev => ({
      ...prev,
      notifications: { ...prev.notifications, [key]: !prev.notifications[key] }
    }));
    setIsModified(true);
    triggerFlicker();
  };

  // Animation variants
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1 }
  };

  return (
    <div className="account-dashboard">
      {/* Hero Header */}
      <motion.header 
        className="account-hero-header"
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
      >
        <div className="hero-left-section flex items-center gap-8">
          <div className="profile-avatar-container relative group">
            <div className="profile-avatar-mask w-32 h-32 rounded-full border-2 border-cyan-500 overflow-hidden relative shadow-lg shadow-cyan-500/20">
              {avatar ? (
                <img src={avatar} alt="Avatar" className="w-full h-full object-cover" />
              ) : (
                <div className="w-full h-full bg-slate-800 flex items-center justify-center">
                  <User size={48} className="text-slate-600" />
                </div>
              )}
              
              {/* Hover Overlay */}
              <div className="profile-avatar-overlay absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 flex flex-col items-center justify-center transition-all duration-300 cursor-pointer">
                <Zap size={20} className="text-cyan-400 mb-1" />
                <span className="text-[10px] font-bold uppercase tracking-tighter text-white">Change Node</span>
              </div>
              
              <input 
                type="file" 
                className="absolute inset-0 opacity-0 cursor-pointer z-10" 
                accept="image/*"
                onChange={handleAvatarChange}
                title="Change Profile Avatar"
              />
            </div>
          </div>

          <div className="hero-title-group">
            <div className="flex items-center gap-4 mb-2">
              <h1 className="text-4xl font-black tracking-tighter">Account Overview</h1>
              <span className="hero-version-tag">V3.2.0-STABLE</span>
            </div>
            <div className="flex flex-col gap-1">
              <span className="clearance-badge font-mono" style={{ color: 'var(--color-system-green)' }}>
                CLEARANCE LEVEL: {accountData.clearance}
              </span>
              <span className="text-[10px] text-zinc-500 font-mono tracking-widest uppercase">
                Institutional ID: {currentUser?.id || 'AUTH-8821-X'}
              </span>
            </div>
          </div>
        </div>

        <div className="top-glimpses">
          <div className="glimpse-widget">
            <div style={{ position: 'relative', width: 40, height: 40 }}>
               {/* Simplified Radial Meter */}
               <svg viewBox="0 0 36 36" style={{ transform: 'rotate(-90deg)' }}>
                  <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#222" strokeWidth="3" />
                  <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="var(--color-system-green)" strokeWidth="3" strokeDasharray="98, 100" />
               </svg>
               <span style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 10, fontWeight: 800 }}>98%</span>
            </div>
            <div>
              <span className="glimpse-label">Security Score</span>
              <span className="glimpse-value">Robust</span>
            </div>
          </div>

          <div className="glimpse-widget">
            <Activity className="text-cyan-400" size={20} />
            <div>
              <span className="glimpse-label">Session Health</span>
              <span className="glimpse-value">
                <span className="status-pulse"></span> Active
              </span>
            </div>
          </div>

          <div className="glimpse-widget">
            <Award className="tier-glow" size={20} />
            <div>
              <span className="glimpse-label">Tier Status</span>
              <span className="glimpse-value tier-glow">INSTITUTIONAL</span>
            </div>
          </div>
        </div>
      </motion.header>

      {/* Bento Grid */}
      <motion.div 
        className="bento-grid"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* Identity Management */}
        <motion.div className="bento-card" variants={itemVariants}>
          <div className="card-header">
            <User className="card-icon" size={18} />
            <h3>Identity Management</h3>
          </div>
          <div className="space-y-4">
             <div className="flex flex-col">
                <span className="text-[10px] text-slate-500 uppercase font-bold">Verified Name</span>
                <span className={`text-sm ${flickerActive ? 'flicker-active' : ''}`}>{accountData.fullName}</span>
             </div>
             <div className="flex flex-col">
                <span className="text-[10px] text-slate-500 uppercase font-bold">Institutional Email</span>
                <span className="text-sm">{accountData.email}</span>
             </div>
             <div className="flex flex-col">
                <span className="text-[10px] text-slate-500 uppercase font-bold">PGP Fingerprint</span>
                <span className={`text-sm font-mono redacted ${showSensitive ? 'unredacted' : ''}`} onClick={() => setShowSensitive(!showSensitive)}>
                  {accountData.pgpKey}
                </span>
             </div>
          </div>
        </motion.div>

        {/* Security & Auth */}
        <motion.div className="bento-card" variants={itemVariants}>
          <div className="card-header">
            <Lock className="card-icon" size={18} />
            <h3>Security & Auth</h3>
          </div>
          <div className="space-y-4">
             <div className="flex justify-between items-center bg-white/5 p-3 rounded-lg border border-white/5">
                <div className="flex flex-col">
                  <span className="text-xs font-bold">MFA Status</span>
                  <span className="text-[10px] text-green-400">{accountData.mfaStatus}</span>
                </div>
                <Shield className="text-green-500" size={16} />
             </div>
             <div className="flex flex-col">
                <span className="text-[10px] text-slate-500 uppercase font-bold">Next Password Rotation</span>
                <span className="text-sm font-mono">{accountData.passRotation}</span>
             </div>
             <button className="w-full bg-white/10 hover:bg-white/20 transition-all border border-white/10 p-2 rounded text-[10px] font-bold tracking-widest uppercase">
                Manage Hardware Keys
             </button>
          </div>
        </motion.div>

        {/* Institutional Clearance */}
        <motion.div className="bento-card" variants={itemVariants}>
          <div className="card-header">
            <Award className="card-icon" size={18} />
            <h3>Institutional Clearance</h3>
          </div>
          <div className="space-y-4">
             <div className="flex flex-col border-l-2 border-yellow-500 pl-3">
                <span className="text-[10px] text-slate-500 uppercase font-bold">Daily Trading Limit</span>
                <span className="text-lg font-bold text-yellow-400">{accountData.tradingLimit}</span>
             </div>
             <div className="flex justify-between">
                <div>
                  <span className="text-[10px] text-slate-500 uppercase font-bold block">KYC Level</span>
                  <span className="text-xs">Level 3 (Full Clearance)</span>
                </div>
                <div>
                  <span className="text-[10px] text-slate-500 uppercase font-bold block">Tax Residency</span>
                  <span className="text-xs">USA / Domestic</span>
                </div>
             </div>
          </div>
        </motion.div>

        {/* API Management */}
        <motion.div className="bento-card" variants={itemVariants}>
          <div className="card-header">
            <Key className="card-icon" size={18} />
            <h3>API Management</h3>
          </div>
          <div className="space-y-3">
             <div className="bg-black/40 p-3 rounded border border-white/5">
                <div className="flex justify-between mb-1">
                  <span className="text-[10px] font-bold">Production-Alpha-01</span>
                  <span className="text-[9px] bg-cyan-900/50 text-cyan-400 px-1 rounded">READ-ONLY</span>
                </div>
                <span className="font-mono text-[10px] redacted">sk_prod_771...4920k</span>
             </div>
             <div className="bg-black/40 p-3 rounded border border-white/5">
                <div className="flex justify-between mb-1">
                  <span className="text-[10px] font-bold">ExecutionGateway-X</span>
                  <span className="text-[9px] bg-red-900/50 text-red-400 px-1 rounded">EXECUTE</span>
                </div>
                <span className="font-mono text-[10px] redacted">sk_exec_902...1155x</span>
             </div>
             <button className="flex items-center justify-center gap-2 text-[10px] text-cyan-400 hover:text-cyan-300 font-bold w-full uppercase mt-2">
                <Zap size={10} /> Provision New Gateway
             </button>
          </div>
        </motion.div>

        {/* Hardware Environment */}
        <motion.div className="bento-card" variants={itemVariants}>
          <div className="card-header">
            <Cpu className="card-icon" size={18} />
            <h3>Hardware Environment</h3>
          </div>
          <div className="grid grid-cols-2 gap-3">
             <div className="flex flex-col bg-white/5 p-2 rounded">
                <span className="text-[9px] text-slate-500 uppercase font-bold">Session IP</span>
                <span className="text-xs font-mono">{accountData.ipAddress}</span>
             </div>
             <div className="flex flex-col bg-white/5 p-2 rounded">
                <span className="text-[9px] text-slate-500 uppercase font-bold">VPN Status</span>
                <span className="text-xs font-mono text-green-400">SECURE</span>
             </div>
             <div className="col-span-2 flex flex-col bg-white/5 p-2 rounded">
                <span className="text-[9px] text-slate-500 uppercase font-bold">Browser Fingerprint</span>
                <span className="text-[10px] font-mono truncate">{accountData.fingerprint}</span>
             </div>
             <div className="col-span-2 flex items-center gap-2 text-[9px] text-slate-400 border-t border-white/10 pt-2 mt-1">
                <ShieldAlert size={10} /> System Masking Active
             </div>
          </div>
        </motion.div>

        {/* Notification Node */}
        <motion.div className="bento-card" variants={itemVariants}>
          <div className="card-header">
            <Bell className="card-icon" size={18} />
            <h3>Notification Node</h3>
          </div>
          <div className="space-y-3">
             {Object.entries(accountData.notifications).map(([key, enabled]) => (
               <div key={key} className="flex justify-between items-center p-2 hover:bg-white/5 rounded transition-colors">
                  <span className="text-xs uppercase font-bold">{key} Alerts</span>
                  <button 
                    onClick={() => handleToggleNotify(key)}
                    className={`w-10 h-5 rounded-full relative transition-colors ${enabled ? 'bg-cyan-600' : 'bg-slate-700'}`}
                  >
                    <motion.div 
                      className="absolute top-1 left-1 w-3 h-3 bg-white rounded-full"
                      animate={{ x: enabled ? 20 : 0 }}
                    />
                  </button>
               </div>
             ))}
             <span className="text-[9px] text-slate-500 block mt-2 italic">* Encrypted delivery via PGP if enabled.</span>
          </div>
        </motion.div>
      </motion.div>

      {/* Breadcrumbs */}
      <div className="account-breadcrumbs">
        <span>Home</span> &gt; <span className="breadcrumb-secure">Account</span>
      </div>

      {/* Persistent Action Bar */}
      <AnimatePresence>
        {isModified && (
          <motion.div 
            className="action-bar-container"
            initial={{ y: 100 }}
            animate={{ y: 0 }}
            exit={{ y: 100 }}
          >
            <div className="action-bar">
              <span className="text-xs font-bold text-white flex items-center gap-2 mr-4 border-r border-white/20 pr-4">
                <Settings size={14} className="animate-spin-slow" /> UNSAVED CHANGES
              </span>
              <button 
                className="btn-discard" 
                onClick={() => {
                  setIsModified(false);
                  // In real app, revert data here
                }}
              >
                Discard
              </button>
              <button 
                className="btn-save flex items-center gap-2"
                onClick={() => {
                  setIsModified(false);
                  triggerFlicker();
                }}
              >
                <Save size={14} /> Save Changes
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default AccountOverview;
