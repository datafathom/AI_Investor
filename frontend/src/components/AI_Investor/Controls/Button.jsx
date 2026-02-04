import React from 'react';

const Button = ({ children, variant = 'primary', className = '', ...props }) => {
    const variants = {
        primary: 'bg-cyan-500/10 border border-cyan-500 text-cyan-400 hover:bg-cyan-500/20 shadow-[0_0_10px_rgba(0,242,255,0.1)]',
        secondary: 'bg-purple-500/10 border border-purple-500 text-purple-400 hover:bg-purple-500/20 shadow-[0_0_10px_rgba(168,85,247,0.1)]',
        danger: 'bg-red-500/10 border border-red-500 text-red-400 hover:bg-red-500/20 shadow-[0_0_10px_rgba(239,68,68,0.1)]',
        ghost: 'bg-transparent border border-white/10 text-dim hover:border-white/30 hover:text-white',
    };

    return (
        <button
            className={`py-2 px-4 rounded font-bold transition-all duration-300 font-display ${variants[variant] || variants.primary} ${className}`}
            {...props}
        >
            {children}
        </button>
    );
};

export default Button;
