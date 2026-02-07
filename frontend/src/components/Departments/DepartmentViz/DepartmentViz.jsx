import React, { useMemo } from 'react';
import ForceGraph from './ForceGraph';
import BubbleChart from './BubbleChart';
import RadialTree from './RadialTree';
import FlowChart from './FlowChart';
import Sunburst from './Sunburst';
import Sankey from './Sankey';
import Timeline from './Timeline';
import GlobeMesh from './GlobeMesh';
import ThreeDSurface from './ThreeDSurface';
import Fractal from './Fractal';
import useVisibility from '../../../hooks/useVisibility';
import { D3_TYPES } from '../../../config/departmentRegistry';

/**
 * DepartmentViz - Factory for D3 visualizations
 */
const DepartmentViz = ({ type, color, deptId, agents = [] }) => {
  const [containerRef, isVisible] = useVisibility();
  
  // Dynamic Data Generators
  const forceData = useMemo(() => {
    if (!agents || agents.length === 0) return { nodes: [], links: [] };
    
    // 1. Central Hub
    const nodes = [{ id: 'CORE', val: 10, group: 'hub' }];
    const links = [];

    // 2. Agent Nodes
    agents.forEach((agent, idx) => {
      const agentId = typeof agent === 'string' ? agent : agent.agent_id;
      const agentStatus = typeof agent === 'string' ? 'idle' : agent.status;
      
      nodes.push({ 
        id: agentId, 
        val: 5, 
        group: 'agent',
        status: agentStatus 
      });
      
      links.push({ 
        source: agentId, 
        target: 'CORE', 
        value: 3 
      });
    });

    return { nodes, links };
  }, [agents]);

  const bubbleData = useMemo(() => [
    { name: 'Alpha-1', value: 400 },
    { name: 'Beta-Scan', value: 300 },
    { name: 'Gamma-Ray', value: 200 },
    { name: 'Delta-Force', value: 150 },
    { name: 'Epsilon-Scout', value: 100 }
  ], []);

  const treeData = useMemo(() => ({
    name: "Root",
    children: [
      { name: "Branch A", children: [{ name: "Leaf A1" }, { name: "Leaf A2" }] },
      { name: "Branch B", children: [{ name: "Leaf B1" }, { name: "Leaf B2" }, { name: "Leaf B3" }] },
      { name: "Branch C", children: [{ name: "Leaf C1" }] }
    ]
  }), []);

  const flowData = useMemo(() => ({
    nodes: [
      { id: '1', name: 'Input' }, { id: '2', name: 'Process' }, { id: '3', name: 'Verify' },
      { id: '4', name: 'Store' }, { id: '5', name: 'Output' }
    ],
    links: [
      { source: '1', target: '2' }, { source: '2', target: '3' },
      { source: '3', target: '4' }, { source: '4', target: '5' }
    ]
  }), []);

  const renderViz = () => {
    switch (type) {
      case D3_TYPES.FORCE_GRAPH:
        return <ForceGraph data={forceData} color={color} isVisible={isVisible} />;
      case D3_TYPES.BUBBLE_CHART:
        return <BubbleChart data={bubbleData} color={color} isVisible={isVisible} />;
      case D3_TYPES.RADIAL_TREE:
        return <RadialTree data={treeData} color={color} isVisible={isVisible} />;
      case D3_TYPES.FLOWCHART:
        return <FlowChart data={flowData} color={color} isVisible={isVisible} />;
      case D3_TYPES.SANKEY:
        return <Sankey color={color} isVisible={isVisible} />;
      case D3_TYPES.SUNBURST:
        return <Sunburst color={color} isVisible={isVisible} />;
      case D3_TYPES.TIMELINE:
        return <Timeline color={color} isVisible={isVisible} />;
      case D3_TYPES.THREE_D_SURFACE:
        return <ThreeDSurface color={color} isVisible={isVisible} />;
      case D3_TYPES.GLOBE_MESH:
        return <GlobeMesh color={color} isVisible={isVisible} />;
      case D3_TYPES.FRACTAL:
        return <Fractal color={color} isVisible={isVisible} />;
      default:
        return (
          <div className="viz-fallback" style={{ color: '#444', textAlign: 'center' }}>
            <p>SPEC: {type?.toUpperCase() || 'UNKNOWN'}</p>
            <p style={{ fontSize: '10px' }}>D3 Engine Initializing...</p>
          </div>
        );
    }
  };

  return (
    <div ref={containerRef} className="dept-viz-container" style={{ width: '100%', height: '100%', minHeight: '400px' }}>
      {renderViz()}
    </div>
  );
};

export default React.memo(DepartmentViz);
