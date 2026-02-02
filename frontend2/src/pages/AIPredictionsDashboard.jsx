import React, { useState, useEffect } from 'react';
import { predictionService } from '../services/predictionService';
import './AIPredictionsDashboard.css';
import { Brain, TrendingUp, Activity, BarChart3, Search, RefreshCw, Layers } from 'lucide-react';
import { Responsive, WidthProvider } from 'react-grid-layout';
import PageHeader from '../components/Navigation/PageHeader';

const ResponsiveGridLayout = WidthProvider(Responsive);
const STORAGE_KEY = 'layout_ai_predictions_v1';

const DEFAULT_LAYOUTS = {
  lg: [
    { i: 'controls', x: 0, y: 0, w: 12, h: 2 },
    { i: 'price', x: 0, y: 2, w: 6, h: 6 },
    { i: 'trend', x: 6, y: 2, w: 6, h: 6 },
    { i: 'regime', x: 0, y: 8, w: 12, h: 4 }
  ],
  md: [
    { i: 'controls', x: 0, y: 0, w: 10, h: 2 },
    { i: 'price', x: 0, y: 2, w: 5, h: 6 },
    { i: 'trend', x: 5, y: 2, w: 5, h: 6 },
    { i: 'regime', x: 0, y: 8, w: 10, h: 4 }
  ]
};

