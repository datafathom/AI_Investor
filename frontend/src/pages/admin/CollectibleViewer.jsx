import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Gem, TrendingUp, TrendingDown } from 'lucide-react';

const CollectibleViewer = () => {
    const [items, setItems] = useState([]);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/assets/collectibles/prices');
            if (res.data.success) setItems(res.data.data);
        };
        load();
    }, []);

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Gem className="text-pink-500" /> Collectibles Viewer
                </h1>
                <p className="text-slate-500">Fine Art, Watches & Rare Assets</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {items.map((item, i) => (
                    <div key={i} className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                        <div className="flex justify-between items-start mb-4">
                            <h3 className="text-xl font-bold text-white">{item.item}</h3>
                            {item.trend === 'UP' ? <TrendingUp className="text-emerald-500" /> : <TrendingDown className="text-red-500" />}
                        </div>
                        
                        <div className="mb-6">
                            <div className="text-xs uppercase text-slate-500 font-bold mb-1">Last Auction Price</div>
                            <div className="text-2xl font-bold text-white">${item.last_auction.toLocaleString()}</div>
                            <div className="text-xs text-slate-500 mt-1">at {item.venue}</div>
                        </div>

                        <div className="flex gap-2">
                             <span className="bg-slate-800 text-slate-300 px-2 py-1 rounded text-xs font-bold">INSURED</span>
                             <span className="bg-slate-800 text-slate-300 px-2 py-1 rounded text-xs font-bold">VERIFIED</span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default CollectibleViewer;
