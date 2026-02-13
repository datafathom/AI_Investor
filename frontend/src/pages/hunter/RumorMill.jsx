import React, { useState, useEffect } from 'react';
import { newsService } from '../../services/newsService';
import RumorCard from '../../components/cards/RumorCard';
import { toast } from 'sonner';
import { Ear, Filter, AlertTriangle } from 'lucide-react';

const RumorMill = () => {
    const [rumors, setRumors] = useState([]);
    const [loading, setLoading] = useState(true);

    const loadRumors = async () => {
        try {
            setLoading(true);
            const data = await newsService.getRumors();
            setRumors(data);
        } catch (e) {
            toast.error("Failed to load rumors");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadRumors();
    }, []);

    const handleVote = async (id, type) => {
        try {
            await newsService.voteRumor(id, type);
            // Optimistic update or reload
            loadRumors();
            toast.success(`Voted ${type}`);
        } catch (e) {
            toast.error("Failed to cast vote");
        }
    };

    return (
        <div className="p-6 h-full flex flex-col bg-slate-950 text-slate-200 overflow-y-auto">
            {/* Header */}
             <div className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                        <Ear className="text-amber-500" /> Rumor Mill
                    </h1>
                    <p className="text-slate-400 mt-2">Unverified market intelligence and whispers.</p>
                </div>
                
                <div className="bg-amber-500/10 border border-amber-500/20 px-4 py-2 rounded-lg flex items-center gap-2 text-amber-500 text-sm">
                    <AlertTriangle size={16} />
                    <span>Information is unverified. Trade with caution.</span>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {rumors.map(rumor => (
                    <RumorCard key={rumor.id} rumor={rumor} onVote={handleVote} />
                ))}
            </div>
            
            {rumors.length === 0 && !loading && (
                 <div className="text-center py-20 text-slate-500">
                    No rumors currently circulating.
                </div>
            )}
        </div>
    );
};

export default RumorMill;
