import React from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

const RoleGlimpseCard = ({ label, value, trend, unit }) => {
  const isPositive = trend.startsWith('+');
  const isNegative = trend.startsWith('-');
  const TrendIcon = isPositive ? TrendingUp : isNegative ? TrendingDown : Minus;

  return (
    <div className="glimpse-card group relative p-6 bg-zinc-900/40 border border-zinc-800 rounded-2xl overflow-hidden hover:border-cyan-500/30 transition-all duration-500">
      <div className="flex justify-between items-start mb-2">
        <label className="text-zinc-500 uppercase text-[10px] font-black tracking-widest block">
          {label}
        </label>
        {trend && (
           <div className={`flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-full ${
             isPositive ? 'bg-green-500/10 text-green-400' : 
             isNegative ? 'bg-red-500/10 text-red-400' : 'bg-zinc-500/10 text-zinc-400'
           }`}>
             <TrendIcon size={10} />
             {trend}
           </div>
        )}
      </div>
      
      <div className="flex items-baseline gap-2">
        <span className="text-3xl font-mono font-bold text-white group-hover:text-cyan-400 transition-colors">
          {value}
        </span>
        {unit && (
          <span className="text-zinc-600 font-mono text-xs uppercase font-bold tracking-tight">
            {unit}
          </span>
        )}
      </div>

      {/* Decorative background element */}
      <div className="absolute -bottom-4 -right-4 w-16 h-16 bg-cyan-500/5 rounded-full blur-2xl group-hover:bg-cyan-500/10 transition-all duration-500" />
    </div>
  );
};

export default RoleGlimpseCard;
