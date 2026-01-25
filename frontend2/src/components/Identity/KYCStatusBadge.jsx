import React from 'react';
import { CheckCircle, AlertCircle, XCircle } from 'lucide-react';

const KYCStatusBadge = ({ status, score }) => {
  const getStatusConfig = () => {
    switch (status?.toLowerCase()) {
      case 'verified':
        return { color: 'text-green-400', bg: 'bg-green-400/10', border: 'border-green-400/20', icon: CheckCircle, label: 'KYC Verified' };
      case 'pending':
        return { color: 'text-yellow-400', bg: 'bg-yellow-400/10', border: 'border-yellow-400/20', icon: AlertCircle, label: 'Verification Pending' };
      case 'failed':
        return { color: 'text-red-400', bg: 'bg-red-400/10', border: 'border-red-400/20', icon: XCircle, label: 'Verification Failed' };
      default:
        return { color: 'text-gray-400', bg: 'bg-gray-400/10', border: 'border-gray-400/20', icon: AlertCircle, label: 'Unknown Status' };
    }
  };

  const config = getStatusConfig();
  const Icon = config.icon;

  return (
    <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full border ${config.bg} ${config.border} ${config.color}`}>
      <Icon className="w-4 h-4" />
      <span className="text-sm font-semibold tracking-wide uppercase">{config.label}</span>
      {score !== undefined && <span className="ml-1 opacity-60">| {score}/100</span>}
    </div>
  );
};

export default KYCStatusBadge;
