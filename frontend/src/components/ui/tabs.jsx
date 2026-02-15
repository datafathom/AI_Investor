import React from 'react';

const Tabs = ({ children, className = '', ...props }) => (
    <div className={`w-full ${className}`} {...props}>{children}</div>
);

const TabsList = ({ children, className = '', ...props }) => (
    <div className={`inline-flex h-10 items-center justify-center rounded-lg bg-slate-900 p-1 text-slate-400 ${className}`} {...props}>
        {children}
    </div>
);

const TabsTrigger = ({ children, className = '', value, ...props }) => (
    <button
        className={`inline-flex items-center justify-center whitespace-nowrap rounded-md px-3 py-1.5 text-sm font-medium ring-offset-white transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-400 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=active]:bg-slate-950 data-[state=active]:text-slate-50 data-[state=active]:shadow-sm ${className}`}
        data-state={props.active ? 'active' : 'inactive'}
        {...props}
    >
        {children}
    </button>
);

const TabsContent = ({ children, className = '', value, ...props }) => (
    <div className={`mt-2 ring-offset-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-400 focus-visible:ring-offset-2 ${className}`} {...props}>
        {children}
    </div>
);

export { Tabs, TabsList, TabsTrigger, TabsContent };
