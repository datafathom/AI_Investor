import React, { useState, useEffect } from 'react';
import apiClient from '../services/apiClient';
import { Target, Calendar, CheckSquare, Plus, ArrowRight, Save } from 'lucide-react';

const MissionPlanner = () => {
    const [missions, setMissions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [newMission, setNewMission] = useState({ title: '', deadline: '', priority: 'medium' });

    useEffect(() => {
        loadMissions();
    }, []);

    const loadMissions = async () => {
        try {
            const res = await apiClient.get('/missions');
            if (res.data.success) {
                setMissions(res.data.data);
            }
        } catch (e) {
            console.error("Failed to load missions", e);
        } finally {
            setLoading(false);
        }
    };

    const handleCreate = async () => {
        if (!newMission.title) return;
        try {
            await apiClient.post('/missions', newMission);
            setNewMission({ title: '', deadline: '', priority: 'medium' });
            loadMissions();
        } catch (e) {
            console.error("Failed to create mission", e);
        }
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Target className="text-purple-500" /> Mission Planner
                </h1>
                <p className="text-slate-500">Strategic Objectives & Milestones</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Create New Mission */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                        <Plus size={16} /> New Mission
                    </h3>
                    <div className="space-y-4">
                        <div>
                            <label className="block text-xs uppercase text-slate-500 mb-1">Mission Title</label>
                            <input 
                                value={newMission.title}
                                onChange={e => setNewMission({...newMission, title: e.target.value})}
                                className="w-full bg-slate-950 border border-slate-800 rounded p-2 text-sm text-white"
                                placeholder="e.g. Expand to Asian Markets"
                            />
                        </div>
                        <div>
                            <label className="block text-xs uppercase text-slate-500 mb-1">Target Deadline</label>
                            <input 
                                type="date"
                                value={newMission.deadline}
                                onChange={e => setNewMission({...newMission, deadline: e.target.value})}
                                className="w-full bg-slate-950 border border-slate-800 rounded p-2 text-sm text-white"
                            />
                        </div>
                        <div>
                            <label className="block text-xs uppercase text-slate-500 mb-1">Priority</label>
                            <select 
                                value={newMission.priority}
                                onChange={e => setNewMission({...newMission, priority: e.target.value})}
                                className="w-full bg-slate-950 border border-slate-800 rounded p-2 text-sm text-white"
                            >
                                <option value="low">Low</option>
                                <option value="medium">Medium</option>
                                <option value="high">High</option>
                                <option value="critical">Critical</option>
                            </select>
                        </div>
                        <button 
                            onClick={handleCreate}
                            className="w-full bg-purple-600 hover:bg-purple-500 text-white font-bold py-2 rounded transition-colors flex items-center justify-center gap-2"
                        >
                            <Save size={16} /> Create Plan
                        </button>
                    </div>
                </div>

                {/* Mission List */}
                <div className="md:col-span-2 space-y-4">
                    {loading ? (
                        <div className="text-center text-slate-500 py-8">Loading strategies...</div>
                    ) : missions.length === 0 ? (
                        <div className="text-center text-slate-500 py-8">No active missions. Start planning above.</div>
                    ) : (
                        missions.map(mission => (
                            <div key={mission.id} className="bg-slate-900 border border-slate-800 rounded-xl p-6 hover:border-purple-500/30 transition-colors">
                                <div className="flex justify-between items-start mb-4">
                                    <div>
                                        <h3 className="text-xl font-bold text-white mb-1">{mission.title}</h3>
                                        <div className="flex gap-3 text-xs text-slate-400">
                                            <span className={`px-2 py-0.5 rounded border ${mission.priority === 'critical' ? 'border-red-500 text-red-400' : 'border-slate-700'}`}>
                                                {mission.priority.toUpperCase()}
                                            </span>
                                            <span className="flex items-center gap-1">
                                                <Calendar size={12} /> {mission.deadline || 'No Deadline'}
                                            </span>
                                        </div>
                                    </div>
                                    <div className="text-right">
                                        <div className="text-2xl font-bold text-purle-400">{mission.progress}%</div>
                                        <div className="text-xs text-slate-500">COMPLETE</div>
                                    </div>
                                </div>

                                {/* Milestones */}
                                <div className="space-y-2 mb-4">
                                    {mission.milestones.map(ms => (
                                        <div key={ms.id} className="flex items-center gap-3 text-sm p-2 bg-slate-950 rounded border border-slate-800/50">
                                            <div className={`w-4 h-4 rounded-full border flex items-center justify-center ${ms.completed ? 'bg-green-500 border-green-500' : 'border-slate-600'}`}>
                                                {ms.completed && <CheckSquare size={10} className="text-black" />}
                                            </div>
                                            <span className={`${ms.completed ? 'text-slate-500 line-through' : 'text-slate-300'}`}>
                                                {ms.title}
                                            </span>
                                            <span className="ml-auto text-xs text-slate-600">{ms.target_date}</span>
                                        </div>
                                    ))}
                                </div>

                                <button className="text-xs flex items-center gap-1 text-purple-400 hover:text-purple-300 font-bold">
                                    MANAGE DETAILS <ArrowRight size={12} />
                                </button>
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    );
};

export default MissionPlanner;
