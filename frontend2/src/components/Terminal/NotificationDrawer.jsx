import React from 'react';
import { Bell, X, Info, AlertTriangle, CheckCircle, AlertOctagon } from 'lucide-react';
import './NotificationDrawer.css'; // Needs styling

const NotificationDrawer = ({ isOpen, onClose, notifications = [] }) => {
    // Mock notifications if none provided
    const displayNotifications = notifications.length > 0 ? notifications : [
        { id: 1, type: 'error', title: 'Connection Severed', message: 'Market data feed lost for 200ms.', time: '10:42:05' },
        { id: 2, type: 'warning', title: 'High Volatility', message: 'VIX spike detected (>25). Risk subsystem engaged.', time: '10:38:12' },
        { id: 3, type: 'success', title: 'Order Filled', message: 'Bought 100 SPY @ 450.20', time: '10:15:00' },
        { id: 4, type: 'info', title: 'System Update', message: 'Patch 2.4 installing in background.', time: '09:00:00' },
    ];

    const getIcon = (type) => {
        switch (type) {
            case 'error': return <AlertOctagon size={16} className="text-red-500" />;
            case 'warning': return <AlertTriangle size={16} className="text-amber-500" />;
            case 'success': return <CheckCircle size={16} className="text-green-500" />;
            default: return <Info size={16} className="text-blue-500" />;
        }
    };

    return (
        <>
            {/* Backdrop */}
            {isOpen && (
                <div
                    className="fixed inset-0 bg-black/20 backdrop-blur-[1px] z-[9990]"
                    onClick={onClose}
                />
            )}

            {/* Drawer */}
            <div className={`fixed top-0 right-0 h-full w-80 bg-[#0a0a0a] border-l border-slate-800 shadow-2xl z-[9995] transform transition-transform duration-300 ease-in-out ${isOpen ? 'translate-x-0' : 'translate-x-full'}`}>
                <div className="flex flex-col h-full">
                    <div className="p-4 border-b border-slate-800 flex justify-between items-center bg-slate-900/50">
                        <div className="flex items-center gap-2">
                            <Bell size={16} className="text-slate-200" />
                            <h2 className="font-bold text-sm text-white uppercase tracking-wider">System Log</h2>
                        </div>
                        <button onClick={onClose} className="text-slate-500 hover:text-white transition-colors">
                            <X size={18} />
                        </button>
                    </div>

                    <div className="flex-1 overflow-y-auto p-4 space-y-3">
                        {displayNotifications.map((note) => (
                            <div key={note.id} className="group relative pl-4 border-l-2 border-slate-700 hover:border-slate-500 transition-colors">
                                <div className="absolute -left-[5px] top-0 w-2 h-2 rounded-full bg-slate-900 border border-slate-700 group-hover:border-slate-400"></div>
                                <div className="bg-slate-900/30 p-3 rounded-r border border-slate-800/50 hover:bg-slate-800/50 transition-all hover:scale-[1.01] hover:border-cyan-500/50 shadow-lg">
                                    <div className="flex justify-between items-start mb-1">
                                        <div className="flex items-center gap-2 font-bold text-xs text-slate-200">
                                            {getIcon(note.type)}
                                            {note.title}
                                        </div>
                                        <span className="text-[10px] text-slate-600 font-mono">{note.time}</span>
                                    </div>
                                    <p className="text-xs text-slate-400 leading-relaxed">
                                        {note.message}
                                    </p>
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="p-4 border-t border-slate-800 bg-slate-900/30 text-center">
                        <button className="text-[10px] text-slate-500 hover:text-white uppercase font-bold tracking-widest transition-colors w-full py-2 border border-dashed border-slate-800 hover:border-slate-600 rounded">
                            Clear All History
                        </button>
                    </div>
                </div>
            </div>
        </>
    );
};

export default NotificationDrawer;
