# Phase 5: Advanced D3.js Visualizations

> **Duration**: 4 Weeks  
> **Status**: [ ] Not Started  
> **Dependencies**: Phase 2 Complete  
> **Owner**: TBD  

---

## Phase Overview

Implement all 18 department-specific D3.js visualizations with reusable React hooks and 60fps performance targets. This phase covers force graphs, Sankey diagrams, sunbursts, 3D surfaces, and more.

---

## Deliverables Checklist

### 5.1 D3 React Hook
- [ ] `useD3.js` hook implemented
- [ ] Cleanup prevents memory leaks
- [ ] Works with SVG and Canvas

### 5.2 Visualization Components (11 Total)
- [ ] ForceGraph.jsx (Depts 1, 3, 7, 13, 14, 17)
- [ ] Sunburst.jsx (Depts 2, 9, 12)
- [ ] SankeyFlow.jsx (Depts 10, 18)
- [ ] RadialTree.jsx (Depts 11, 13)
- [ ] BubbleChart.jsx (Depts 5, 7)
- [ ] Flowchart.jsx (Dept 4)
- [ ] Timeline.jsx (Dept 15)
- [ ] FractalTree.jsx (Dept 16)
- [ ] VolatilitySurface.jsx (Dept 6) - Three.js
- [ ] GlobeMesh.jsx (Dept 8) - Three.js
- [ ] SpiderWeb.jsx (Dept 3)

### 5.3 Storybook Stories
- [ ] All visualizations have Storybook stories
- [ ] Mock data provided

### 5.4 Performance Optimization
- [ ] All visualizations hit 60fps target
- [ ] Canvas fallback for high-density graphs

---

## Deliverable 5.1: D3 React Hook

### File Location
`frontend/src/hooks/useD3.js`

```javascript
import { useRef, useEffect, useCallback } from 'react';
import * as d3 from 'd3';

/**
 * Custom hook for D3.js integration with React
 * 
 * @param {Function} renderFn - D3 render function receiving svg selection
 * @param {Array} dependencies - Effect dependency array
 * @returns {React.RefObject} - Ref to attach to SVG element
 */
export const useD3 = (renderFn, dependencies = []) => {
  const ref = useRef(null);
  
  useEffect(() => {
    if (!ref.current) return;
    
    const svg = d3.select(ref.current);
    
    // Clear previous content
    svg.selectAll('*').remove();
    
    // Execute render function
    renderFn(svg);
    
    // Cleanup on unmount or dependency change
    return () => {
      svg.selectAll('*').remove();
    };
  }, dependencies);
  
  return ref;
};

/**
 * Hook for responsive D3 visualizations
 */
export const useD3Responsive = (renderFn, dependencies = []) => {
  const containerRef = useRef(null);
  const svgRef = useRef(null);
  
  const resizeHandler = useCallback(() => {
    if (!containerRef.current || !svgRef.current) return;
    
    const { width, height } = containerRef.current.getBoundingClientRect();
    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height);
    
    svg.selectAll('*').remove();
    renderFn(svg, { width, height });
  }, [renderFn]);
  
  useEffect(() => {
    resizeHandler();
    
    const resizeObserver = new ResizeObserver(resizeHandler);
    if (containerRef.current) {
      resizeObserver.observe(containerRef.current);
    }
    
    return () => resizeObserver.disconnect();
  }, dependencies);
  
  return { containerRef, svgRef };
};

export default useD3;
```

---

## Deliverable 5.2: Visualization Components

### ForceGraph.jsx (Neural Net, Correlation Web)

