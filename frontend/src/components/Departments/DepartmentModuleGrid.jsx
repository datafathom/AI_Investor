import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ExternalLink, ChevronRight } from 'lucide-react';
import './DepartmentModuleGrid.css';

const DepartmentModuleGrid = ({ subModules = [], color = "#00f2ff" }) => {
  const navigate = useNavigate();

  if (!subModules || subModules.length === 0) return null;

  return (
    <div className="dept-module-grid-container">
      <div className="dept-grid-header">
        <h3 style={{ color }}>CORE CAPABILITIES</h3>
        <span className="dept-grid-subtitle">SUB-MODULE ACCESS LAYER</span>
      </div>
      
      <div className="dept-module-grid">
        {subModules.map((module, idx) => (
          <div 
            key={idx} 
            className="dept-module-card"
            onClick={() => navigate(module.path)}
            style={{ "--accent": color }}
          >
            <div className="module-card-glow" />
            <div className="module-card-content">
              <div className="module-info">
                <h4>{module.label}</h4>
                <p>{module.description}</p>
              </div>
              <div className="module-action">
                <ChevronRight size={18} />
              </div>
            </div>
            <div className="module-card-border" />
          </div>
        ))}
      </div>
    </div>
  );
};

export default DepartmentModuleGrid;
