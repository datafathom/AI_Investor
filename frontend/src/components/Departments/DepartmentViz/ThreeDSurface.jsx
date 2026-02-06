import React, { useMemo, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Grid, Text } from '@react-three/drei';
import * as THREE from 'three';

const VolatilitySurface = ({ color }) => {
  const meshRef = useRef();

  // Generate Volatility Surface Geometry (Smile)
  const geometry = useMemo(() => {
    const size = 50;
    const geom = new THREE.PlaneGeometry(10, 10, size, size);
    
    const count = geom.attributes.position.count;
    for (let i = 0; i < count; i++) {
        const x = geom.attributes.position.getX(i);
        const z = geom.attributes.position.getY(i); // Plane is usually XY, we map to XZ later or rotate
        
        // Volatility Smile Function: higher at edges (deep OTM/ITM)
        const dist = Math.sqrt(x * x + z * z);
        const y = 0.5 * Math.pow(dist, 2) * 0.1 + Math.sin(x * 2) * 0.2;
        
        geom.attributes.position.setZ(i, y); // Deform Z (which will be Up after rotation)
    }
    geom.computeVertexNormals();
    return geom;
  }, []);

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.z += 0.002;
    }
  });

  return (
    <group rotation={[-Math.PI / 2.5, 0, 0]}> {/* Tilt to view surface */}
      <mesh ref={meshRef} geometry={geometry}>
        <meshStandardMaterial 
            color={color || "#a855f7"} 
            wireframe 
            side={THREE.DoubleSide}
            emissive={color || "#a855f7"}
            emissiveIntensity={0.5}
        />
      </mesh>
      
      {/* Base Grid */}
      <Grid position={[0, 0, -1]} args={[10, 10]} cellColor="#ffffff" sectionColor={color} fadeDistance={20} />
    </group>
  );
};

const ThreeDSurface = ({ color = "#a855f7" }) => {
  return (
    <div style={{ width: '100%', height: '100%', minHeight: '400px', background: 'linear-gradient(to bottom, #0f0c29, #302b63, #24243e)' }}>
      <Canvas camera={{ position: [0, 5, 10], fov: 60 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <VolatilitySurface color={color} />
        <OrbitControls enableZoom={true} autoRotate autoRotateSpeed={0.5} />
      </Canvas>
      <div style={{ position: 'absolute', bottom: 20, left: 20, color: 'white', pointerEvents: 'none' }}>
        <h4 style={{ margin: 0 }}>VOLATILITY SURFACE</h4>
        <p style={{ margin: 0, fontSize: '0.8em', opacity: 0.7 }}>Real-time Greeks Rendering</p>
      </div>
    </div>
  );
};

export default ThreeDSurface;
