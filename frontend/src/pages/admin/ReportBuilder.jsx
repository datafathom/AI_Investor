import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { FileDown, Layout, Printer } from 'lucide-react';

const ReportBuilder = () => {
    const [templates, setTemplates] = useState([]);
    const [selectedTemplate, setSelectedTemplate] = useState('');

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/reporting/templates');
            if (res.data.success) {
                setTemplates(res.data.data);
                if(res.data.data.length > 0) setSelectedTemplate(res.data.data[0].id);
            }
        };
        load();
    }, []);

    const generate = async () => {
        const res = await apiClient.post('/reporting/generate-pdf', null, { params: { template_id: selectedTemplate } });
        if (res.data.success) {
            alert(`PDF Generation Started (ETA: ${res.data.data.eta})`);
        }
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Printer className="text-slate-400" /> Professional Report Builder
                </h1>
                <p className="text-slate-500">Custom PDF Generation & Branding</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 h-fit">
                    <h3 className="font-bold text-white mb-6">Select Template</h3>
                    <div className="space-y-2">
                        {templates.map(t => (
                            <div 
                                key={t.id} 
                                onClick={() => setSelectedTemplate(t.id)}
                                className={`p-4 rounded border cursor-pointer transition-colors ${selectedTemplate === t.id ? 'bg-blue-600/20 border-blue-500' : 'bg-slate-950 border-slate-800 hover:border-slate-600'}`}
                            >
                                <div className="font-bold text-white">{t.name}</div>
                                <div className="text-xs text-slate-500 mt-1">{t.sections.join(', ')}</div>
                            </div>
                        ))}
                    </div>
                    
                    <button 
                        onClick={generate}
                        className="w-full mt-6 bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 rounded flex justify-center items-center gap-2"
                    >
                        <FileDown size={18} /> DOWNLOAD PDF
                    </button>
                </div>

                <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-8 flex flex-col items-center justify-center text-slate-500 min-h-[400px]">
                    <Layout size={64} className="mb-4 opacity-20" />
                    <p className="text-lg">Drag & Drop Layout Editor Placeholder</p>
                    <p className="text-sm mt-2">Customize sections, add custom charts, and upload logo here.</p>
                </div>
            </div>
        </div>
    );
};

export default ReportBuilder;
