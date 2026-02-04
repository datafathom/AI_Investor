import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

/**
 * LiveGlimpseWidget
 * 
 * A sleek, compact widget for top-level category metrics.
 * Features a background sparkline and value-flicker animation on update.
 */
const LiveGlimpseWidget = ({ label, value, unit, trend, sparklineData = [20, 40, 35, 50, 45, 60, 55] }) => {
  const [flicker, setFlicker] = useState(false);

  useEffect(() => {
    // Trigger flicker animation when value changes
    setFlicker(true);
    const timer = setTimeout(() => setFlicker(false), 400);
    return () => clearTimeout(timer);
  }, [value]);

  // Generate SVG path for sparkline
  const generatePath = (data) => {
    const width = 120;
    const height = 40;
    const padding = 5;
    const max = Math.max(...data) + padding;
    const min = Math.min(...data) - padding;
    const range = max - min;
    
    return data.map((val, i) => {
      const x = (i / (data.length - 1)) * width;
      const y = height - ((val - min) / range) * height;
      return `${i === 0 ? 'M' : 'L'} ${x} ${y}`;
    }).join(' ');
  };

  return (
    <div className="glimpse-widget overflow-hidden relative" style={{ minWidth: '180px' }}>
      {/* Background Sparkline */}
      <div className="absolute inset-x-0 bottom-0 h-1/2 opacity-20 pointer-events-none">
        <svg viewBox="0 0 120 40" preserveAspectRatio="none" className="w-full h-full">
          <motion.path
            d={generatePath(sparklineData)}
            fill="none"
            stroke="var(--accent-color)"
            strokeWidth="2"
            initial={{ pathLength: 0 }}
            animate={{ pathLength: 1 }}
            transition={{ duration: 1.5, ease: "easeInOut" }}
          />
        </svg>
      </div>

      <div className="relative z-10 flex flex-col">
        <span className="glimpse-label mb-1">{label}</span>
        <div className="flex items-baseline gap-2">
          <motion.span 
            className={`glimpse-value text-xl font-bold ${flicker ? 'flicker-active' : ''}`}
            animate={flicker ? { textShadow: "0 0 8px var(--accent-color)" } : { textShadow: "none" }}
          >
            {value}
            <span className="text-xs font-medium ml-1 opacity-60 uppercase">{unit}</span>
          </motion.span>
          
          {trend && (
            <span className={`text-[10px] font-bold ${trend.startsWith('+') ? 'text-green-500' : 'text-red-500'}`}>
              {trend}
            </span>
          )}
        </div>
      </div>
    </div>
  );
};

export default LiveGlimpseWidget;
