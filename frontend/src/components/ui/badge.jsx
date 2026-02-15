import React from 'react';

const Badge = ({ children, variant = 'default', className = '', ...props }) => {
    const variants = {
        default: 'bg-slate-800 text-slate-100',
        secondary: 'bg-slate-700 text-slate-300',
        destructive: 'bg-red-900/50 text-red-400 border border-red-900/50',
        outline: 'text-slate-400 border border-slate-800',
        success: 'bg-green-900/50 text-green-400 border border-green-900/50',
    };

    return (
        <div
            className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 ${variants[variant] || variants.default} ${className}`}
            {...props}
        >
            {children}
        </div>
    );
};

export { Badge };
export default Badge;
