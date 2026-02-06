import React, { useMemo, useState, useEffect } from 'react';
import ForceGraph3D from 'react-force-graph-3d';
import { useTheme } from '@mui/material/styles';
import { Card, CardContent, Typography, Box } from '@mui/material';

// Dummy data generator for prototype
const genRandomTree = (N = 300, reverse = false) => {
  return {
    nodes: [...Array(N).keys()].map(i => ({ 
      id: i,
      group: Math.floor(Math.random() * 5),
      val: Math.random() * 10
    })),
    links: [...Array(N).keys()]
      .filter(id => id)
      .map(id => ({
        source: id,
        target: Math.round(Math.random() * (id - 1))
      }))
  };
};

const MemoryMap = ({ data }) => {
  const theme = useTheme();
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [highlightNode, setHighlightNode] = useState(null);

  useEffect(() => {
    // In prod, this would transform props.data from the API
    // For now, use dummy data if no data provided
    if (!data) {
      setGraphData(genRandomTree(50));
    } else {
        setGraphData(data);
    }
  }, [data]);

  const nodeColor = (node) => {
    if (highlightNode && node.id === highlightNode.id) return '#ff0000';
    const colors = ['#268bd2', '#859900', '#dc322f', '#d33682', '#b58900'];
    return colors[node.group % colors.length];
  };

  return (
    <Box sx={{ height: '100%', position: 'relative', bgcolor: '#002b36' }}>
      <ForceGraph3D
        graphData={graphData}
        nodeLabel="id"
        nodeColor={nodeColor}
        nodeRelSize={4}
        linkColor={() => 'rgba(147, 161, 161, 0.2)'}
        linkOpacity={0.3}
        backgroundColor="#002b36"
        onNodeClick={node => {
            setHighlightNode(node);
            console.log("Clicked node:", node);
        }}
        width={800} // This should be responsive in real usage
        height={600}
      />
      
      {highlightNode && (
          <Card sx={{ position: 'absolute', top: 20, right: 20, maxWidth: 300, bgcolor: 'rgba(255,255,255,0.9)' }}>
              <CardContent>
                  <Typography variant="h6">Memory Node #{highlightNode.id}</Typography>
                  <Typography variant="body2">Group: {highlightNode.group}</Typography>
                  <Typography variant="body2">Value: {highlightNode.val.toFixed(2)}</Typography>
              </CardContent>
          </Card>
      )}
    </Box>
  );
};

export default MemoryMap;
