import React from 'react';
import { X, Copy, Mail, Globe } from 'lucide-react';

const ShareWatchlistModal = ({ isOpen, onClose, watchlistName = "Tech Giants" }) => {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50">
            <div className="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-md p-6">
                <div className="flex justify-between items-center mb-6">
                    <h3 className="text-xl font-bold text-white">Share "{watchlistName}"</h3>
                    <button onClick={onClose} className="text-slate-500 hover:text-white"><X size={20} /></button>
                </div>

                <div className="space-y-6">
                    <div>
                        <label className="block text-xs uppercase text-slate-500 mb-2">Public Link</label>
                        <div className="flex gap-2">
                            <input 
                                readOnly 
                                value="https://app.invstr.com/w/xf92k" 
                                className="bg-slate-950 border border-slate-700 rounded p-2 text-slate-400 flex-1 text-sm font-mono"
                            />
                            <button className="bg-slate-800 hover:bg-slate-700 text-white p-2 rounded">
                                <Copy size={16} />
                            </button>
                        </div>
                        <div className="flex items-center gap-2 mt-2 text-xs text-green-400">
                            <Globe size={12} /> Public access enabled
                        </div>
                    </div>

                    <div>
                        <label className="block text-xs uppercase text-slate-500 mb-2">Invite Collaborators</label>
                        <div className="flex gap-2">
                            <input 
                                placeholder="colleague@fund.com" 
                                className="bg-slate-950 border border-slate-700 rounded p-2 text-white flex-1"
                            />
                            <button className="bg-blue-600 hover:bg-blue-500 text-white px-4 rounded font-bold text-sm">
                                INVITE
                            </button>
                        </div>
                    </div>

                    <div className="border-t border-slate-800 pt-4">
                        <div className="space-y-3">
                            <div className="flex justify-between items-center">
                                <div className="flex items-center gap-3">
                                    <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center font-bold text-white text-xs">JD</div>
                                    <div>
                                        <div className="text-white text-sm font-bold">John Doe</div>
                                        <div className="text-slate-500 text-xs">Owner</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ShareWatchlistModal;
