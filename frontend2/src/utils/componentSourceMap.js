/**
 * Component Source Code Map
 * 
 * Maps widget IDs to their example source code for the "View Source" feature.
 * This allows developers to see how each widget is implemented.
 */

export const COMPONENT_SOURCE_MAP = {
  'api': `import React, { useState, useEffect } from 'react';
import apiClient from './services/apiClient';

export default function ApiIntegration() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
    try {
      const response = await apiClient.get('/example');
      setData(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <button onClick={fetchData}>Fetch Data</button>
      {loading && <p>Loading...</p>}
      {error && <p>Error: {error}</p>}
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
    </div>
  );
}`,

  'palette': `import React from 'react';
import { useColorPalette } from '../hooks/useColorPalette';

export default function ColorSystem() {
  const { palette } = useColorPalette();
  
  const COLOR_TOKENS = [
    { label: 'Burgundy / Primary', path: ['burgundy', 'primary'] },
    { label: 'Burgundy / Accent', path: ['burgundy', 'accent'] },
    { label: 'Burgundy / Dark', path: ['burgundy', 'dark'] },
    { label: 'Cream / Primary', path: ['cream', 'primary'] },
    { label: 'Cream / Medium', path: ['cream', 'medium'] },
    { label: 'Text / On Burgundy', path: ['text', 'on_burgundy'] },
  ];

  return (
    <div className="palette-swatches">
      {COLOR_TOKENS.map((token) => {
        const value = token.path.reduce((acc, key) => acc?.[key], palette) || '--';
        const cssVar = \`--color-\${token.path.join('-')}\`;
        return (
          <div key={token.label} className="palette-swatch">
            <span className="swatch-dot" style={{ backgroundColor: value }} />
            <div>
              <p>{token.label}</p>
              <small>CSS: var(\${cssVar})</small>
              <small>Value: {value}</small>
            </div>
          </div>
        );
      })}
    </div>
  );
}`,

  'bar-chart': `import { SimpleBarChart } from './components/Charts/SimpleCharts';

<SimpleBarChart
  data={[
    { label: 'Q1 Sales', values: [
      { x: 'Jan', y: 45 },
      { x: 'Feb', y: 52 },
      { x: 'Mar', y: 48 }
    ]},
    { label: 'Q2 Sales', values: [
      { x: 'Apr', y: 61 },
      { x: 'May', y: 55 },
      { x: 'Jun', y: 67 }
    ]}
  ]}
  height={400}
/>`,

  'pie-chart': `import { SimplePieChart } from './components/Charts/SimpleCharts';

<SimplePieChart
  data={[
    { label: 'Desktop', value: 45 },
    { label: 'Mobile', value: 30 },
    { label: 'Tablet', value: 25 }
  ]}
  height={400}
/>`,

  'line-chart': `import { SimpleLineChart } from './components/Charts/SimpleCharts';

<SimpleLineChart
  data={[
    { label: 'Revenue', values: [
      { x: 'Jan', y: 4000 },
      { x: 'Feb', y: 3000 },
      { x: 'Mar', y: 5000 }
    ]}
  ]}
  height={400}
/>`,

  'area-chart': `import { SimpleAreaChart } from './components/Charts/SimpleCharts';

<SimpleAreaChart
  data={[
    { label: 'Users', values: [
      { x: 'Mon', y: 100 },
      { x: 'Tue', y: 150 },
      { x: 'Wed', y: 200 }
    ]}
  ]}
  height={400}
/>`,

  'scatter-plot': `import { SimpleScatterPlot } from './components/Charts/SimpleCharts';

<SimpleScatterPlot
  data={[
    { x: 10, y: 20 },
    { x: 15, y: 30 },
    { x: 20, y: 25 }
  ]}
  height={400}
/>`,

  'moving-average': `import { MovingAverageChart } from './components/Charts/SimpleCharts';

<MovingAverageChart
  data={[10, 20, 15, 30, 25, 40, 35]}
  windowSize={3}
  height={400}
/>`,

  'audio-waveform': `import { AudioWaveform } from './components/Charts/SimpleCharts';

<AudioWaveform
  data={[0.1, 0.3, 0.5, 0.7, 0.9, 0.6, 0.4, 0.2]}
  height={200}
/>`,

  'simple-planet-menu': `import { SimplePlanetMenu } from './components/Charts/PlanetMenus';

<SimplePlanetMenu
  centerLabel="Menu"
  items={[
    { color: '#9257ad', icon: '📁', action: () => console.log('File') },
    { color: '#1da8a4', icon: '🔍', action: () => console.log('Search') },
    { color: '#ff6b6b', icon: '⚙️', action: () => console.log('Settings') }
  ]}
  orbitRadius={120}
/>`,

  'draggable-planet-menu': `import { DraggablePlanetMenu } from './components/Charts/PlanetMenus';

<DraggablePlanetMenu
  centerLabel="Drag Me"
  items={[
    { color: '#9257ad', icon: '📁', action: () => {} },
    { color: '#1da8a4', icon: '🔍', action: () => {} }
  ]}
  orbitRadius={120}
/>`,

  'custom-orbit-menu': `import { CustomOrbitMenu } from './components/Charts/PlanetMenus';

<CustomOrbitMenu
  centerLabel="Custom"
  items={[
    { color: '#9257ad', icon: '📁', action: () => {} },
    { color: '#1da8a4', icon: '🔍', action: () => {} }
  ]}
  orbitRadius={120}
/>`,

  'nested-planet-menu': `import { NestedPlanetMenu } from './components/Charts/PlanetMenus';

<NestedPlanetMenu
  centerLabel="Solar"
  items={[
    { color: '#ffd700', icon: '☀️', action: () => {} },
    { color: '#8884d8', icon: '🌍', action: () => {} },
    { color: '#82ca9d', icon: '🌙', action: () => {} }
  ]}
  orbitRadius={120}
/>`,

  'checklist': `const CHECKLIST_STEPS = [
  { title: 'Craft the UI System', description: 'Replace App.jsx...' },
  { title: 'Wire Backend APIs', description: 'Add new endpoints...' }
];

{CHECKLIST_STEPS.map((step, idx) => (
  <div key={idx} className="checklist-item">
    <h3>{step.title}</h3>
    <p>{step.description}</p>
  </div>
))}`,

  'telemetry': `import { LineChart, Line, XAxis, YAxis, ResponsiveContainer } from 'recharts';

const memoryData = memorySeries.map((value, index) => ({
  time: index,
  memory: value
}));

<ResponsiveContainer width="100%" height="100%">
  <LineChart data={memoryData}>
    <XAxis dataKey="time" />
    <YAxis />
    <Line type="monotone" dataKey="memory" stroke="#8884d8" />
  </LineChart>
</ResponsiveContainer>`,

  'socketio': `import io from 'socket.io-client';

const socket = io('http://localhost:3004');

socket.on('connect', () => {
  console.log('Connected:', socket.id);
});

socket.on('chatMessage', (data) => {
  setMessages(prev => [...prev, data]);
});

socket.emit('chatMessage', { room: 'general', message: 'Hello!' });`,

  'ping-api': `const [status, setStatus] = useState('idle');

const pingServer = async () => {
  setStatus('pinging');
  const start = Date.now();
  try {
  try {
    await apiClient.get('/health');
    const latency = Date.now() - start;
    setStatus(\`Success: \${latency}ms\`);
  } catch (err) {
    setStatus('Error');
  }
};`,

  'server-status': `const [serverStatus, setServerStatus] = useState('unknown');

useEffect(() => {
  const checkStatus = async () => {
    try {
      const res = await apiClient.get('/health');
      setServerStatus('online');
    } catch {
      setServerStatus('offline');
    }
  };
  checkStatus();
  const interval = setInterval(checkStatus, 5000);
  return () => clearInterval(interval);
}, []);`,

  'ux': `const [loading, setLoading] = useState(false);
const [toast, setToast] = useState(null);

const handleAction = async () => {
  setLoading(true);
  try {
    await performAction();
    setToast({ type: 'success', message: 'Action completed!' });
  } catch (err) {
    setToast({ type: 'error', message: err.message });
  } finally {
    setLoading(false);
  }
};`
};

