import React, { useState, useEffect } from 'react';
import { useWealthStore } from '../stores/wealthStore';
import { Responsive, WidthProvider } from 'react-grid-layout';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';
import '../App.css'; 

import ManualEntry from '../widgets/Assets/ManualEntry';
import ValuationSlider from '../widgets/Assets/ValuationSlider';
import NetWorthGauges from '../widgets/Assets/NetWorthGauges';

// New UI/UX Components
import { StatCard, Badge } from '../components/DataViz';
import { GlassCard } from '../components/Common';

const ResponsiveGridLayout = WidthProvider(Responsive);

export default function AssetsDashboard() {
  const fetchAssets = useWealthStore((state) => state.fetchAssets);

  useEffect(() => {
    fetchAssets();
  }, [fetchAssets]);

  const DEFAULT_LAYOUT = {
    lg: [
      { i: 'stats', x: 0, y: 0, w: 12, h: 2 },
      { i: 'manual_entry', x: 0, y: 2, w: 4, h: 6 },
      { i: 'net_worth_gauges', x: 4, y: 2, w: 4, h: 6 },
      { i: 'valuation_slider', x: 8, y: 2, w: 4, h: 6 },
    ]
  };
  const STORAGE_KEY = 'layout_assets_dashboard';

  const [layouts, setLayouts] = useState(() => {
     try {
         const saved = localStorage.getItem(STORAGE_KEY);
         return saved ? JSON.parse(saved) : DEFAULT_LAYOUT;
     } catch (e) {
         return DEFAULT_LAYOUT;
     }
  });

  const onLayoutChange = (currentLayout, allLayouts) => {
      setLayouts(allLayouts);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(allLayouts));
  };

  const assetStats = [
    { label: 'Total Real Estate', value: 2850000, prefix: '$', status: 'positive' },
    { label: 'Illiquid Assets', value: 485000, prefix: '$', status: 'neutral' },
    { label: 'Properties', value: 4, status: 'neutral' },
    { label: 'Appreciation YTD', value: 8.4, suffix: '%', status: 'positive' }
  ];

  return (
    <div className="full-bleed-page assets-dashboard">
      <header className="mb-6">
        <div className="flex items-center gap-4">
          <h1 className="text-3xl font-black text-white tracking-tight uppercase">
            Real Estate & Illiquid
          </h1>
          <Badge count="4 Properties" variant="info" />
        </div>
        <p className="text-zinc-500 mt-1">Net worth visualization, manual entry, and valuation sliders.</p>
      </header>

      <div className="scrollable-content-wrapper">
        <ResponsiveGridLayout
          className="layout"
          layouts={layouts}
          breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
          cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
          rowHeight={80}
          draggableHandle=".glass-panel"
          onLayoutChange={onLayoutChange}
          isDraggable={true}
          isResizable={true}
        >
          <div key="stats" style={{ display: 'flex', gap: '16px' }}>
            {assetStats.map((stat, idx) => (
              <div key={idx} style={{ flex: 1 }}>
                <StatCard {...stat} formatValue={v => typeof v === 'number' && v > 100 ? v.toLocaleString() : v} />
              </div>
            ))}
          </div>

          <div key="manual_entry" style={{ borderRadius: '12px', overflow: 'hidden' }}>
            <GlassCard variant="elevated" hoverable={false} className="h-full">
              <h3 className="font-bold text-white mb-4">Manual Entry</h3>
              <ManualEntry />
            </GlassCard>
          </div>
          <div key="net_worth_gauges" style={{ borderRadius: '12px', overflow: 'hidden' }}>
            <GlassCard variant="elevated" hoverable={false} className="h-full">
              <h3 className="font-bold text-white mb-4">Net Worth Gauges</h3>
              <NetWorthGauges />
            </GlassCard>
          </div>
          <div key="valuation_slider" style={{ borderRadius: '12px', overflow: 'hidden' }}>
            <GlassCard variant="elevated" hoverable={false} className="h-full">
              <div className="flex justify-between items-center mb-3">
                <h3 className="font-bold text-white">Valuation Slider</h3>
                <Badge count="+8.4% YTD" variant="success" />
              </div>
              <ValuationSlider />
            </GlassCard>
          </div>
        </ResponsiveGridLayout>
        
        {/* Bottom Buffer */}
        <div className="scroll-buffer-100" />
      </div>
    </div>
  );
};
