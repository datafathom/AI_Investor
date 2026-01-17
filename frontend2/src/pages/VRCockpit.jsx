/**
 * VRCockpit.jsx
 * 
 * Immersive 3D/VR Dashboard using Three.js and @react-three/fiber.
 */

import React, { useState, useEffect, Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars, Text, Float, MeshDistortMaterial, PerspectiveCamera } from '@react-three/drei';
import { XR, VRButton } from '@react-three/xr';
import xrService from '../services/xrService';
import './VRCockpit.css';

const DataNode = ({ position, label, color, val }) => {
    const [hovered, setHover] = useState(false);

    return (
        <Float speed={2} rotationIntensity={0.5} floatIntensity={0.5}>
            <mesh
                position={position}
                onPointerOver={() => setHover(true)}
                onPointerOut={() => setHover(false)}
            >
                <sphereGeometry args={[val / 50, 32, 32]} />
                <MeshDistortMaterial
                    color={hovered ? "#fff" : color}
                    speed={2}
                    distort={0.3}
                    radius={1}
                />
                <Text
                    position={[0, 1.2, 0]}
                    fontSize={0.2}
                    color="white"
                    anchorX="center"
                    anchorY="middle"
                >
                    {label}
                </Text>
            </mesh>
        </Float>
    );
};

const VRCockpit = () => {
    const [spatialData, setSpatialData] = useState({ nodes: [], links: [] });
    const [isXRSupported, setIsXRSupported] = useState(false);

    useEffect(() => {
        const init = async () => {
            const data = await xrService.getSpatialData();
            setSpatialData(data);
            const supported = await xrService.isSupported();
            setIsXRSupported(supported);
        };
        init();
    }, []);

    return (
        <div className="vr-container">
            <header className="vr-ui-overlay glass">
                <div className="vr-header-info">
                    <h1>Minority Report Cockpit</h1>
                    <p>Spatial Trading Interface Active</p>
                </div>
                {isXRSupported ? (
                    <VRButton className="vr-action-btn" />
                ) : (
                    <div className="vr-badge">DESKTOP EMULATION MODE</div>
                )}
            </header>

            <div className="canvas-wrapper">
                <Canvas>
                    <XR>
                        <Suspense fallback={null}>
                            <PerspectiveCamera makeDefault position={[0, 0, 10]} />
                            <color attach="background" args={['#020617']} />
                            <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
                            <ambientLight intensity={0.5} />
                            <pointLight position={[10, 10, 10]} />

                            {/* XRControllers and XRHands removed for build compatibility - handled by XR provider */}

                            {spatialData.nodes.map((node) => (
                                <DataNode
                                    key={node.id}
                                    position={[node.x / 10, node.y / 10, node.z / 10]}
                                    label={node.label}
                                    color={node.color}
                                    val={node.val}
                                />
                            ))}

                            <OrbitControls enablePan={true} enableZoom={true} />
                        </Suspense>
                    </XR>
                </Canvas>
            </div>
        </div>
    );
};

export default VRCockpit;
