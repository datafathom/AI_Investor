import React, { useRef, useEffect, useMemo } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

const SpatialAssetBubble = ({ data }) => {
    const mountRef = useRef(null);

    const assetNodes = useMemo(() => {
        if (!data || !data.nodes) return [];
        return data.nodes.filter(n => n.group === 'asset' || n.group === 'portfolio');
    }, [data]);

    useEffect(() => {
        if (!mountRef.current) return;

        const width = mountRef.current.clientWidth;
        const height = mountRef.current.clientHeight;

        // Scene setup
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x020617); // Slate-950

        // Camera
        const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
        camera.position.z = 150;

        // Renderer
        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(width, height);
        renderer.setPixelRatio(window.devicePixelRatio);
        mountRef.current.appendChild(renderer.domElement);

        // Controls
        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;

        // Assets
        const spheres = [];
        assetNodes.forEach((node, i) => {
            const geometry = new THREE.SphereGeometry(Math.sqrt(node.val || 1) * 2, 32, 32);
            const material = new THREE.MeshPhongMaterial({
                color: node.group === 'portfolio' ? 0x10b981 : 0xf59e0b, // Emerald or Amber
                transparent: true,
                opacity: 0.8,
                shininess: 100,
            });
            const sphere = new THREE.Mesh(geometry, material);
            
            // Random distribution for now (will use spatial_service projection later)
            sphere.position.x = (Math.random() - 0.5) * 200;
            sphere.position.y = (Math.random() - 0.5) * 200;
            sphere.position.z = (Math.random() - 0.5) * 200;
            
            scene.add(sphere);
            spheres.push(sphere);
        });

        // Lights
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        scene.add(ambientLight);

        const pointLight = new THREE.PointLight(0x38bdf8, 1, 500); // Cyan glow
        pointLight.position.set(50, 50, 50);
        scene.add(pointLight);

        // Animation loop
        const animate = () => {
            requestAnimationFrame(animate);
            controls.update();
            
            spheres.forEach(s => {
                s.rotation.y += 0.01;
            });
            
            renderer.render(scene, camera);
        };
        animate();

        // Cleanup
        return () => {
            if (mountRef.current) {
                mountRef.current.removeChild(renderer.domElement);
            }
            geometry.dispose();
            material.dispose();
        };
    }, [assetNodes]);

    return (
        <div className="w-full h-full relative overflow-hidden bg-slate-950">
            <div className="absolute top-4 left-4 z-10">
                <p className="text-[10px] text-cyan-400 font-mono uppercase tracking-widest">3D Spatial Asset Grid</p>
                <p className="text-zinc-500 text-[9px] uppercase">Alpha Release v0.3</p>
            </div>
            <div ref={mountRef} className="w-full h-full" />
        </div>
    );
};

export default SpatialAssetBubble;
