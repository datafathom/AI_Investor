import React, { useMemo } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars } from '@react-three/drei';

const FitnessSurface3D = ({ data }) => {
  return (
    <div style={{ width: '100%', height: '400px', background: '#111', borderRadius: '12px' }}>
      <Canvas camera={{ position: [0, 5, 10] }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />
        <Stars />
        <mesh rotation={[-Math.PI / 2, 0, 0]}>
          <planeGeometry args={[10, 10, 32, 32]} />
          <meshStandardMaterial wireframe color="#00ff88" />
        </mesh>
        <OrbitControls />
        <gridHelper args={[20, 20, 0xff0000, 0x444444]} />
      </Canvas>
    </div>
  );
};

export default FitnessSurface3D;
