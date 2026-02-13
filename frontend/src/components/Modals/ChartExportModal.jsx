import React, { useState } from 'react';
import { X, Download, Share2, Link, FileImage, FileText } from 'lucide-react';
import { chartService } from '../../services/chartService';
import { toast } from 'sonner';

export const ChartExportModal = ({ isOpen, onClose }) => {
    const [loading, setLoading] = useState(false);
    const [shareLink, setShareLink] = useState(null);

    if (!isOpen) return null;

    const handleExport = async (format) => {
        setLoading(true);
        try {
            const res = await chartService.exportChart(format);
            toast.success(`Chart exported as ${format.toUpperCase()}`, {
                description: "Download started automatically."
            });
            // Mock download action
            console.log("Download URL:", res.url);
        } catch (e) {
            toast.error("Export failed");
        } finally {
            setLoading(false);
        }
    };

    const handleShare = async () => {
        setLoading(true);
        try {
            const res = await chartService.shareChart();
            setShareLink(res.link);
            toast.success("Share link created");
        } catch (e) {
            toast.error("Share failed");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
            <div className="bg-slate-900 border border-slate-800 rounded-xl w-96 p-6 shadow-2xl relative">
                <button 
                    onClick={onClose}
                    className="absolute top-4 right-4 text-slate-500 hover:text-white"
                >
                    <X size={20} />
                </button>

                <h2 className="text-lg font-bold text-white mb-6 flex items-center gap-2">
                    <Download size={20} className="text-cyan-400" /> Export & Share
                </h2>

                <div className="space-y-6">
                    <div>
                        <label className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3 block">Download Image</label>
                        <div className="grid grid-cols-3 gap-3">
                            <button 
                                onClick={() => handleExport('png')}
                                className="bg-slate-800 hover:bg-slate-700 p-3 rounded-lg flex flex-col items-center gap-2 transition-colors"
                            >
                                <FileImage size={24} className="text-emerald-400" />
                                <span className="text-xs font-bold text-slate-300">PNG</span>
                            </button>
                            <button 
                                onClick={() => handleExport('svg')}
                                className="bg-slate-800 hover:bg-slate-700 p-3 rounded-lg flex flex-col items-center gap-2 transition-colors"
                            >
                                <FileText size={24} className="text-orange-400" />
                                <span className="text-xs font-bold text-slate-300">SVG</span>
                            </button>
                            <button 
                                onClick={() => handleExport('pdf')}
                                className="bg-slate-800 hover:bg-slate-700 p-3 rounded-lg flex flex-col items-center gap-2 transition-colors"
                            >
                                <FileText size={24} className="text-red-400" />
                                <span className="text-xs font-bold text-slate-300">PDF</span>
                            </button>
                        </div>
                    </div>

                    <div className="border-t border-slate-800 pt-6">
                        <label className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3 block">Share Link</label>
                        {!shareLink ? (
                            <button 
                                onClick={handleShare}
                                disabled={loading}
                                className="w-full bg-cyan-600 hover:bg-cyan-500 text-white font-bold py-2 rounded-lg flex items-center justify-center gap-2 transition-colors"
                            >
                                {loading ? <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div> : <Share2 size={16} />}
                                Generate Share Link
                            </button>
                        ) : (
                            <div className="bg-slate-950 border border-slate-800 rounded p-2 flex items-center justify-between">
                                <span className="text-xs text-slate-400 truncate max-w-[200px]">{shareLink}</span>
                                <button 
                                    onClick={() => {
                                        navigator.clipboard.writeText(shareLink);
                                        toast.success("Copied to clipboard");
                                    }}
                                    className="text-cyan-400 hover:text-cyan-300 text-xs font-bold"
                                >
                                    Copy
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};
