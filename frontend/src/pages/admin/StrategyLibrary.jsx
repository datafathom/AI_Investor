import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { BookOpen, Copy, Code } from 'lucide-react';

const StrategyLibrary = () => {
    const [templates, setTemplates] = useState([]);
    const [selected, setSelected] = useState(null);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/strategy/templates');
            if (res.data.success) setTemplates(res.data.data);
        };
        load();
    }, []);

    const loadCode = async (id) => {
        const res = await apiClient.get(`/strategy/templates/${id}`);
        if (res.data.success) setSelected(res.data.data);
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <BookOpen className="text-orange-500" /> Strategy Library
                </h1>
                <p className="text-slate-500">Pre-built Templates & Community Algorithms</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="space-y-4">
                    {templates.map(t => (
                        <div 
                            key={t.id} 
                            onClick={() => loadCode(t.id)}
                            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-orange-500 transition-colors"
                        >
                            <div className="flex justify-between items-start mb-2">
                                <h3 className="font-bold text-white">{t.name}</h3>
                                <span className="bg-slate-800 text-xs px-2 py-1 rounded text-slate-300">{t.category}</span>
                            </div>
                            <div className="flex justify-between text-xs text-slate-500">
                                <span>Difficulty: <span className={t.difficulty === 'Hard' ? 'text-red-400' : 'text-green-400'}>{t.difficulty}</span></span>
                                <span>⭐ {t.rating}</span>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="lg:col-span-2 bg-slate-950 border border-slate-800 rounded-xl p-6 font-mono text-sm overflow-auto">
                    {selected ? (
                        <>
                            <div className="flex justify-between items-center mb-4 border-b border-slate-800 pb-4">
                                <span className="text-slate-400 italic">// {selected.docs}</span>
                                <button className="text-orange-500 hover:text-orange-400 flex items-center gap-1">
                                    <Copy size={14} /> CLONE
                                </button>
                            </div>
                            <pre className="text-green-400">{selected.code}</pre>
                        </>
                    ) : (
                        <div className="h-full flex items-center justify-center text-slate-600 flex-col gap-2">
                            <Code size={48} />
                            <p>Select a template to view source code.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default StrategyLibrary;
