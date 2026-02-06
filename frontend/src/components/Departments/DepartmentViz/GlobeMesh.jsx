import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Sphere, Stars } from '@react-three/drei';
import * as THREE from 'three';

const Globe = ({ color }) => {
  const meshRef = useRef();
  
  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += delta * 0.2;
    }
  });

  // Generate random markers on sphere surface
  const markers = React.useMemo(() => {
    return new Array(20).fill(0).map(() => {
      const phi = Math.acos(-1 + (2 * Math.random()));
      const theta = Math.sqrt(20 * Math.PI) * phi;
      return {
        position: [
          2.5 * Math.sin(phi) * Math.cos(theta),
          2.5 * Math.sin(phi) * Math.sin(theta),
          2.5 * Math.cos(phi)
        ]
      };
    });
  }, []);

  return (
    <group ref={meshRef}>
      {/* Core Globe */}
      <Sphere args={[2.5, 32, 32]}>
        <meshStandardMaterial 
          color={color || "#ef4444"} 
          wireframe={true} 
          transparent 
          opacity={0.3} 
        />
      </Sphere>
      
      {/* Inner Glow */}
      <Sphere args={[2.4, 32, 32]}>
        <meshBasicMaterial color={color || "#ef4444"} transparent opacity={0.1} />
      </Sphere>

      {/* Security Node Markers */}
      {markers.map((marker, idx) => (
        <mesh position={marker.position} key={idx}>
          <boxGeometry args={[0.05, 0.05, 0.2]} />
          <meshStandardMaterial color="#ffffff" emissive="#ffffff" emissiveIntensity={2} />
        </mesh>
      ))}
    </group>
  );
};

const GlobeMesh = ({ color = "#ef4444" }) => {
  return (
    <div style={{ width: '100%', height: '100%', minHeight: '400px', background: 'linear-gradient(to bottom, #000, #111)' }}>
      <Canvas camera={{ position: [0, 0, 7] }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
        <Globe color={color} />
        <OrbitControls enableZoom={false} autoRotate autoRotateSpeed={0.5} />
      </Canvas>
      <div style={{ position: 'absolute', bottom: 20, left: 20, color: 'white', pointerEvents: 'none' }}>
        <h4 style={{ margin: 0 }}>GLOBAL THREAT MAP</h4>
        <p style={{ margin: 0, fontSize: '0.8em', opacity: 0.7 }}>Real-time Node Monitoring</p>
      </div>
    </div>
  );
};

export default GlobeMesh;
