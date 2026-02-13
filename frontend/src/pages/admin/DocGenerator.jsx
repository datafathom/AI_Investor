import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { FileText, PenTool, Download } from 'lucide-react';

const DocGenerator = () => {
    const [templates, setTemplates] = useState([]);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/legal/templates');
            if (res.data.success) setTemplates(res.data.data);
        };
        load();
    }, []);

    const generate = async (id) => {
        // Mock generation
        console.log("Generating doc from template:", id);
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <PenTool className="text-pink-500" /> Legal Document Generator
                </h1>
                <p className="text-slate-500">Automated Contract & Agreement Creation</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 h-[600px] overflow-y-auto">
                    <h3 className="font-bold text-white mb-4 px-2">Templates</h3>
                    <div className="space-y-2">
                        {templates.map(t => (
                            <div key={t.id} className="p-3 rounded hover:bg-slate-800 cursor-pointer transition-colors text-slate-300">
                                <div className="font-bold">{t.name}</div>
                                <div className="text-xs opacity-70">{t.category}</div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="lg:col-span-3 bg-slate-900 border border-slate-800 rounded-xl p-8 flex flex-col items-center justify-center text-slate-500">
                    <FileText size={48} className="mb-4 opacity-50" />
                    <p>Select a template to start drafting a new legal document.</p>
                </div>
            </div>
        </div>
    );
};

export default DocGenerator;
