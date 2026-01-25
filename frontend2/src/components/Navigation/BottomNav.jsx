import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Home, PieChart, Shield, Cpu, Settings } from 'lucide-react';
import './BottomNav.css';

const navItems = [
  { path: '/', icon: Home, label: 'Home' },
  { path: '/portfolio', icon: PieChart, label: 'Portfolio' },
  { path: '/guardian', icon: Shield, label: 'Guardian' },
  { path: '/analytics', icon: Cpu, label: 'Lab' },
  { path: '/settings', icon: Settings, label: 'Settings' }
];

/**
 * Fixed bottom navigation for mobile devices.
 * Only visible on screens < 768px.
 */
const BottomNav = () => {
  const navigate = useNavigate();
  const location = useLocation();
  
  const isActive = (path) => {
    if (path === '/') return location.pathname === '/';
    return location.pathname.startsWith(path);
  };

  return (
    <nav className="bottom-nav" role="navigation" aria-label="Primary navigation">
      {navItems.map(({ path, icon: Icon, label }) => (
        <button
          key={path}
          className={`bottom-nav__item ${isActive(path) ? 'bottom-nav__item--active' : ''}`}
          onClick={() => navigate(path)}
          aria-label={label}
          aria-current={isActive(path) ? 'page' : undefined}
        >
          <Icon size={20} strokeWidth={isActive(path) ? 2.5 : 1.5} />
          <span className="bottom-nav__label">{label}</span>
          {isActive(path) && <span className="bottom-nav__indicator" />}
        </button>
      ))}
    </nav>
  );
};

export default BottomNav;
