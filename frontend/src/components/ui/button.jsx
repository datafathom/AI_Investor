import React from 'react';

const Button = ({ children, variant = 'primary', className = '', ...props }) => {
    const variants = {
        primary: 'bg-indigo-600 hover:bg-indigo-700 text-white',
        secondary: 'bg-slate-800 hover:bg-slate-700 text-slate-100',
        outline: 'border border-slate-700 hover:bg-slate-800 text-slate-300',
        ghost: 'hover:bg-slate-800 text-slate-400 hover:text-slate-100',
        destructive: 'bg-red-600 hover:bg-red-700 text-white',
    };

    return (
        <button
            className={`inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-slate-400 disabled:pointer-events-none disabled:opacity-50 ${variants[variant] || variants.outline} ${className}`}
            {...props}
        >
            {children}
        </button>
    );
};

export { Button };
export default Button;
