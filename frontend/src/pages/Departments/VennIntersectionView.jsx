import React, { useMemo } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useDepartmentStore } from '../../stores/departmentStore';
import { useShallow } from 'zustand/react/shallow';
import { DEPT_REGISTRY } from '../../config/departmentRegistry';
import { getIcon } from '../../config/iconRegistry';
import AgentPanel from '../../components/Departments/AgentPanel';
import DepartmentViz from '../../components/Departments/DepartmentViz/DepartmentViz';
import { ArrowLeft, Link2 } from 'lucide-react';
import './VennIntersectionView.css';

/**
 * VennIntersectionView - Blended view of two combined departments
 * URL: /dept/venn?d1={deptId1}&d2={deptId2}
 */
const VennIntersectionView = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  
  const { departments, exitVennMode } = useDepartmentStore(useShallow(state => ({
    departments: state.departments,
    exitVennMode: state.exitVennMode
  })));
  
  // Parse department IDs from URL
  const dept1Id = parseInt(searchParams.get('d1') || '0', 10);
  const dept2Id = parseInt(searchParams.get('d2') || '0', 10);
  
  const dept1 = DEPT_REGISTRY[dept1Id];
  const dept2 = DEPT_REGISTRY[dept2Id];
  const dept1Data = departments[dept1Id];
  const dept2Data = departments[dept2Id];
  
  // Blend colors for header gradient
  const blendedGradient = useMemo(() => {
    if (!dept1 || !dept2) return 'linear-gradient(135deg, #333, #555)';
    return `linear-gradient(135deg, ${dept1.color}, ${dept2.color})`;
  }, [dept1, dept2]);
  
  // Combined agents from both departments
  const combinedAgents = useMemo(() => {
    const agents1 = dept1Data?.agents || [];
    const agents2 = dept2Data?.agents || [];
    return [
      ...agents1.map(a => ({ ...a, fromDept: dept1Id })),
      ...agents2.map(a => ({ ...a, fromDept: dept2Id }))
    ];
  }, [dept1Data, dept2Data, dept1Id, dept2Id]);
  
  const handleBack = () => {
    exitVennMode();
    navigate('/special/scrum');
  };
  
  if (!dept1 || !dept2) {
    return (
      <div className="venn-view-error">
        <h2>Invalid Venn Configuration</h2>
        <p>Please select two valid departments to combine.</p>
        <button onClick={() => navigate('/special/scrum')}>
          Return to Scrum Master
        </button>
      </div>
    );
  }
  
  const Dept1Icon = getIcon(dept1.icon);
  const Dept2Icon = getIcon(dept2.icon);
  
  return (
    <div className="venn-intersection-view">
      {/* Blended Header */}
      <header className="venn-header" style={{ background: blendedGradient }}>
        <button className="venn-back-btn" onClick={handleBack}>
          <ArrowLeft size={20} />
          Back to Scrum
        </button>
        
        <div className="venn-title-group">
          <div className="venn-dept-badge" style={{ borderColor: dept1.color }}>
            <Dept1Icon size={24} />
            <span>{dept1.name}</span>
          </div>
          
          <Link2 size={28} className="venn-link-icon" />
          
          <div className="venn-dept-badge" style={{ borderColor: dept2.color }}>
            <Dept2Icon size={24} />
            <span>{dept2.name}</span>
          </div>
        </div>
        
        <div className="venn-mode-label">VENN INTERSECTION MODE</div>
      </header>
      
      {/* Main Content Grid */}
      <div className="venn-content-grid">
        {/* Left Panel: Combined Agents */}
        <section className="venn-agents-panel">
          <h3>Combined Agent Team ({combinedAgents.length})</h3>
          <div className="venn-agents-list">
            {combinedAgents.map((agent, idx) => (
              <div 
                key={agent.id || idx} 
                className="venn-agent-item"
                style={{ 
                  borderLeftColor: agent.fromDept === dept1Id ? dept1.color : dept2.color 
                }}
              >
                <span className="agent-name">{agent.name || agent.id}</span>
                <span className="agent-role">{agent.role}</span>
              </div>
            ))}
          </div>
        </section>
        
        {/* Right Panel: Dual Visualizations */}
        <section className="venn-viz-panel">
          <div className="viz-stack">
            <div className="viz-container" style={{ borderColor: dept1.color }}>
              <h4>{dept1.name} View</h4>
              <DepartmentViz 
                departmentId={dept1Id}
                d3Type={dept1.d3Type}
                color={dept1.color}
              />
            </div>
            <div className="viz-container" style={{ borderColor: dept2.color }}>
              <h4>{dept2.name} View</h4>
              <DepartmentViz 
                departmentId={dept2Id}
                d3Type={dept2.d3Type}
                color={dept2.color}
              />
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default VennIntersectionView;
