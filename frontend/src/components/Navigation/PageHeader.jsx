
import React from 'react';
import './PageHeader.css';

/**
 * PageHeader Component
 * Standardized header for every route.
 * @param {React.ReactNode} icon - Lucide icon component
 * @param {string} title - Main page title
 * @param {string} subtitle - Descriptive tagline
 * @param {React.ReactNode} children - Optional right-side actions/stats
 */
const PageHeader = ({ icon, title, subtitle, children }) => {
    return (
        <header className="page-header-standard flex justify-between items-end border-b border-amber-500/20 pb-6 mb-8 mt-2">
            <div className="flex items-center gap-5">
                {icon && (
                    <div className="page-icon-wrapper p-3 bg-amber-500/10 rounded-xl border border-amber-500/20 shadow-glow-gold-sm">
                        {React.cloneElement(icon, { size: 28, className: "text-amber-400" })}
                    </div>
                )}
                <div>
                    <h1 className="text-3xl font-bold text-white tracking-tight flex items-center gap-2">
                        {title}
                    </h1>
                    {subtitle && (
                        <p className="text-slate-400 font-mono text-xs tracking-widest uppercase mt-1">
                            {subtitle}
                        </p>
                    )}
                </div>
            </div>
            {children && (
                <div className="header-actions-area flex gap-8">
                    {children}
                </div>
            )}
        </header>
    );
};

export default PageHeader;
