import React, { useState, useEffect, useRef } from 'react';
import { StorageService } from '../utils/storageService';
import { assistantService } from '../services/assistantService';
import './AIAssistantDashboard.css';
import { Bot, MessageSquare, Lightbulb, Send, Clock, Sparkles, RefreshCw } from 'lucide-react';
import { Responsive, WidthProvider } from 'react-grid-layout';
import PageHeader from '../components/Navigation/PageHeader';

const ResponsiveGridLayout = WidthProvider(Responsive);
const STORAGE_KEY = 'layout_ai_assistant_v1';

const DEFAULT_LAYOUTS = {
  lg: [
    { i: 'chat', x: 0, y: 0, w: 8, h: 12 },
    { i: 'recommendations', x: 8, y: 0, w: 4, h: 12 }
  ],
  md: [
    { i: 'chat', x: 0, y: 0, w: 6, h: 12 },
    { i: 'recommendations', x: 6, y: 0, w: 4, h: 12 }
  ]
};

const AIAssistantDashboard = () => {
  const [conversation, setConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [userId] = useState('user_1');
  const messagesEndRef = useRef(null);

  const [layouts, setLayouts] = useState(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      return saved ? JSON.parse(saved) : DEFAULT_LAYOUTS;
    } catch (e) {
      return DEFAULT_LAYOUTS;
    }
  });

  const onLayoutChange = (current, all) => {
    setLayouts(all);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(all));
  };

  useEffect(() => {
    initAssistant();
    loadRecommendations();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const initAssistant = async () => {
    try {
      const data = await assistantService.createConversation(userId);
      setConversation(data);
    } catch (error) {
      console.error('Failed to init assistant:', error);
    }
  };

  const loadRecommendations = async () => {
    try {
      const data = await assistantService.getRecommendations(userId);
      setRecommendations(data);
    } catch (error) {
      console.error('Failed to load recommendations:', error);
    }
  };

  const handleSendMessage = async (e) => {
    if (e) e.preventDefault();
    if (!inputMessage.trim() || !conversation || loading) return;

    const userMsg = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMsg]);
    setInputMessage('');
    setLoading(true);

    try {
      const data = await assistantService.sendMessage(conversation.conversation_id, inputMessage);
      const assistantMsg = {
        role: 'assistant',
        content: data.content,
        timestamp: data.timestamp
      };
      setMessages(prev => [...prev, assistantMsg]);
    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: 'I encountered an error while processing your request. Please check your connection and try again.',
        timestamp: new Date().toISOString(),
        error: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="full-bleed-page ai-assistant-page">
      <PageHeader
        icon={<Bot />}
        title={<>AI <span className="text-purple-400">ASSISTANT</span></>}
      />

      <div className="scrollable-content-wrapper">
        <ResponsiveGridLayout
          className="layout"
          layouts={layouts}
          onLayoutChange={onLayoutChange}
          breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
          cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
          rowHeight={60}
          isDraggable={true}
          isResizable={true}
          draggableHandle=".glass-panel-header"
          margin={[15, 15]}
        >
          {/* Main Chat Interface */}
          <div key="chat" className="glass-panel">
            <div className="glass-panel-header">
              <MessageSquare size={14} className="text-purple-400" />
              <span>Personalized Investment Link | Neural Stream</span>
            </div>

            <div className="flex-1 flex flex-col min-h-0 bg-black/20">
              <div className="flex-1 overflow-y-auto p-6 space-y-4 scrollbar-gold">
                {messages.length === 0 ? (
                  <div className="h-full flex flex-col items-center justify-center text-center p-10 opacity-50">
                    <Sparkles size={48} className="text-purple-500 mb-4 animate-pulse" />
                    <h3 className="text-xl font-bold text-white mb-2">Neural Link Ready</h3>
                    <p className="max-w-md text-sm font-mono uppercase tracking-widest text-slate-500">
                      Ask about portfolio diversification, retirement strategies, or technical market analysis.
                    </p>
                  </div>
                ) : (
                  messages.map((msg, idx) => (
                    <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                      <div className={`max-w-[80%] p-4 rounded-2xl border ${
                        msg.role === 'user' 
                          ? 'bg-purple-900/20 border-purple-500/30 text-purple-100 rounded-tr-none' 
                          : msg.error ? 'bg-red-950/20 border-red-500/30 text-red-200' : 'bg-slate-900/60 border-slate-700/50 text-slate-100 rounded-tl-none'
                      } shadow-xl`}>
                        <p className="text-sm leading-relaxed">{msg.content}</p>
                        <div className="flex items-center gap-2 mt-2 opacity-40 text-[9px] font-mono uppercase font-bold">
                          <Clock size={10} />
                          {new Date(msg.timestamp).toLocaleTimeString()}
                        </div>
                      </div>
                    </div>
                  ))
                )}
                {loading && (
                   <div className="flex justify-start">
                     <div className="bg-slate-900/60 border border-slate-700/50 p-4 rounded-2xl rounded-tl-none">
                        <div className="flex gap-1.5 h-4 items-center">
                           <div className="w-1.5 h-1.5 bg-purple-500 rounded-full animate-bounce [animation-delay:-0.3s]" />
                           <div className="w-1.5 h-1.5 bg-purple-500 rounded-full animate-bounce [animation-delay:-0.15s]" />
                           <div className="w-1.5 h-1.5 bg-purple-500 rounded-full animate-bounce" />
                        </div>
                     </div>
                   </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* Chat Input */}
              <form onSubmit={handleSendMessage} className="p-4 border-t border-white/5 bg-black/40 flex gap-3">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-purple-500/50 transition-all font-mono"
                  placeholder="Inquire AI engine..."
                />
                <button
                  type="submit"
                  disabled={loading || !inputMessage.trim()}
                  className="bg-purple-600/20 text-purple-400 border border-purple-500/30 w-12 h-12 rounded-xl flex items-center justify-center hover:bg-purple-500/30 disabled:opacity-50 transition-all"
                >
                  {loading ? <RefreshCw className="animate-spin" size={18} /> : <Send size={18} />}
                </button>
              </form>
            </div>
          </div>

          {/* Recommendations Side Panel */}
          <div key="recommendations" className="glass-panel">
            <div className="glass-panel-header">
              <Lightbulb size={14} className="text-purple-400" />
              <span>Smart Recommendations</span>
            </div>
            <div className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-gold bg-black/10">
               {recommendations.length > 0 ? (
                 recommendations.map((rec, idx) => (
                   <div key={idx} className="p-4 bg-slate-900/40 border border-white/5 rounded-xl hover:border-purple-500/30 transition-all group cursor-pointer">
                      <div className="flex justify-between items-start mb-2">
                        <h4 className="text-xs font-black text-white group-hover:text-purple-300 transition-colors uppercase tracking-tight">{rec.title}</h4>
                        <span className="text-[9px] font-bold bg-purple-500/20 text-purple-400 px-2 py-0.5 rounded-full border border-purple-500/20">
                          {(rec.confidence * 100).toFixed(0)}% Match
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-400 leading-tight mb-3 italic">"{rec.description}"</p>
                      <div className="text-[9px] font-bold text-slate-600 uppercase tracking-widest border-t border-white/5 pt-2">
                         Logic: {rec.reasoning}
                      </div>
                   </div>
                 ))
               ) : (
                 <div className="h-full flex flex-col items-center justify-center text-center p-6 opacity-30 text-slate-500">
                    <Lightbulb size={32} className="mb-2" />
                    <p className="text-[10px] font-mono uppercase">Initializing logic engine...</p>
                 </div>
               )}
            </div>
          </div>
        </ResponsiveGridLayout>
        <div className="scroll-buffer-100" />
      </div>
    </div>
  );
};

export default AIAssistantDashboard;
