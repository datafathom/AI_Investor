import React, { useState } from 'react';
import apiClient from '../../services/apiClient';
import { FileText, Download, Printer } from 'lucide-react';

const PerformanceReport = () => {
    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <FileText className="text-yellow-500" /> Performance Report
                    </h1>
                    <p className="text-slate-500">Comprehensive Strategy Analysis & Metrics</p>
                </div>
                <div className="flex gap-2">
                    <button className="bg-slate-800 hover:bg-slate-700 text-white px-4 py-2 rounded font-bold flex items-center gap-2">
                        <Printer size={16} /> PRINT
                    </button>
                    <button className="bg-slate-800 hover:bg-slate-700 text-white px-4 py-2 rounded font-bold flex items-center gap-2">
                        <Download size={16} /> PDF
                    </button>
                </div>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">CAGR</div>
                    <div className="text-3xl font-bold text-green-400">18.5%</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Sharpe</div>
                    <div className="text-3xl font-bold text-blue-400">1.92</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Max DD</div>
                    <div className="text-3xl font-bold text-red-400">-14.2%</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Win Rate</div>
                    <div className="text-3xl font-bold text-purple-400">62%</div>
                </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center text-slate-500">
                Detailed monthly returns heatmap and trade distribution charts will appear here.
            </div>
        </div>
    );
};

export default PerformanceReport;
