import React, { useState, useEffect } from 'react';
import { analysisService } from '../../services/analysisService';
import { ScannerBuilder, ScanResultsTable } from '../../components/builders/ScannerBuilder';
import { toast } from 'sonner';
import { Filter, Database } from 'lucide-react';

const FundamentalScanner = () => {
    const [metrics, setMetrics] = useState([]);
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadMetrics();
    }, []);

    const loadMetrics = async () => {
        try {
            const data = await analysisService.getMetrics();
            setMetrics(data);
        } catch (e) {
            toast.error("Failed to load metrics");
        } finally {
            setLoading(false);
        }
    };

    const handleRunScan = async (criteria) => {
        try {
            const data = await analysisService.runScan(criteria);
            setResults(data);
            toast.success(`Found ${data.length} matches`);
        } catch (e) {
            toast.error("Scan failed");
        }
    };

    return (
        <div className="p-6 h-full flex flex-col bg-slate-950 text-slate-200 overflow-y-auto">
             <div className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                        <Filter className="text-emerald-500" /> Fundamental Scanner
                    </h1>
                    <p className="text-slate-400 mt-2">Filter the market universe by fundamental criteria.</p>
                </div>
                <div className="flex items-center gap-2 text-slate-500 bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-lg text-sm">
                    <Database size={16} /> Universe: US Equities (Mock)
                </div>
            </div>

            <div className="max-w-6xl mx-auto w-full">
                <ScannerBuilder metrics={metrics} onRun={handleRunScan} />
                
                {results.length > 0 && (
                    <ScanResultsTable results={results} metrics={metrics} />
                )}
            </div>
        </div>
    );
};

export default FundamentalScanner;
