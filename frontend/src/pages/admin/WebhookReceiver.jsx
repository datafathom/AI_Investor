import React, { useState, useEffect } from 'react';
import { webhookService } from '../../services/webhookService';
import { toast } from 'sonner';
import { Radio, RefreshCw, Code, CheckCircle, XCircle, Clock } from 'lucide-react';

const WebhookReceiver = () => {
  const [events, setEvents] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      setLoading(true);
      const data = await webhookService.getEvents();
      setEvents(data);
      if (!selectedEvent && data.length > 0) {
        setSelectedEvent(data[0]);
      }
    } catch (error) {
      toast.error("Failed to load webhook events");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 10000); // Poll every 10s
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-6 h-full overflow-y-auto bg-slate-950 text-slate-200">
        <div className="flex justify-between items-center mb-6">
            <div>
                <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                    <Radio className="text-purple-500" /> Webhook Receiver
                </h1>
                <p className="text-slate-400 mt-2">Inspect incoming webhooks and their payloads.</p>
            </div>
             <button 
                onClick={loadData}
                className="p-2 bg-slate-800 hover:bg-slate-700 rounded-md border border-slate-700 text-slate-400 hover:text-white transition-colors"
            >
                <RefreshCw size={20} className={loading ? "animate-spin" : ""} />
            </button>
        </div>

        <div className="grid grid-cols-12 gap-6 h-[calc(100%-100px)]">
            {/* List */}
            <div className="col-span-12 lg:col-span-4 bg-slate-900 border border-slate-800 rounded-lg overflow-hidden flex flex-col">
                <div className="p-4 border-b border-slate-800 bg-slate-900/50 font-semibold text-slate-300">
                    Recent Events
                </div>
                <div className="flex-1 overflow-y-auto">
                    {events.map(event => (
                        <div 
                            key={event.id}
                            onClick={() => setSelectedEvent(event)}
                            className={`p-4 border-b border-slate-800 cursor-pointer hover:bg-slate-800/50 transition-colors ${
                                selectedEvent?.id === event.id ? 'bg-purple-900/20 border-l-4 border-l-purple-500' : 'border-l-4 border-l-transparent'
                            }`}
                        >
                            <div className="flex justify-between items-start mb-1">
                                <span className="font-mono text-xs font-bold text-purple-400 uppercase">{event.source}</span>
                                <span className="text-[10px] text-slate-500">{new Date(event.received_at).toLocaleTimeString()}</span>
                            </div>
                            <div className="font-semibold text-slate-200 text-sm mb-1">{event.event_type}</div>
                            <div className="flex items-center gap-2">
                                {event.status === 'processed' ? (
                                    <div className="flex items-center gap-1 text-[10px] text-emerald-400">
                                        <CheckCircle size={10} /> Processed
                                    </div>
                                ) : (
                                     <div className="flex items-center gap-1 text-[10px] text-slate-400">
                                        <Clock size={10} /> {event.status}
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                    {events.length === 0 && !loading && (
                        <div className="p-8 text-center text-slate-500 text-sm">No events received yet.</div>
                    )}
                </div>
            </div>

            {/* Details */}
            <div className="col-span-12 lg:col-span-8 bg-slate-900 border border-slate-800 rounded-lg overflow-hidden flex flex-col">
                 <div className="p-4 border-b border-slate-800 bg-slate-900/50 flex justify-between items-center">
                    <span className="font-semibold text-slate-300">Payload Inspector</span>
                    {selectedEvent && <span className="text-xs font-mono text-slate-500">ID: {selectedEvent.id}</span>}
                </div>
                {selectedEvent ? (
                    <div className="p-6 flex-1 overflow-y-auto">
                        <div className="grid grid-cols-2 gap-4 mb-6">
                            <div className="bg-slate-950 p-3 rounded border border-slate-800">
                                <div className="text-xs text-slate-500 uppercase mb-1">Source</div>
                                <div className="text-slate-200 font-mono">{selectedEvent.source}</div>
                            </div>
                            <div className="bg-slate-950 p-3 rounded border border-slate-800">
                                <div className="text-xs text-slate-500 uppercase mb-1">Event Type</div>
                                <div className="text-slate-200 font-mono">{selectedEvent.event_type}</div>
                            </div>
                             <div className="bg-slate-950 p-3 rounded border border-slate-800 col-span-2">
                                <div className="text-xs text-slate-500 uppercase mb-1">Processing Log</div>
                                <div className="text-slate-300 text-sm">{selectedEvent.processing_log}</div>
                            </div>
                        </div>

                        <div className="border border-slate-800 rounded-lg overflow-hidden">
                            <div className="bg-slate-950 p-2 border-b border-slate-800 text-xs text-slate-500 flex items-center gap-2">
                                <Code size={14} /> JSON Payload
                            </div>
                            <div className="p-4 bg-[#0d1117]">
                                <pre className="text-sm font-mono text-slate-300 whitespace-pre-wrap break-all overflow-x-auto">
                                    {JSON.stringify(selectedEvent.payload, null, 2)}
                                </pre>
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className="h-full flex flex-col items-center justify-center text-slate-500">
                        <Radio size={48} className="mb-4 opacity-20" />
                        <p>Select an event to view payload</p>
                    </div>
                )}
            </div>
        </div>
    </div>
  );
};

export default WebhookReceiver;
