import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import useDepartmentStore from '../../stores/departmentStore';
import { DEPT_REGISTRY } from '../../config/departmentRegistry';
import AgentPanel from './AgentPanel';
import DepartmentMetricPanel from './DepartmentMetricPanel';
import DepartmentActivityLog from './DepartmentActivityLog';
import DepartmentViz from './DepartmentViz/DepartmentViz';
import './DepartmentDashboard.css';

/**
 * DepartmentDashboard - Reusable template for 18 department views
 */
const DepartmentDashboard = ({ deptId }) => {
  const setActiveDepartment = useDepartmentStore((state) => state.setActiveDepartment);
  const departments = useDepartmentStore((state) => state.departments);
  const pulse = useDepartmentStore((state) => state.pulse);
  const addLogEntry = useDepartmentStore((state) => state.addLogEntry);
  const department = departments[deptId];
  const registryInfo = DEPT_REGISTRY[deptId];

  if (!department || !registryInfo) {
    return (
      <div className="dept-error">
        <h1>Department {deptId} Not Found</h1>
      </div>
    );
  }

  const { color, name, icon, d3Type, description, agents, subModules } = registryInfo;

  const fetchDepartments = useDepartmentStore((state) => state.fetchDepartments);

  useEffect(() => {
    setActiveDepartment(deptId);
    fetchDepartments(); // Ensure we have the latest agent status and metrics
    
    return () => {
      setActiveDepartment(null);
    };
  }, [deptId, setActiveDepartment, fetchDepartments]);

  const handleWorkflowExecute = async (workflow) => {
    addLogEntry(deptId, {
      type: 'workflow_start',
      message: `Executing workflow: ${workflow.label}`,
      payload: workflow
    });

    try {
      if (workflow.action === 'invoke_agent' && workflow.agentId) {
        await useDepartmentStore.getState().invokeAgent(deptId, workflow.agentId, {
          trigger: 'manual_workflow',
          workflow_id: workflow.id
        });
      } else {
        // Generic system action or placeholder
        setTimeout(() => {
          addLogEntry(deptId, {
            type: 'workflow_complete',
            message: `Workflow ${workflow.label} completed successfully.`
          });
        }, 1000);
      }
    } catch (err) {
      console.error('Workflow failed:', err);
    }
  };

  return (
    <div className="dept-dashboard-container" style={{ '--dept-color': color }}>
      {/* Main Grid Layout */}
      <div className="dept-grid">
        {/* Left: Agent Fleet */}
        <aside className="dept-sidebar">
          <AgentPanel agents={registryInfo.agents} deptId={deptId} />
        </aside>

        {/* Center: D3 Visualization Area */}
        <main className="dept-main-viz">
          <div className="viz-scroll-area">
            <div className="viz-placeholder">
              <div className="viz-header">
                <h3>{d3Type.toUpperCase()} VISUALIZATION</h3>
                <span className="viz-status">LIVE STREAM POLLING</span>
              </div>
              <div className="viz-content">
                <DepartmentViz 
                  type={d3Type} 
                  color={color} 
                  deptId={deptId}
                  agents={department?.agents || agents}
                />
              </div>
            </div>

            <DepartmentActivityLog 
              deptId={deptId} 
              color={color} 
            />
          </div>
        </main>

        {/* Right/Bottom: Metrics & Pulse */}
        <section className="dept-metrics-area">
          <DepartmentMetricPanel 
            metrics={department.metrics} 
            primaryMetric={registryInfo.primaryMetric}
            primaryLabel={registryInfo.primaryMetricLabel}
            unit={registryInfo.primaryMetricUnit}
            pulse={pulse}
            workflows={registryInfo.workflows}
            onWorkflowExecute={handleWorkflowExecute}
          />
        </section>
      </div>

    </div>
  );
};

export default DepartmentDashboard;
