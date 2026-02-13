import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Eye, Plus, Trash2, Share2, Tag } from 'lucide-react';

const WatchlistManager = () => {
    const [watchlists, setWatchlists] = useState([]);
    const [selectedId, setSelectedId] = useState(null);

    useEffect(() => {
        loadWatchlists();
    }, []);

    const loadWatchlists = async () => {
        try {
            const res = await apiClient.get('/watchlist/');
            if (res.data.success) {
                setWatchlists(res.data.data);
                if (res.data.data.length > 0 && !selectedId) {
                    setSelectedId(res.data.data[0].id);
                }
            }
        } catch (e) { console.error(e); }
    };

    const selectedWatchlist = watchlists.find(w => w.id === selectedId);

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <Eye className="text-blue-500" /> Watchlist Manager
                    </h1>
                    <p className="text-slate-500">Track & Monitor Key Assets</p>
                </div>
                <button className="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded font-bold flex items-center gap-2">
                    <Plus size={18} /> NEW LIST
                </button>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
                {/* Sidebar List */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 overflow-y-auto h-[600px]">
                    <h3 className="font-bold text-white mb-4 px-2">My Watchlists</h3>
                    <div className="space-y-2">
                        {watchlists.map(w => (
                            <div 
                                key={w.id} 
                                onClick={() => setSelectedId(w.id)}
                                className={`p-3 rounded cursor-pointer transition-colors ${
                                    selectedId === w.id ? 'bg-blue-600/20 border border-blue-600/40 text-white' : 'hover:bg-slate-800 text-slate-400'
                                }`}
                            >
                                <div className="font-bold">{w.name}</div>
                                <div className="text-xs opacity-70">{w.symbols.length} Assets</div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Main Content */}
                <div className="lg:col-span-3 bg-slate-900 border border-slate-800 rounded-xl p-6 h-[600px] overflow-y-auto">
                    {selectedWatchlist ? (
                        <>
                            <div className="flex justify-between items-center mb-6 border-b border-slate-800 pb-4">
                                <h2 className="text-2xl font-bold text-white">{selectedWatchlist.name}</h2>
                                <div className="flex gap-2">
                                    <button className="text-slate-400 hover:text-white p-2" title="Share">
                                        <Share2 size={20} />
                                    </button>
                                    <button className="text-red-400 hover:text-red-300 p-2" title="Delete">
                                        <Trash2 size={20} />
                                    </button>
                                </div>
                            </div>

                            <div className="flex gap-2 mb-6">
                                {selectedWatchlist.tags.map(tag => (
                                    <span key={tag} className="bg-slate-800 text-slate-300 px-2 py-1 rounded text-xs flex items-center gap-1 border border-slate-700">
                                        <Tag size={12} /> {tag}
                                    </span>
                                ))}
                            </div>

                            <table className="w-full text-left">
                                <thead className="text-slate-500 text-xs uppercase bg-slate-950">
                                    <tr>
                                        <th className="p-3">Symbol</th>
                                        <th className="p-3">Price</th>
                                        <th className="p-3">Change %</th>
                                        <th className="p-3">Volume</th>
                                    </tr>
                                </thead>
                                <tbody className="text-sm">
                                    {selectedWatchlist.symbols.map(sym => (
                                        <tr key={sym} className="border-b border-slate-800 hover:bg-slate-800/50">
                                            <td className="p-3 font-bold text-white font-mono">{sym}</td>
                                            <td className="p-3 text-slate-300">$150.00</td>
                                            <td className="p-3 text-green-400">+1.2%</td>
                                            <td className="p-3 text-slate-400">5.2M</td>
                                        </tr>
                                    ))}
                                    {selectedWatchlist.symbols.length === 0 && (
                                        <tr>
                                            <td colSpan="4" className="p-8 text-center text-slate-500">
                                                No symbols in this watchlist. Add some to get started.
                                            </td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </>
                    ) : (
                        <div className="h-full flex items-center justify-center text-slate-500">
                            Select a watchlist to view data.
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default WatchlistManager;
