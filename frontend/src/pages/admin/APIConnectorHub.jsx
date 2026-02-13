import React, { useState, useEffect } from 'react';
import { integrationsService } from '../../services/integrationsService';
import { toast } from 'sonner';
import { Plus, Plug, Activity, Key, Webhook, CheckCircle, AlertCircle, RefreshCw } from 'lucide-react';
import { authService } from '../../utils/authService';

const ConnectorCard = ({ connector, onTest }) => (
    <div className="bg-slate-900 border border-slate-700/50 rounded-lg p-5 hover:border-cyan-500/50 transition-all group">
        <div className="flex justify-between items-start mb-4">
            <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center text-cyan-400">
                    <Plug size={20} />
                </div>
                <div>
                    <h3 className="font-semibold text-slate-100">{connector.name}</h3>
                    <p className="text-xs text-slate-500 capitalize">{connector.type}</p>
                </div>
            </div>
            <div className={`px-2 py-0.5 rounded text-[10px] font-mono uppercase border ${
                connector.status === 'connected' ? 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10' : 
                connector.status === 'error' ? 'text-red-400 border-red-500/30 bg-red-500/10' : 'text-slate-400 border-slate-600'
            }`}>
                {connector.status}
            </div>
        </div>
        <div className="text-xs text-slate-400 mb-4">
            Last Sync: {connector.last_sync ? new Date(connector.last_sync).toLocaleString() : 'Never'}
        </div>
        <button 
            onClick={() => onTest(connector.id)}
            className="w-full py-2 text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700 transition-colors"
        >
            Test Connection
        </button>
    </div>
);

const APIKeyRow = ({ apiKey }) => (
    <div className="flex items-center justify-between p-3 bg-slate-900/50 border border-slate-800 rounded mb-2">
        <div className="flex items-center gap-3">
            <Key size={16} className="text-amber-400" />
            <div>
                <div className="text-sm font-medium text-slate-200">{apiKey.label}</div>
                <div className="text-xs text-slate-500 font-mono">{apiKey.prefix}••••••••</div>
            </div>
        </div>
        <div className="text-xs text-slate-500">
            Created: {apiKey.created_at}
        </div>
    </div>
);

const APIConnectorHub = () => {
    const [connectors, setConnectors] = useState([]);
    const [apiKeys, setApiKeys] = useState([]);
    const [webhooks, setWebhooks] = useState([]);
    const [loading, setLoading] = useState(true);
    const currentUser = authService.getCurrentUser();

    const loadData = async () => {
        try {
            setLoading(true);
            const [conns, keys, hooks] = await Promise.all([
                integrationsService.getConnectors(),
                integrationsService.getApiKeys(),
                integrationsService.getWebhooks()
            ]);
            setConnectors(conns.data || []);
            setApiKeys(keys.data || []);
            setWebhooks(hooks.data || []);
        } catch (error) {
            console.error("Failed to load integration data", error);
            toast.error("Failed to load integrations");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadData();
    }, []);

    const handleTestConnector = async (id) => {
        try {
            toast.promise(integrationsService.testConnector(id), {
                loading: 'Testing connection...',
                success: 'Connection test passed',
                error: 'Connection test failed'
            });
        } catch (e) {
            console.error(e);
        }
    };

    const handleCreateKey = async () => {
        const label = prompt("Enter a label for the new API Key:");
        if (label) {
            try {
                await integrationsService.createApiKey(label);
                toast.success("API Key created");
                loadData();
            } catch (e) {
                toast.error("Failed to create API key");
            }
        }
    };

    return (
        <div className="p-8 h-full overflow-y-auto bg-slate-950 text-slate-200">
            <div className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                        <Plug className="text-cyan-500" /> API Connector Hub
                    </h1>
                    <p className="text-slate-400 mt-2">Manage external data sources, API keys, and webhooks.</p>
                </div>
                <button 
                    onClick={loadData}
                    className="p-2 bg-slate-800 hover:bg-slate-700 rounded-md border border-slate-700 text-slate-400 hover:text-white transition-colors"
                >
                    <RefreshCw size={20} className={loading ? "animate-spin" : ""} />
                </button>
            </div>

            <div className="grid grid-cols-12 gap-8">
                {/* Main Content - Connectors */}
                <div className="col-span-12 lg:col-span-8">
                    <section className="mb-8">
                        <div className="flex justify-between items-center mb-4">
                            <h2 className="text-xl font-semibold text-slate-200">Active Connectors</h2>
                            <button className="flex items-center gap-2 px-3 py-1.5 text-sm bg-cyan-600 hover:bg-cyan-500 text-white rounded transition-colors">
                                <Plus size={16} /> Add Connector
                            </button>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {connectors.map(c => (
                                <ConnectorCard key={c.id} connector={c} onTest={handleTestConnector} />
                            ))}
                            {connectors.length === 0 && !loading && (
                                <div className="col-span-2 text-center py-12 border border-dashed border-slate-800 rounded-lg text-slate-500">
                                    No active connectors found.
                                </div>
                            )}
                        </div>
                    </section>

                    <section>
                         <h2 className="text-xl font-semibold text-slate-200 mb-4">Available Integrations</h2>
                         <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
                            <p className="text-slate-400 text-sm mb-4">Connect to these services to expand your data ingestion capabilties.</p>
                            <div className="flex flex-wrap gap-3">
                                {['Salesforce', 'Slack', 'QuickBooks', 'Jira', 'Notion', 'GitHub'].map(name => (
                                    <div key={name} className="px-3 py-2 bg-slate-800 rounded border border-slate-700 text-sm text-slate-300 hover:border-cyan-500/50 cursor-pointer transition-all">
                                        + {name}
                                    </div>
                                ))}
                            </div>
                         </div>
                    </section>
                </div>

                {/* Sidebar - Keys & Webhooks */}
                <div className="col-span-12 lg:col-span-4 space-y-8">
                    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                        <div className="flex justify-between items-center mb-4">
                            <h3 className="font-semibold text-slate-200 flex items-center gap-2">
                                <Key size={18} className="text-amber-400" /> API Keys
                            </h3>
                            <button onClick={handleCreateKey} className="text-xs text-cyan-400 hover:text-cyan-300">
                                + New Key
                            </button>
                        </div>
                        <div className="space-y-2">
                            {apiKeys.map(k => <APIKeyRow key={k.id} apiKey={k} />)}
                        </div>
                    </div>

                    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                        <div className="flex justify-between items-center mb-4">
                            <h3 className="font-semibold text-slate-200 flex items-center gap-2">
                                <Webhook size={18} className="text-purple-400" /> Webhooks
                            </h3>
                            <button className="text-xs text-cyan-400 hover:text-cyan-300">
                                + Add Endpoint
                            </button>
                        </div>
                        <div className="space-y-3">
                            {webhooks.map(w => (
                                <div key={w.id} className="text-sm border-b border-slate-800 pb-2 last:border-0 last:pb-0">
                                    <div className="font-mono text-xs text-slate-400 truncate">{w.url}</div>
                                    <div className="flex gap-1 mt-1 flex-wrap">
                                        {w.events.map(e => (
                                            <span key={e} className="px-1.5 py-0.5 bg-purple-500/10 text-purple-400 text-[10px] rounded border border-purple-500/20">{e}</span>
                                        ))}
                                    </div>
                                </div>
                            ))}
                            {webhooks.length === 0 && <div className="text-xs text-slate-500">No webhooks configured.</div>}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default APIConnectorHub;
