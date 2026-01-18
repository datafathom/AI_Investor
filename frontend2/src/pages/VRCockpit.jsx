import React from 'react';
import HUDOverlay from '../components/VR/HUDOverlay';
import InfiniteGrid from '../components/VR/InfiniteGrid';
import GestureControls from '../components/VR/GestureControls';

const VRCockpit = () => {
    return (
        <div className="relative w-full h-screen bg-black overflow-hidden font-sans">
            <InfiniteGrid />
            <HUDOverlay />
            <GestureControls />

            {/* Vignette & Scanlines */}
            <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(circle,transparent_50%,black_150%)] z-10"></div>
            <div className="absolute inset-0 pointer-events-none bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,255,0.06))] bg-[size:100%_2px,3px_100%] z-10 opacity-20"></div>
        </div>
    );
};

export default VRCockpit;