```jsx
// components/D3Visualizations/ForceGraph.jsx
import React, { useMemo } from 'react';
import * as d3 from 'd3';
import { useD3Responsive } from '@/hooks/useD3';
import styles from './D3Visualization.module.css';

export const ForceGraph = ({ 
  nodes = [], 
  links = [],
  nodeColor,
  onNodeClick,
  options = {}
}) => {
  const renderGraph = useMemo(() => (svg, dimensions) => {
    const { width, height } = dimensions;
    const centerX = width / 2;
    const centerY = height / 2;
    
    // Create simulation
    const simulation = d3.forceSimulation(nodes)
      .force('link', d3.forceLink(links).id(d => d.id).distance(100))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(centerX, centerY))
      .force('collision', d3.forceCollide().radius(30));
    
    // Draw links
    const link = svg.append('g')
      .attr('class', 'links')
      .selectAll('line')
      .data(links)
      .join('line')
      .attr('stroke', 'var(--border-primary)')
      .attr('stroke-opacity', 0.6)
      .attr('stroke-width', d => Math.sqrt(d.value) || 1);
    
    // Draw nodes
    const node = svg.append('g')
      .attr('class', 'nodes')
      .selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', d => d.size || 10)
      .attr('fill', d => nodeColor?.(d) || d.color || '#00f2ff')
      .attr('stroke', 'var(--bg-primary)')
      .attr('stroke-width', 2)
      .style('cursor', 'pointer')
      .call(drag(simulation));
    
    // Labels
    const label = svg.append('g')
      .attr('class', 'labels')
      .selectAll('text')
      .data(nodes)
      .join('text')
      .text(d => d.label || d.id)
      .attr('font-size', 10)
      .attr('fill', 'var(--text-secondary)')
      .attr('text-anchor', 'middle')
      .attr('dy', -15);
    
    // Tick handler
    simulation.on('tick', () => {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);
      
      node
        .attr('cx', d => d.x)
        .attr('cy', d => d.y);
      
      label
        .attr('x', d => d.x)
        .attr('y', d => d.y);
    });
    
    // Click handler
    if (onNodeClick) {
      node.on('click', (event, d) => {
        event.stopPropagation();
        onNodeClick(d);
      });
    }
    
    // Hover effects
    node
      .on('mouseover', function(event, d) {
        d3.select(this)
          .transition()
          .duration(200)
          .attr('r', (d.size || 10) * 1.5);
      })
      .on('mouseout', function(event, d) {
        d3.select(this)
          .transition()
          .duration(200)
          .attr('r', d.size || 10);
      });
    
    return () => simulation.stop();
  }, [nodes, links, nodeColor, onNodeClick]);
  
  const { containerRef, svgRef } = useD3Responsive(renderGraph, [nodes, links]);
  
  return (
    <div ref={containerRef} className={styles.container}>
      <svg ref={svgRef} className={styles.svg} />
    </div>
  );
};

// Drag behavior
function drag(simulation) {
  function dragstarted(event) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    event.subject.fx = event.subject.x;
    event.subject.fy = event.subject.y;
  }
  
  function dragged(event) {
    event.subject.fx = event.x;
    event.subject.fy = event.y;
  }
  
  function dragended(event) {
    if (!event.active) simulation.alphaTarget(0);
    event.subject.fx = null;
    event.subject.fy = null;
  }
  
  return d3.drag()
    .on('start', dragstarted)
    .on('drag', dragged)
    .on('end', dragended);
}

export default ForceGraph;
```

### SankeyFlow.jsx (Liquidity River)

