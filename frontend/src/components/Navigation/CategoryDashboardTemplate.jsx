import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import LiveGlimpseWidget from './LiveGlimpseWidget';
import './CategoryDashboardTemplate.css';

/**
 * CategoryDashboardTemplate
 * 
 * The master template for all "Category/Role" hubs (Trader, Architect, etc.)
 * Implements the bento grid, standardized header, and role-based theme injection.
 */
const CategoryDashboardTemplate = ({ 
  title, 
  subtitle, 
  metrics = [], 
  capabilities = [], 
  accentColor = '#00d1ff',
  icon: CategoryIcon
}) => {
  
  // Theme Injection: Set CSS variables based on the role's accent color
  useEffect(() => {
    const root = document.documentElement;
    root.style.setProperty('--accent-color', accentColor);
    // Create a semi-transparent version for glows
    root.style.setProperty('--accent-color-glow', `${accentColor}1A`); // 10% opacity
    root.style.setProperty('--accent-color-glow-heavy', `${accentColor}33`); // 20% opacity
    
    return () => {
      // Clean up on unmount if needed, though usually overwriting is fine
    };
  }, [accentColor]);

  // Animation variants
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.05 }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { 
      y: 0, 
      opacity: 1,
      transition: { type: 'spring', stiffness: 300, damping: 24 }
    }
  };

  return (
    <div className="category-dashboard">
      {/* Namespace Header */}
      <motion.header 
        className="namespace-header"
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
      >
        <div className="namespace-title-group">
          <h1>
            <span className="namespace-accent-dot"></span>
            # {title}
            {CategoryIcon && <CategoryIcon size={32} className="opacity-40" />}
          </h1>
          <span className="namespace-status">
            {subtitle} — ROLE STATUS: <strong>VERIFIED</strong>
          </span>
        </div>

        <div className="live-glimpse-bar">
          {metrics.map((m, i) => (
            <LiveGlimpseWidget 
              key={`${m.label}-${i}`} 
              label={m.label} 
              value={m.value} 
              unit={m.unit}
              trend={m.trend}
            />
          ))}
        </div>
      </motion.header>

      {/* Capability Grid (Bento) */}
      <motion.div 
        className="capability-grid"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {capabilities.map((cap, i) => (
          <motion.div key={cap.path} variants={itemVariants}>
            <Link to={cap.path} className="capability-card group">
              {/* Active Scanning Overlay (Simulated) */}
              {(i % 3 === 0) && <div className="scanning-line" />}
              
              <div className="card-content">
                <h3>{cap.label}</h3>
                <p>{cap.description}</p>
              </div>

              <div className="card-footer">
                <div className="card-status">
                  <span className="status-indicator"></span>
                  Node: Active
                </div>
                <div className="text-[10px] text-zinc-600 font-mono">
                  {cap.path.split('/').pop().toUpperCase()}::EXEC
                </div>
              </div>

              {/* Decorative Sparkline for the Card */}
              <div className="card-mini-sparkline">
                <svg viewBox="0 0 120 40" preserveAspectRatio="none">
                  <path 
                    d="M 0 30 L 20 25 L 40 35 L 60 10 L 80 20 L 100 5 L 120 15" 
                    fill="none" 
                    stroke="var(--accent-color)" 
                    strokeWidth="1" 
                  />
                </svg>
              </div>
            </Link>
          </motion.div>
        ))}
      </motion.div>

      {/* Breadcrumb pathing Home > [Category] is handled by Taskbar/Global UI, 
          but we ensure the content here aligns with it. */}
    </div>
  );
};

export default CategoryDashboardTemplate;
