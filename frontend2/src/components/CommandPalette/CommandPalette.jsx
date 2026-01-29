import React, { useState, useEffect, useRef, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Search, Command, ArrowRight, Home, PieChart, Shield, Cpu, 
  Activity, HardDrive, Globe, Layout, Settings, Moon, Sun,
  Zap, TrendingUp, DollarSign, FileText, Users, Bot, BarChart3
} from 'lucide-react';
import { searchService } from '../../services/searchService';
import './CommandPalette.css';

const COMMANDS = [
  // Navigation
  { id: 'nav-home', label: 'Go to Dashboard', category: 'Navigation', icon: Home, action: 'navigate', path: '/' },
  { id: 'nav-portfolio', label: 'Go to Portfolio', category: 'Navigation', icon: PieChart, action: 'navigate', path: '/portfolio' },
  { id: 'nav-guardian', label: 'Go to Guardian', category: 'Navigation', icon: Shield, action: 'navigate', path: '/guardian' },
  { id: 'nav-analytics', label: 'Go to Analytics Lab', category: 'Navigation', icon: Cpu, action: 'navigate', path: '/analytics' },
  { id: 'nav-strategist', label: 'Go to Strategist', category: 'Navigation', icon: Activity, action: 'navigate', path: '/strategist' },
  { id: 'nav-architect', label: 'Go to Architect', category: 'Navigation', icon: HardDrive, action: 'navigate', path: '/architect' },
  { id: 'nav-observer', label: 'Go to Observer', category: 'Navigation', icon: Globe, action: 'navigate', path: '/observer' },
  { id: 'nav-workspace', label: 'Go to Workspace', category: 'Navigation', icon: Layout, action: 'navigate', path: '/workspace' },
  
  // Actions
  { id: 'act-settings', label: 'Open Settings', category: 'Actions', icon: Settings, action: 'navigate', path: '/settings' },
  { id: 'act-theme', label: 'Toggle Theme', category: 'Actions', icon: Moon, action: 'theme' },
  { id: 'act-quick-trade', label: 'Quick Trade', category: 'Actions', icon: Zap, action: 'trade' },
  
  // Shortcuts
  { id: 'short-market', label: 'Market Overview', category: 'Shortcuts', icon: TrendingUp, action: 'navigate', path: '/scanner/global' },
  { id: 'short-cash', label: 'Cash Flow', category: 'Shortcuts', icon: DollarSign, action: 'navigate', path: '/portfolio/cash-flow' },
  { id: 'short-docs', label: 'Documentation', category: 'Shortcuts', icon: FileText, action: 'docs' },
];

const CommandPalette = ({ isOpen, onClose, onThemeToggle }) => {
  const [query, setQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [serverResults, setServerResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const inputRef = useRef(null);
  const listRef = useRef(null);
  const navigate = useNavigate();

  // Initial indexing
  useEffect(() => {
    if (isOpen) {
      searchService.refreshIndex();
    }
  }, [isOpen]);

  // Debounced server search
  useEffect(() => {
    if (query.length < 3) {
      setServerResults([]);
      return;
    }

    const timer = setTimeout(async () => {
      setIsSearching(true);
      const results = await searchService.serverSearch(query);
      setServerResults(results);
      setIsSearching(false);
    }, 300);

    return () => clearTimeout(timer);
  }, [query]);

  const filteredCommands = useMemo(() => {
    const lowerQuery = query.toLowerCase();
    
    // Command filtering
    const cmds = query 
      ? COMMANDS.filter(cmd => 
          cmd.label.toLowerCase().includes(lowerQuery) ||
          cmd.category.toLowerCase().includes(lowerQuery)
        )
      : COMMANDS;

    // Dynamic filtering (Local Index)
    const localResults = searchService.localSearch(query);
    
    // Group all together
    const all = [...cmds];
    
    localResults.forEach(res => {
        const icon = res.type === 'ticker' ? BarChart3 : res.type === 'agent' ? Bot : Users;
        all.push({ ...res, icon, action: 'navigate', path: `/${res.type}/${res.id}` });
    });

    // Server results
    serverResults.forEach(res => {
        all.push({ ...res, icon: FileText, action: 'navigate', path: `/search/${res.id}` });
    });

    return all;
  }, [query, serverResults]);

  // Group by category
  const groupedCommands = useMemo(() => {
    return filteredCommands.reduce((acc, cmd) => {
      if (!acc[cmd.category]) acc[cmd.category] = [];
      acc[cmd.category].push(cmd);
      return acc;
    }, {});
  }, [filteredCommands]);

  useEffect(() => {
    if (isOpen) {
      inputRef.current?.focus();
      setQuery('');
      setSelectedIndex(0);
    }
  }, [isOpen]);

  useEffect(() => {
    setSelectedIndex(0);
  }, [query]);

  const executeCommand = (cmd) => {
    if (cmd.action === 'navigate') {
      navigate(cmd.path);
    } else if (cmd.action === 'theme') {
      onThemeToggle?.();
    }
    onClose();
  };

  const handleKeyDown = (e) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex(i => Math.min(i + 1, filteredCommands.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex(i => Math.max(i - 1, 0));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (filteredCommands[selectedIndex]) {
        executeCommand(filteredCommands[selectedIndex]);
      }
    } else if (e.key === 'Escape') {
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="command-palette-overlay" onClick={onClose}>
      <div className="command-palette animate-scale-in" onClick={e => e.stopPropagation()}>
        <div className="command-palette__header">
          <Search size={18} className={`command-palette__search-icon ${isSearching ? 'animate-pulse' : ''}`} />
          <input
            ref={inputRef}
            type="text"
            className="command-palette__input"
            placeholder="Search commands, symbols, agents (Type 3+ chars for deep search)..."
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <kbd className="command-palette__kbd">ESC</kbd>
        </div>

        <div className="command-palette__list" ref={listRef}>
          {Object.entries(groupedCommands).map(([category, commands]) => (
            <div key={category} className="command-palette__group">
              <div className="command-palette__category">{category}</div>
              {commands.map((cmd, idx) => {
                const globalIndex = filteredCommands.indexOf(cmd);
                const Icon = cmd.icon;
                return (
                  <div
                    key={cmd.id}
                    className={`command-palette__item ${globalIndex === selectedIndex ? 'command-palette__item--selected' : ''}`}
                    onClick={() => executeCommand(cmd)}
                    onMouseEnter={() => setSelectedIndex(globalIndex)}
                  >
                    <Icon size={16} className="command-palette__item-icon" />
                    <span className="command-palette__item-label">{cmd.label}</span>
                    <ArrowRight size={14} className="command-palette__item-arrow" />
                  </div>
                );
              })}
            </div>
          ))}
          
          {filteredCommands.length === 0 && !isSearching && (
            <div className="command-palette__empty">
              No results for "{query}"
            </div>
          )}
        </div>

        <div className="command-palette__footer">
          <span><kbd>↑↓</kbd> Navigate</span>
          <span><kbd>↵</kbd> Select</span>
          <span><kbd>ESC</kbd> Close</span>
        </div>
      </div>
    </div>
  );
};

export default CommandPalette;
