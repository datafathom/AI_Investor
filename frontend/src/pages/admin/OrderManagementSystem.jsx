import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { ShoppingCart, Clock, AlertTriangle, CheckCircle, XCircle, Play, Pause, RefreshCw } from 'lucide-react';
import OrderPreviewModal from '../../components/Execution/OrderPreviewModal';

const OrderManagementSystem = () => {
    const [orders, setOrders] = useState([]);
    const [stats, setStats] = useState({ active: 0, filled: 0, cancelled: 0 });
    const [showPreview, setShowPreview] = useState(false);
    const [newOrder, setNewOrder] = useState({ ticker: '', side: 'BUY', qty: 100, type: 'LIMIT' });

    useEffect(() => {
        loadOrders();
        const interval = setInterval(loadOrders, 5000);
        return () => clearInterval(interval);
    }, []);

    const loadOrders = async () => {
        try {
            const res = await apiClient.get('/execution/orders');
            if (res.success) {
                setOrders(res.data);
                // Calculate stats
                const active = res.data.filter(o => ['QUEUED', 'PARTIAL', 'PENDING'].includes(o.status)).length;
                const filled = res.data.filter(o => o.status === 'FILLED').length;
                const cancelled = res.data.filter(o => o.status === 'CANCELLED').length;
                setStats({ active, filled, cancelled });
            }
        } catch (e) { console.error(e); }
    };

    const handleCancel = async (id) => {
        try {
            await apiClient.delete(`/execution/orders/${id}`);
            loadOrders();
        } catch (e) { console.error(e); }
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
             <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <ShoppingCart className="text-orange-500" /> Order Management
                    </h1>
                    <p className="text-slate-500">Execution Lifecycle & State Tracking</p>
                </div>
                <button 
                    onClick={() => setShowPreview(true)}
                    className="bg-orange-600 hover:bg-orange-500 text-white px-6 py-2 rounded font-bold transition-colors"
                >
                    + NEW ORDER
                </button>
            </header>

            {/* Stats Bar */}
            <div className="grid grid-cols-3 gap-6 mb-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-center justify-between">
                    <div>
                        <div className="text-slate-500 text-xs uppercase font-bold">Active Orders</div>
                        <div className="text-2xl font-bold text-blue-400">{stats.active}</div>
                    </div>
                    <Clock className="text-slate-700" />
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-center justify-between">
                    <div>
                        <div className="text-slate-500 text-xs uppercase font-bold">Filled Today</div>
                        <div className="text-2xl font-bold text-green-400">{stats.filled}</div>
                    </div>
                    <CheckCircle className="text-slate-700" />
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-center justify-between">
                    <div>
                        <div className="text-slate-500 text-xs uppercase font-bold">Cancelled</div>
                        <div className="text-2xl font-bold text-red-400">{stats.cancelled}</div>
                    </div>
                    <XCircle className="text-slate-700" />
                </div>
            </div>

            {/* Order Blotter */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <div className="p-4 border-b border-slate-800 flex justify-between items-center">
                    <h3 className="font-bold text-white">Order Blotter</h3>
                    <button onClick={loadOrders} className="text-slate-400 hover:text-white"><RefreshCw size={16} /></button>
                </div>
                <table className="w-full text-sm text-left">
                    <thead className="bg-slate-950 text-slate-500 uppercase text-xs">
                        <tr>
                            <th className="p-4">Time</th>
                            <th className="p-4">Ticker</th>
                            <th className="p-4">Side</th>
                            <th className="p-4">Type</th>
                            <th className="p-4 text-right">Qty</th>
                            <th className="p-4 text-right">Price</th>
                            <th className="p-4 text-center">Status</th>
                            <th className="p-4 text-right">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {orders.map(order => (
                            <tr key={order.id} className="border-t border-slate-800 hover:bg-slate-800/50">
                                <td className="p-4 font-mono text-slate-500 text-xs">{order.submitted_at.split('T')[1].split('.')[0]}</td>
                                <td className="p-4 font-bold text-white">{order.ticker}</td>
                                <td className={`p-4 font-bold ${order.side === 'BUY' ? 'text-green-400' : 'text-red-400'}`}>{order.side}</td>
                                <td className="p-4 text-slate-300">{order.type}</td>
                                <td className="p-4 font-mono text-right text-slate-200">{order.qty}</td>
                                <td className="p-4 font-mono text-right text-slate-200">{order.limit_price || 'MKT'}</td>
                                <td className="p-4 text-center">
                                    <span className={`px-2 py-1 rounded text-xs font-bold ${
                                        order.status === 'FILLED' ? 'bg-green-500/20 text-green-400' :
                                        order.status === 'CANCELLED' ? 'bg-red-500/20 text-red-400' :
                                        'bg-blue-500/20 text-blue-400'
                                    }`}>{order.status}</span>
                                </td>
                                <td className="p-4 text-right">
                                    {['QUEUED', 'PENDING'].includes(order.status) && (
                                        <button 
                                            onClick={() => handleCancel(order.id)}
                                            className="text-red-500 hover:text-red-400 text-xs font-bold border border-red-500/30 px-2 py-1 rounded"
                                        >
                                            CANCEL
                                        </button>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {showPreview && (
                <OrderPreviewModal 
                    onClose={() => setShowPreview(false)} 
                    onSuccess={() => { setShowPreview(false); loadOrders(); }}
                />
            )}
        </div>
    );
};

export default OrderManagementSystem;