const AIPredictionsDashboard = () => {
  const [prediction, setPrediction] = useState(null);
  const [trend, setTrend] = useState(null);
  const [regime, setRegime] = useState(null);
  const [selectedSymbol, setSelectedSymbol] = useState('AAPL');
  const [loading, setLoading] = useState(false);

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
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [priceP, trendP, regimeP] = await Promise.allSettled([
        predictionService.getPricePrediction(selectedSymbol),
        predictionService.getTrendPrediction(selectedSymbol),
        predictionService.getMarketRegime('SPY')
      ]);

      if (priceP.status === 'fulfilled') setPrediction(priceP.value);
      if (trendP.status === 'fulfilled') setTrend(trendP.value);
      if (regimeP.status === 'fulfilled') setRegime(regimeP.value);
    } catch (error) {
      console.error('Error loading AI Predictions:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="full-bleed-page ai-predictions-page">
      <PageHeader 
        icon={<Brain />}
        title={<>AI <span className="text-cyan-400">PREDICTIONS</span></>}
      />

      <div className="scrollable-content-wrapper">
        <ResponsiveGridLayout
          className="layout"
          layouts={layouts}
          onLayoutChange={onLayoutChange}
          breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
          cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
          rowHeight={80}
          isDraggable={true}
          isResizable={true}
          draggableHandle=".glass-panel-header"
          margin={[15, 15]}
        >
          {/* Controls Panel */}
          <div key="controls" className="glass-panel flex items-center px-6">
            <div className="flex-1 flex gap-4 items-center">
              <div className="relative flex-1 max-w-md">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={16} />
                <input
                  type="text"
                  value={selectedSymbol}
                  onChange={(e) => setSelectedSymbol(e.target.value.toUpperCase())}
                  className="w-full bg-black/40 border border-white/10 rounded-lg pl-10 pr-4 py-2 text-sm text-white focus:outline-none focus:border-cyan-500/50"
                  placeholder="Analyze Ticker..."
                />
              </div>
              <button 
                onClick={loadData} 
                disabled={loading}
                className="bg-cyan-600/20 text-cyan-400 border border-cyan-500/30 px-6 py-2 rounded-lg text-xs font-bold hover:bg-cyan-500/30 transition-all flex items-center gap-2"
              >
                {loading ? <RefreshCw className="animate-spin" size={14} /> : <TrendingUp size={14} />}
                RUN INFERENCE
              </button>
            </div>
            <div className="flex gap-6 font-mono text-[10px] uppercase text-slate-500">
               <div className="flex flex-col items-end">
                  <span>Inference Engine</span>
                  <span className="text-white font-bold">Alpha-Zero v4</span>
               </div>
               <div className="flex flex-col items-end">
                  <span>Latency</span>
                  <span className="text-green-400 font-bold">42ms</span>
               </div>
            </div>
          </div>

          {/* Price Forecasting */}
          <div key="price" className="glass-panel">
            <div className="glass-panel-header">
               <BarChart3 size={14} className="text-cyan-400" />
               <span>Price Forecasting | Next 30 Days</span>
            </div>
            <div className="p-8 flex flex-col items-center justify-center h-full">
              {prediction ? (
                <>
                  <div className="text-5xl font-black text-white tracking-tighter mb-4">
                    ${prediction.predicted_price?.toFixed(2)}
                  </div>
                  <div className="flex gap-4">
                    <div className="px-4 py-2 bg-black/40 border border-white/10 rounded-xl text-center">
                       <div className="text-[9px] text-slate-500 uppercase font-black mb-1">Confidence</div>
                       <div className="text-xl font-bold text-cyan-400">{(prediction.confidence * 100).toFixed(0)}%</div>
                    </div>
                    {prediction.confidence_interval && (
                      <div className="px-4 py-2 bg-black/40 border border-white/10 rounded-xl text-center">
                         <div className="text-[9px] text-slate-500 uppercase font-black mb-1">Interval (95%)</div>
                         <div className="text-sm font-bold text-white">
                            ${prediction.confidence_interval.lower?.toFixed(2)} - ${prediction.confidence_interval.upper?.toFixed(2)}
                         </div>
                      </div>
                    )}
                  </div>
                </>
              ) : (
                <div className="text-slate-600 font-mono text-xs italic">Awaiting telemetry...</div>
              )}
            </div>
          </div>

          {/* Trend Analysis */}
          <div key="trend" className="glass-panel">
            <div className="glass-panel-header">
               <TrendingUp size={14} className="text-cyan-400" />
               <span>Trend Confluence Analysis</span>
            </div>
            <div className="p-8 flex flex-col items-center justify-center h-full">
              {trend ? (
                <>
                  <div className={`text-4xl font-black mb-2 tracking-widest ${trend.trend_direction === 'bullish' ? 'text-green-400' : 'text-red-400'}`}>
                    {trend.trend_direction?.toUpperCase()}
                  </div>
                  <div className="text-2xl font-mono text-white mb-6">
                    {trend.predicted_change > 0 ? '+' : ''}{trend.predicted_change?.toFixed(2)}%
                  </div>
                  <div className="w-64 h-2 bg-slate-900 rounded-full overflow-hidden border border-white/5 shadow-inner">
                     <div 
                        className="h-full bg-cyan-500 shadow-[0_0_15px_rgba(34,211,238,0.5)] transition-all duration-1000"
                        style={{ width: `${trend.trend_strength * 100}%` }}
                     />
                  </div>
                  <div className="text-[10px] text-slate-500 font-bold uppercase mt-2 tracking-widest">
                    Sentiment Strength: {(trend.trend_strength * 100).toFixed(0)}%
                  </div>
                </>
              ) : (
                <div className="text-slate-600 font-mono text-xs italic">Parsing social/macro signals...</div>
              )}
            </div>
          </div>

          {/* Market Regime Detection */}
          <div key="regime" className="glass-panel">
            <div className="glass-panel-header">
               <Layers size={14} className="text-cyan-400" />
               <span>Market Regime Detection | SPY Basis</span>
            </div>
            <div className="p-6 h-full flex items-center justify-around">
               {regime ? (
                 <>
                   <div className="flex flex-col items-center">
                     <div className="text-[10px] text-slate-500 font-black uppercase mb-2 tracking-widest">Detected Regime</div>
                     <div className={`text-3xl font-black ${regime.regime_type === 'bull' ? 'text-green-400' : regime.regime_type === 'bear' ? 'text-red-400' : 'text-amber-400'}`}>
                        {regime.regime_type?.toUpperCase()}
                     </div>
                   </div>
                   <div className="h-12 w-px bg-white/10" />
                   <div className="flex flex-col items-center">
                     <div className="text-[10px] text-slate-500 font-black uppercase mb-2 tracking-widest">Model Certainty</div>
                     <div className="text-3xl font-black text-white">{(regime.confidence * 100).toFixed(0)}%</div>
                   </div>
                   <div className="h-12 w-px bg-white/10" />
                   <div className="flex flex-col items-center">
                     <div className="text-[10px] text-slate-500 font-black uppercase mb-2 tracking-widest">Expected persistence</div>
                     <div className="text-3xl font-black text-cyan-400">{regime.expected_duration || 'Unknown'}</div>
                   </div>
                 </>
               ) : (
                 <div className="text-slate-600 font-mono text-xs italic">Syncing with global market pulse...</div>
               )}
            </div>
          </div>
        </ResponsiveGridLayout>
        <div className="scroll-buffer-100" />
      </div>
    </div>
  );
};

export default AIPredictionsDashboard;
