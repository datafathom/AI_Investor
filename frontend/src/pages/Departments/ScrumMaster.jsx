import React, { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { DEPT_REGISTRY } from '../../config/departmentRegistry';
import { getIcon } from '../../config/iconRegistry';
import { ChevronRight, Link2 } from 'lucide-react';
import useDepartmentStore from '../../stores/departmentStore';
import GlobalActionsBar from '../../components/Departments/GlobalActionsBar';
import './ScrumMaster.css';

const QUADRANTS = [
  {
    id: 'attack',
    name: 'ATTACK ENGINE',
    depts: [3, 4, 5, 6, 7]
  },
  {
    id: 'defense',
    name: 'DEFENSE FORTRESS',
    depts: [8, 10, 11, 12]
  },
  {
    id: 'household',
    name: 'HOUSEHOLD',
    depts: [9, 13, 14, 18]
  },
  {
    id: 'meta',
    name: 'META-COGNITION',
    depts: [1, 2, 15, 16, 17]
  }
];

const ScrumMaster = () => {
  const navigate = useNavigate();
  const triggerVennMode = useDepartmentStore(state => state.triggerVennMode);
  
  // Drag state for Venn intersection
  const [draggedDept, setDraggedDept] = useState(null);
  const [dropTarget, setDropTarget] = useState(null);

  const handleDragStart = useCallback((e, deptId) => {
    setDraggedDept(deptId);
    e.dataTransfer.effectAllowed = 'link';
    e.dataTransfer.setData('text/plain', deptId.toString());
  }, []);

  const handleDragOver = useCallback((e, deptId) => {
    e.preventDefault();
    if (draggedDept && draggedDept !== deptId) {
      setDropTarget(deptId);
    }
  }, [draggedDept]);

  const handleDragLeave = useCallback(() => {
    setDropTarget(null);
  }, []);

  const handleDrop = useCallback((e, targetDeptId) => {
    e.preventDefault();
    if (draggedDept && draggedDept !== targetDeptId) {
      // Trigger Venn mode and navigate
      triggerVennMode(draggedDept, targetDeptId);
      navigate(`/dept/venn?d1=${draggedDept}&d2=${targetDeptId}`);
    }
    setDraggedDept(null);
    setDropTarget(null);
  }, [draggedDept, triggerVennMode, navigate]);

  const handleDragEnd = useCallback(() => {
    setDraggedDept(null);
    setDropTarget(null);
  }, []);

  const handleGlobalAction = useCallback((action) => {
    console.log(`Global Action Triggered: ${action.label}`);
    // Logic for Panic, Cold Haven, etc.
    if (action.id === 'panic') {
      // Navigate to terminal or trigger global event
      navigate('/special/terminal');
    }
    // Shared toast or confirmation logic can be added here
  }, [navigate]);

  return (
    <div className="scrum-master-container os-integrated">
      {/* Venn Hint */}
      {draggedDept && (
        <div className="venn-hint">
          <Link2 size={16} />
          Drop on another department to create Venn view
        </div>
      )}
      
      <div className="scrum-grid">
        {QUADRANTS.map(quad => (
          <div key={quad.id} className={`quadrant-panel ${quad.id}`}>
            <h2 className="quadrant-title">{quad.name}</h2>
            <div className="dept-list">
              {quad.depts.map(deptId => {
                const dept = DEPT_REGISTRY[deptId];
                if (!dept) return null;
                const DeptIcon = getIcon(dept.icon);
                const isDragging = draggedDept === deptId;
                const isDropTarget = dropTarget === deptId;
                
                return (
                  <div 
                    key={deptId} 
                    className={`dept-card ${isDragging ? 'dragging' : ''} ${isDropTarget ? 'drop-target' : ''}`}
                    onClick={() => !draggedDept && navigate(dept.route)}
                    draggable
                    onDragStart={(e) => handleDragStart(e, deptId)}
                    onDragOver={(e) => handleDragOver(e, deptId)}
                    onDragLeave={handleDragLeave}
                    onDrop={(e) => handleDrop(e, deptId)}
                    onDragEnd={handleDragEnd}
                  >
                    <div className="dept-icon">
                      <DeptIcon size={24} />
                    </div>
                    <div className="dept-info">
                      <span className="dept-name">{dept.name}</span>
                      <div className="dept-status">
                         <span className="status-dot online"></span>
                         <span className="status-text">OPERATIONAL</span>
                      </div>
                    </div>
                    <div className="dept-chevron">
                      <ChevronRight size={16} />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      <GlobalActionsBar onAction={handleGlobalAction} />
    </div>
  );
};

export default ScrumMaster;
