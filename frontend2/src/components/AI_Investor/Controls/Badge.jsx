import React from 'react';

const Badge = ({ children, status = 'info', className = '' }) => {
    const styles = {
        success: 'bg-green-500/10 text-green-400 border-green-500/20',
        error: 'bg-red-500/10 text-red-400 border-red-500/20',
        warning: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
        info: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20',
        active: 'bg-purple-500/10 text-purple-400 border-purple-500/20 animate-pulse',
        bullish: 'bg-green-400/10 text-green-400 border-green-400/20'
    };

    return (
        <span className={`px-2 py-0.5 rounded text-[10px] font-mono border ${styles[status] || styles.info} ${className}`}>
            {children}
        </span>
    );
};

export default Badge;
