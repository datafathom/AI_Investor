
import React, { useState } from 'react';
import { Lock, AlertOctagon } from 'lucide-react';
import { motion } from 'framer-motion';

const FrozenOverlay = ({ isFrozen, onUnlock }) => {
    const [pin, setPin] = useState('');
    const [error, setError] = useState(false);

    if (!isFrozen) return null;

    const handleUnlock = (e) => {
        e.preventDefault();
        // Mock PIN check (would be backend validated in real app)
        if (pin === '123456') {
            onUnlock();
            setPin('');
            setError(false);
        } else {
            setError(true);
            setPin('');
        }
    };

    return (
        <div className="fixed inset-0 z-[9999] bg-red-950/90 backdrop-blur-md flex flex-col items-center justify-center text-white font-mono">
            <motion.div 
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                className="bg-black/40 p-12 rounded-xl border-2 border-red-500 shadow-[0_0_100px_rgba(220,38,38,0.5)] text-center max-w-lg w-full"
            >
                <AlertOctagon size={80} className="mx-auto text-red-500 mb-6 animate-pulse" />
                
                <h1 className="text-4xl font-bold tracking-widest text-red-500 mb-2">SYSTEM FROZEN</h1>
                <p className="text-red-300 mb-8 uppercase tracking-widest text-xs">Emergency Kill Switch Activated</p>

                <div className="bg-red-500/10 border border-red-500/30 p-4 rounded mb-8 text-left text-sm">
                    <p className="mb-2">⚠️ <strong className="text-red-400">STATUS REPORT:</strong></p>
                    <ul className="list-disc pl-5 space-y-1 text-red-300/80">
                        <li>All Agent Threads: <strong>HALTED</strong></li>
                        <li>Open Orders: <strong>CANCELLED</strong></li>
                        <li>Kafka Consumer: <strong>DISCONNECTED</strong></li>
                        <li>WebSocket Feed: <strong>TERMINATED</strong></li>
                    </ul>
                </div>

                <form onSubmit={handleUnlock} className="flex flex-col gap-4">
                    <div className="relative">
                        <input 
                            type="password" 
                            maxLength={6}
                            value={pin}
                            onChange={(e) => setPin(e.target.value)}
                            placeholder="ENTER 6-DIGIT OVERRIDE PIN"
                            className={`w-full bg-black/50 border ${error ? 'border-red-500 animate-shake' : 'border-red-900'} p-4 text-center text-2xl tracking-[1rem] outline-none focus:border-red-400 transition-colors rounded placeholder:text-red-900/50 placeholder:text-sm placeholder:tracking-normal`}
                            autoFocus
                        />
                        <Lock size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-red-700" />
                    </div>
                    
                    <button 
                        type="submit"
                        className="bg-red-600 hover:bg-red-500 text-white font-bold py-3 px-6 rounded transition-all shadow-lg shadow-red-900/50"
                    >
                        UNLOCK SYSTEM
                    </button>
                </form>
            </motion.div>
        </div>
    );
};

export default FrozenOverlay;
