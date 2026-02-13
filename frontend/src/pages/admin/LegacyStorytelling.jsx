import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { BookOpen, Camera } from 'lucide-react';

const LegacyStorytelling = () => {
    const [history, setHistory] = useState(null);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/philanthropy/history/impact');
            if (res.data.success) setHistory(res.data.data);
        };
        load();
    }, []);

    if (!history) return <div>Loading History...</div>;

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <BookOpen className="text-indigo-500" /> Legacy & Storytelling
                </h1>
                <p className="text-slate-500">Your Philanthropic Journey & Impact History</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
                 <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center">
                    <div className="text-4xl font-bold text-white mb-2">{history.total_lives_touched}</div>
                    <div className="text-indigo-400 font-bold uppercase text-xs">Lives Touched</div>
                 </div>
                 <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center">
                    <div className="text-4xl font-bold text-white mb-2">{history.acres_preserved}</div>
                    <div className="text-emerald-400 font-bold uppercase text-xs">Acres Preserved</div>
                 </div>
                 <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center">
                    <div className="text-4xl font-bold text-white mb-2">Since 2023</div>
                    <div className="text-slate-500 font-bold uppercase text-xs">Giving Active</div>
                 </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-8">
                <h3 className="font-bold text-white mb-8 text-xl">Impact Timeline</h3>
                <div className="relative border-l-2 border-slate-800 ml-4 space-y-8 pl-8">
                    {history.timeline.map((item, i) => (
                        <div key={i} className="relative">
                            <div className="absolute -left-[42px] top-0 w-5 h-5 rounded-full bg-slate-950 border-4 border-indigo-500"></div>
                            <div className="text-2xl font-bold text-indigo-400 mb-1">{item.year}</div>
                            <h4 className="text-white font-bold text-lg">{item.event}</h4>
                            <p className="text-slate-400 mt-1">{item.impact}</p>
                        </div>
                    ))}
                </div>
            </div>
            
            <div className="mt-8 bg-slate-900 border border-slate-800 rounded-xl p-8 flex flex-col items-center justify-center text-center">
                <Camera size={48} className="text-slate-600 mb-4" />
                <h3 className="font-bold text-white">Impact Gallery</h3>
                <p className="text-slate-500 text-sm mt-2">Upload photos from site visits and charity events.</p>
                <button className="mt-4 bg-slate-800 hover:bg-slate-700 text-white px-4 py-2 rounded text-sm font-bold">
                    UPLOAD MEDIA
                </button>
            </div>
        </div>
    );
};

export default LegacyStorytelling;
