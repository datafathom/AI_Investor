import React from 'react';

const PRIORITIES = [
  { id: 'CRITICAL', color: '#ff4757', label: 'CRITICAL' },
  { id: 'HIGH', color: '#ffa502', label: 'HIGH' },
  { id: 'MEDIUM', color: '#eccc68', label: 'MEDIUM' },
  { id: 'LOW', color: '#00f2ff', label: 'LOW' }
];

const PriorityFilter = ({ activeFilters, onToggle }) => {
  return (
    <div className="priority-filter-bar">
      <span className="filter-label">FILTER_PRIORITY:</span>
      <div className="filter-group">
        {PRIORITIES.map(p => {
          const isActive = activeFilters.includes(p.id);
          return (
            <button
              key={p.id}
              className={`filter-btn ${isActive ? 'active' : ''}`}
              onClick={() => onToggle(p.id)}
              style={{
                '--glow-color': p.color,
                '--btn-opacity': isActive ? '1' : '0.3',
                borderColor: isActive ? p.color : 'rgba(255,255,255,0.1)',
                color: isActive ? '#fff' : '#666'
              }}
            >
              <div className="btn-indicator" style={{ background: p.color }} />
              {p.label}
            </button>
          );
        })}
      </div>

      <style jsx="true">{`
        .priority-filter-bar {
          display: flex;
          align-items: center;
          gap: 15px;
          padding: 8px 15px;
          background: rgba(0, 0, 0, 0.3);
          border-bottom: 1px solid #1a1a1a;
        }
        .filter-label {
          font-size: 0.65rem;
          color: #555;
          font-weight: 800;
          letter-spacing: 0.05em;
        }
        .filter-group {
          display: flex;
          gap: 10px;
        }
        .filter-btn {
          position: relative;
          padding: 4px 12px;
          font-size: 0.7rem;
          font-weight: 900;
          background: rgba(255, 255, 255, 0.02);
          border: 1px solid transparent;
          cursor: pointer;
          transition: all 0.2s ease;
          display: flex;
          align-items: center;
          gap: 6px;
          text-transform: uppercase;
          clip-path: polygon(10% 0, 100% 0, 100% 70%, 90% 100%, 0 100%, 0 30%);
        }
        .filter-btn:hover {
          background: rgba(255, 255, 255, 0.05);
          opacity: 1;
        }
        .filter-btn.active {
          box-shadow: 0 0 10px var(--glow-color);
          background: color-mix(in srgb, var(--glow-color) 10%, transparent);
        }
        .btn-indicator {
          width: 6px;
          height: 6px;
          border-radius: 1px;
        }
      `}</style>
    </div>
  );
};

export default PriorityFilter;
