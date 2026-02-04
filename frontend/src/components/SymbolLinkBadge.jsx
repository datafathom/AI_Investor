import React, { useState } from 'react';
import './SymbolLinkBadge.css';

const SymbolLinkBadge = ({ group, onGroupChange }) => {
  const [isOpen, setIsOpen] = useState(false);
  
  const groups = [
    { id: 'red', label: 'Red Group', color: '#ff4757' },
    { id: 'blue', label: 'Blue Group', color: '#1e90ff' },
    { id: 'green', label: 'Green Group', color: '#2ed573' },
    { id: 'none', label: 'Unlinked', color: '#a4b0be' }
  ];

  const currentGroup = groups.find(g => g.id === group) || groups[3];

  return (
    <div className="symbol-link-badge-container">
      <div 
        className={`link-dot ${group}`}
        title={`Group: ${currentGroup.label}`}
        onClick={() => setIsOpen(!isOpen)}
        style={{ backgroundColor: currentGroup.color }}
      />
      
      {isOpen && (
        <div className="link-dropdown">
          {groups.map(g => (
            <div 
              key={g.id}
              className={`link-option ${g.id === group ? 'active' : ''}`}
              onClick={() => {
                onGroupChange(g.id);
                setIsOpen(false);
              }}
            >
              <span className="option-dot" style={{ backgroundColor: g.color }} />
              {g.label}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SymbolLinkBadge;
