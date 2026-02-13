import React, { useState } from 'react';
import apiClient from '../../services/apiClient';
import { RefreshCw, CheckCircle, Clock } from 'lucide-react';

const TransactionSync = () => {
    const [status, setStatus] = useState('IDLE');
    const [logs, setLogs] = useState([
        { time: '10:00:00', msg: 'Sync completed successfully.', type: 'SUCCESS' },
        { time: '09:00:00', msg: 'Sync started.', type: 'INFO' }
    ]);

    const handleSync = async () => {
        setStatus('SYNCING');
        try {
            await apiClient.post('/brokerage/sync');
            setTimeout(() => {
                setStatus('COMPLETED');
                setLogs([{ time: new Date().toLocaleTimeString(), msg: 'Manual sync completed.', type: 'SUCCESS' }, ...logs]);
            }, 2000);
        } catch (e) {
            setStatus('ERROR');
        }
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
             <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <RefreshCw className={`text-orange-500 ${status === 'SYNCING' ? 'animate-spin' : ''}`} /> Transaction Sync
                </h1>
                <p className="text-slate-500">Reconcile Trades & Ledger Entries</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 flex flex-col items-center justify-center text-center">
                    <div className={`w-24 h-24 rounded-full flex items-center justify-center text-4xl mb-6 ${
                        status === 'SYNCING' ? 'bg-orange-500/20 text-orange-400 animate-pulse' :
                        status === 'COMPLETED' ? 'bg-green-500/20 text-green-400' :
                        'bg-slate-800 text-slate-400'
                    }`}>
                        {status === 'SYNCING' ? <RefreshCw size={40} className="animate-spin" /> : 
                         status === 'COMPLETED' ? <CheckCircle size={40} /> : <Clock size={40} />}
                    </div>
                    <h2 className="text-2xl font-bold text-white mb-2">{status}</h2>
                    <p className="text-slate-500 mb-8 max-w-sm">
                        Synchronize trades, dividends, and transfers across all connected brokerage accounts.
                    </p>
                    <button 
                        onClick={handleSync}
                        disabled={status === 'SYNCING'}
                        className="bg-orange-600 hover:bg-orange-500 text-white px-8 py-3 rounded-full font-bold transition-all transform hover:scale-105"
                    >
                        {status === 'SYNCING' ? 'SYNCING...' : 'START SYNC NOW'}
                    </button>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                    <div className="p-4 bg-slate-950 font-bold text-white border-b border-slate-800">Sync History</div>
                    <div className="max-h-[300px] overflow-y-auto">
                        {logs.map((log, i) => (
                            <div key={i} className="p-4 border-b border-slate-800 flex justify-between items-center text-sm">
                                <span className="font-mono text-slate-500">{log.time}</span>
                                <span className={log.type === 'SUCCESS' ? 'text-green-400' : 'text-slate-300'}>{log.msg}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TransactionSync;
