import React from 'react';

const Card = ({ className = '', ...props }) => (
  <div className={`rounded-xl border border-slate-800 bg-slate-950 text-slate-50 shadow-sm ${className}`} {...props} />
);

const CardHeader = ({ className = '', ...props }) => (
  <div className={`flex flex-col space-y-1.5 p-6 ${className}`} {...props} />
);

const CardTitle = ({ className = '', ...props }) => (
  <h3 className={`font-semibold leading-none tracking-tight ${className}`} {...props} />
);

const CardDescription = ({ className = '', ...props }) => (
  <p className={`text-sm text-slate-400 ${className}`} {...props} />
);

const CardContent = ({ className = '', ...props }) => (
  <div className={`p-6 pt-0 ${className}`} {...props} />
);

const CardFooter = ({ className = '', ...props }) => (
  <div className={`flex items-center p-6 pt-0 ${className}`} {...props} />
);

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent };
