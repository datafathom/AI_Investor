import React from 'react';
import { Shield, CheckCircle, AlertTriangle, User, MapPin, Mail } from 'lucide-react';
import KYCStatusBadge from './KYCStatusBadge';
import './IdentityProfileCard.css';

const IdentityProfileCard = ({ profile, trustScore, onRefresh }) => {
  if (!profile) return null;

  return (
    <div className="identity-profile-card glass-panel p-6 rounded-xl">
      <div className="flex justify-between items-start mb-6">
        <div>
            <h2 className="text-2xl font-bold flex items-center gap-2">
                <Shield className="w-6 h-6 text-cyan-400" />
                Unified Identity Profile
            </h2>
            <p className="text-white/60 text-sm mt-1">Reconciled "Golden Record" from linked providers</p>
        </div>
        <KYCStatusBadge status={profile.kyc_status} score={trustScore} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Golden Record Details */}
        <div className="space-y-4">
            <h3 className="text-lg font-semibold text-cyan-300 border-b border-white/10 pb-2">Verified Identity</h3>
            
            <div className="flex items-center gap-3">
                <User className="w-5 h-5 text-white/40" />
                <div>
                    <label className="text-xs text-white/40 block">Legal Name</label>
                    <span className="text-lg">{profile.legal_name || 'Not Verified'}</span>
                </div>
            </div>

            <div className="flex items-center gap-3">
                <Mail className="w-5 h-5 text-white/40" />
                <div>
                    <label className="text-xs text-white/40 block">Primary Email</label>
                    <span className="text-lg">{profile.email}</span>
                </div>
            </div>

            <div className="flex items-center gap-3">
                <MapPin className="w-5 h-5 text-white/40" />
                <div>
                    <label className="text-xs text-white/40 block">Verified Address</label>
                    <span className="text-lg">
                        {profile.address ? `${profile.address.street}, ${profile.address.city}` : 'Not Verified'}
                    </span>
                </div>
            </div>
        </div>

        {/* Trust Score & Actions */}
        <div className="bg-black/20 rounded-lg p-6 flex flex-col items-center justify-center text-center">
            <div className="relative w-32 h-32 flex items-center justify-center mb-4">
                <svg className="w-full h-full transform -rotate-90">
                    <circle cx="64" cy="64" r="60" stroke="#333" strokeWidth="8" fill="none" />
                    <circle cx="64" cy="64" r="60" stroke={trustScore > 70 ? "#10B981" : "#F59E0B"} strokeWidth="8" fill="none" strokeDasharray={377} strokeDashoffset={377 - (377 * trustScore) / 100} className="transition-all duration-1000 ease-out" />
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className="text-3xl font-bold">{trustScore}</span>
                    <span className="text-xs text-white/50">TRUST SCORE</span>
                </div>
            </div>
            
            <button 
                onClick={onRefresh}
                className="mt-2 text-sm bg-white/10 hover:bg-white/20 px-4 py-2 rounded-lg transition-colors flex items-center gap-2"
            >
                Refresh Identity
            </button>
        </div>
      </div>
    </div>
  );
};

export default IdentityProfileCard;