```jsx
// components/D3Visualizations/SankeyFlow.jsx
import React, { useMemo } from 'react';
import * as d3 from 'd3';
import { sankey, sankeyLinkHorizontal } from 'd3-sankey';
import { useD3Responsive } from '@/hooks/useD3';
import styles from './D3Visualization.module.css';

export const SankeyFlow = ({ 
  nodes = [],
  links = [],
  onNodeClick,
  options = {}
}) => {
  const renderSankey = useMemo(() => (svg, { width, height }) => {
    const margin = { top: 20, right: 20, bottom: 20, left: 20 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;
    
    const g = svg.append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);
    
    // Create Sankey generator
    const sankeyGenerator = sankey()
      .nodeWidth(15)
      .nodePadding(10)
      .extent([[0, 0], [innerWidth, innerHeight]]);
    
    const { nodes: sankeyNodes, links: sankeyLinks } = sankeyGenerator({
      nodes: nodes.map(d => ({ ...d })),
      links: links.map(d => ({ ...d }))
    });
    
    // Color scale
    const colorScale = d3.scaleOrdinal()
      .domain(['income', 'reservoir', 'expense'])
      .range(['#22c55e', '#3b82f6', '#ef4444']);
    
    // Draw links
    g.append('g')
      .attr('fill', 'none')
      .selectAll('path')
      .data(sankeyLinks)
      .join('path')
      .attr('d', sankeyLinkHorizontal())
      .attr('stroke', d => colorScale(d.source.type))
      .attr('stroke-opacity', 0.5)
      .attr('stroke-width', d => Math.max(1, d.width))
      .on('mouseover', function() {
        d3.select(this).attr('stroke-opacity', 0.8);
      })
      .on('mouseout', function() {
        d3.select(this).attr('stroke-opacity', 0.5);
      });
    
    // Draw nodes
    g.append('g')
      .selectAll('rect')
      .data(sankeyNodes)
      .join('rect')
      .attr('x', d => d.x0)
      .attr('y', d => d.y0)
      .attr('height', d => d.y1 - d.y0)
      .attr('width', d => d.x1 - d.x0)
      .attr('fill', d => colorScale(d.type))
      .attr('stroke', 'var(--bg-primary)')
      .style('cursor', 'pointer')
      .on('click', (event, d) => onNodeClick?.(d));
    
    // Node labels
    g.append('g')
      .selectAll('text')
      .data(sankeyNodes)
      .join('text')
      .attr('x', d => d.x0 < innerWidth / 2 ? d.x1 + 6 : d.x0 - 6)
      .attr('y', d => (d.y1 + d.y0) / 2)
      .attr('dy', '0.35em')
      .attr('text-anchor', d => d.x0 < innerWidth / 2 ? 'start' : 'end')
      .attr('fill', 'var(--text-primary)')
      .attr('font-size', 11)
      .text(d => d.name);
    
    // Value labels
    g.append('g')
      .selectAll('text.value')
      .data(sankeyNodes)
      .join('text')
      .attr('class', 'value')
      .attr('x', d => (d.x0 + d.x1) / 2)
      .attr('y', d => d.y0 - 5)
      .attr('text-anchor', 'middle')
      .attr('fill', 'var(--text-secondary)')
      .attr('font-size', 9)
      .text(d => `$${d.value?.toLocaleString()}`);
  }, [nodes, links, onNodeClick]);
  
  const { containerRef, svgRef } = useD3Responsive(renderSankey, [nodes, links]);
  
  return (
    <div ref={containerRef} className={styles.container}>
      <svg ref={svgRef} className={styles.svg} />
    </div>
  );
};

export default SankeyFlow;
```

### Sunburst.jsx (Life-Tree, Asset Tree, Ledger)

```jsx
// components/D3Visualizations/Sunburst.jsx
import React, { useMemo } from 'react';
import * as d3 from 'd3';
import { useD3Responsive } from '@/hooks/useD3';
import styles from './D3Visualization.module.css';

export const Sunburst = ({ 
  data,
  onArcClick,
  colorScale,
  options = {}
}) => {
  const renderSunburst = useMemo(() => (svg, { width, height }) => {
    const radius = Math.min(width, height) / 2;
    
    const g = svg.append('g')
      .attr('transform', `translate(${width / 2},${height / 2})`);
    
    // Create hierarchy
    const root = d3.hierarchy(data)
      .sum(d => d.value)
      .sort((a, b) => b.value - a.value);
    
    // Partition layout
    const partition = d3.partition()
      .size([2 * Math.PI, radius]);
    
    partition(root);
    
    // Arc generator
    const arc = d3.arc()
      .startAngle(d => d.x0)
      .endAngle(d => d.x1)
      .innerRadius(d => d.y0)
      .outerRadius(d => d.y1);
    
    // Color scale
    const color = colorScale || d3.scaleOrdinal(d3.schemeCategory10);
    
    // Draw arcs
    g.selectAll('path')
      .data(root.descendants())
      .join('path')
      .attr('d', arc)
      .attr('fill', d => {
        let node = d;
        while (node.depth > 1) node = node.parent;
        return color(node.data.name);
      })
      .attr('fill-opacity', d => 0.9 - d.depth * 0.1)
      .attr('stroke', 'var(--bg-primary)')
      .attr('stroke-width', 1)
      .style('cursor', 'pointer')
      .on('click', (event, d) => onArcClick?.(d))
      .on('mouseover', function(event, d) {
        d3.select(this).attr('fill-opacity', 1);
        showTooltip(event, d);
      })
      .on('mouseout', function() {
        d3.select(this).attr('fill-opacity', d => 0.9 - d.depth * 0.1);
        hideTooltip();
      });
    
    // Center label
    g.append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .attr('fill', 'var(--text-primary)')
      .attr('font-size', 14)
      .attr('font-weight', 600)
      .text(data.name);
    
    function showTooltip(event, d) {
      // Tooltip implementation
    }
    
    function hideTooltip() {
      // Hide tooltip
    }
  }, [data, colorScale, onArcClick]);
  
  const { containerRef, svgRef } = useD3Responsive(renderSunburst, [data]);
  
  return (
    <div ref={containerRef} className={styles.container}>
      <svg ref={svgRef} className={styles.svg} />
    </div>
  );
};

export default Sunburst;
```

