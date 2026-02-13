import React, { useState } from 'react';
import apiClient from '../../services/apiClient';
import { X, Check, AlertTriangle, ArrowRight } from 'lucide-react';

const OrderPreviewModal = ({ onClose, onSuccess }) => {
    const [details, setDetails] = useState({ ticker: 'AAPL', side: 'BUY', qty: 100, type: 'LIMIT', limit_price: 150.00 });
    const [preview, setPreview] = useState(null);
    const [loading, setLoading] = useState(false);

    const handlePreview = async () => {
        setLoading(true);
        try {
            const res = await apiClient.post('/execution/orders/preview', details);
            if (res.data.success) {
                setPreview(res.data.data);
            }
        } catch (e) { console.error(e); } 
        finally { setLoading(false); }
    };

    const handleSubmit = async () => {
        try {
            await apiClient.post('/execution/orders', details);
            onSuccess();
        } catch (e) { console.error(e); }
    };

    return (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 backdrop-blur-sm">
            <div className="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-md overflow-hidden shadow-2xl">
                <div className="p-4 border-b border-slate-800 flex justify-between items-center bg-slate-950">
                    <h3 className="text-white font-bold">New Order Entry</h3>
                    <button onClick={onClose} className="text-slate-500 hover:text-white"><X size={20} /></button>
                </div>
                
                <div className="p-6 space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-xs uppercase text-slate-500 mb-1">Ticker</label>
                            <input 
                                value={details.ticker} 
                                onChange={e => setDetails({...details, ticker: e.target.value.toUpperCase()})}
                                className="w-full bg-slate-950 border border-slate-800 rounded p-2 text-white font-mono"
                            />
                        </div>
                        <div>
                            <label className="block text-xs uppercase text-slate-500 mb-1">Side</label>
                            <select 
                                value={details.side}
                                onChange={e => setDetails({...details, side: e.target.value})} 
                                className={`w-full bg-slate-950 border border-slate-800 rounded p-2 font-bold ${details.side === 'BUY' ? 'text-green-500' : 'text-red-500'}`}
                            >
                                <option value="BUY">BUY</option>
                                <option value="SELL">SELL</option>
                            </select>
                        </div>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-xs uppercase text-slate-500 mb-1">Quantity</label>
                            <input 
                                type="number"
                                value={details.qty}
                                onChange={e => setDetails({...details, qty: parseInt(e.target.value)})}
                                className="w-full bg-slate-950 border border-slate-800 rounded p-2 text-white font-mono"
                            />
                        </div>
                        <div>
                             <label className="block text-xs uppercase text-slate-500 mb-1">Price</label>
                            <input 
                                type="number"
                                value={details.limit_price}
                                onChange={e => setDetails({...details, limit_price: parseFloat(e.target.value)})}
                                className="w-full bg-slate-950 border border-slate-800 rounded p-2 text-white font-mono"
                            />
                        </div>
                    </div>

                    {!preview ? (
                        <button 
                            onClick={handlePreview}
                            disabled={loading}
                            className="w-full bg-slate-800 hover:bg-slate-700 text-white font-bold py-3 rounded mt-4"
                        >
                            {loading ? 'CALCULATING...' : 'PREVIEW ORDER'}
                        </button>
                    ) : (
                        <div className="bg-slate-950 rounded p-4 mt-4 border border-slate-800 animate-fade-in">
                            <div className="flex justify-between mb-2 text-sm">
                                <span className="text-slate-500">Notional</span>
                                <span className="text-white font-mono">${preview.notional.toLocaleString()}</span>
                            </div>
                            <div className="flex justify-between mb-2 text-sm">
                                <span className="text-slate-500">Comm + Fees</span>
                                <span className="text-white font-mono">${preview.commission.toFixed(2)}</span>
                            </div>
                            <div className="flex justify-between mb-2 text-sm">
                                <span className="text-slate-500">Slippage Est.</span>
                                <span className="text-orange-400 font-mono">{(preview.slippage_estimate * 100).toFixed(2)}%</span>
                            </div>
                            <div className="mt-4 pt-4 border-t border-slate-800">
                                <button 
                                    onClick={handleSubmit}
                                    className="w-full bg-green-600 hover:bg-green-500 text-white font-bold py-3 rounded flex items-center justify-center gap-2"
                                >
                                    <Check size={18} /> CONFIRM SUBMISSION
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default OrderPreviewModal;