### VolatilitySurface.jsx (3D with Three.js)

```jsx
// components/D3Visualizations/three/VolatilitySurface.jsx
import React, { useMemo, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text } from '@react-three/drei';
import * as THREE from 'three';

export const VolatilitySurface = ({ data, options = {} }) => {
  return (
    <div style={{ width: '100%', height: '100%' }}>
      <Canvas camera={{ position: [3, 3, 3], fov: 50 }}>
        <ambientLight intensity={0.4} />
        <pointLight position={[10, 10, 10]} />
        <Surface data={data} />
        <OrbitControls enablePan enableZoom enableRotate />
        <AxisLabels />
      </Canvas>
    </div>
  );
};

const Surface = ({ data }) => {
  const meshRef = useRef();
  
  const geometry = useMemo(() => {
    const width = 100;
    const height = 100;
    const geom = new THREE.PlaneGeometry(2, 2, width - 1, height - 1);
    
    const positions = geom.attributes.position.array;
    for (let i = 0; i < positions.length; i += 3) {
      const x = positions[i];
      const y = positions[i + 1];
      // Z = implied volatility based on strike (x) and time (y)
      positions[i + 2] = data?.[Math.floor(i / 3)]?.iv || Math.sin(x * 3) * Math.cos(y * 2) * 0.3;
    }
    
    geom.computeVertexNormals();
    return geom;
  }, [data]);
  
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.z += 0.001;
    }
  });
  
  return (
    <mesh ref={meshRef} geometry={geometry} rotation={[-Math.PI / 2, 0, 0]}>
      <meshPhongMaterial 
        color="#00f2ff"
        wireframe
        side={THREE.DoubleSide}
      />
    </mesh>
  );
};

const AxisLabels = () => (
  <>
    <Text position={[1.5, 0, 0]} fontSize={0.1} color="white">Strike</Text>
    <Text position={[0, 0, 1.5]} fontSize={0.1} color="white">Expiry</Text>
    <Text position={[0, 1.2, 0]} fontSize={0.1} color="white">IV</Text>
  </>
);

export default VolatilitySurface;
```

---

## Performance Targets

| Visualization | Data Points | Target FPS | Strategy |
|---------------|-------------|------------|----------|
| ForceGraph | 1000 nodes | 60 fps | Canvas fallback |
| Sunburst | 500 slices | 60 fps | SVG |
| SankeyFlow | 50 flows | 60 fps | SVG |
| VolatilitySurface | 10000 vertices | 60 fps | WebGL |
| Timeline | 10 years | 60 fps | Virtual scroll |

---

## E2E Definition of Done

1. **Render**: Each visualization loads with mock data
2. **Performance**: Chrome DevTools shows 60fps during interaction
3. **Resize**: Visualizations respond to container resize
4. **Export**: Right-click → Export PNG works
5. **Theme**: Dark/light themes display correctly
6. **Storybook**: Each has a story with controls

---

## Phase Sign-Off

- [ ] useD3 hook tested and documented
- [ ] All 11 visualization components complete  
- [ ] Performance targets met
- [ ] Storybook stories created
- [ ] No memory leaks (heap snapshot verified)
