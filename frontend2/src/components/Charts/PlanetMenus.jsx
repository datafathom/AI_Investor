import React, { useState } from 'react';
import { Planet } from 'react-planet';

// --- Shared Satellite Component (The items orbiting the planet) ---
const Satellite = React.memo(({ color = '#9257ad', icon, onClick }) => (
    <div
        onClick={onClick}
        style={{
            height: 50,
            width: 50,
            borderRadius: '50%',
            backgroundColor: color,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            cursor: 'pointer',
            boxShadow: '0 2px 5px rgba(0,0,0,0.2)'
        }}
    >
        {icon || 'S'}
    </div>
));
Satellite.displayName = 'Satellite';

// --- Shared Center Component (The main planet) ---
const PlanetCenter = React.memo(({ color = '#1da8a4', label, onClick }) => (
    <div
        onClick={onClick}
        style={{
            height: 80,
            width: 80,
            borderRadius: '50%',
            backgroundColor: color,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            cursor: 'pointer',
            boxShadow: '0 4px 10px rgba(0,0,0,0.3)'
        }}
    >
        {label || 'Center'}
    </div>
));
PlanetCenter.displayName = 'PlanetCenter';

// --- 1. Simple Circular Menu ---
// Basic usage with auto-close functionality
export const SimplePlanetMenu = React.memo(({ 
    centerLabel, 
    items, 
    orbitRadius = 120, 
    open: initialOpen = false 
}) => {
    const [open, setOpen] = useState(initialOpen);
    
    const handleCenterClick = React.useCallback(() => {
        setOpen(prev => !prev);
    }, []);
    
    return (
        <div className="planet-container" style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 0, margin: 0 }}>
            <Planet
                centerContent={<PlanetCenter label={centerLabel} onClick={handleCenterClick} />}
                open={open}
                orbitRadius={orbitRadius}
                autoClose
                rotation={30} // Offset starting angle
            >
                {items.map((item, index) => (
                    <Satellite 
                        key={index} 
                        color={item.color} 
                        icon={item.icon} 
                        onClick={item.action} 
                    />
                ))}
            </Planet>
        </div>
    );
});
SimplePlanetMenu.displayName = 'SimplePlanetMenu';

// --- 2. Draggable Planet Menu ---
// Enables dragging for both the center planet and its satellites
export const DraggablePlanetMenu = React.memo(({ centerLabel, items }) => {
    return (
        <div className="planet-container" style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 0, margin: 0 }}>
            <Planet
                centerContent={<PlanetCenter label={centerLabel} color="#e67e22" />}
                open
                orbitRadius={140}
                dragablePlanet
                dragRadiusPlanet={20}
                dragableSatellites
                dragRadiusSatellites={20}
                bounce
            >
                {items.map((item, index) => (
                    <Satellite 
                        key={index} 
                        color="#d35400"
                        icon={item.icon} 
                    />
                ))}
            </Planet>
        </div>
    );
});
DraggablePlanetMenu.displayName = 'DraggablePlanetMenu';

// --- 3. Custom Orbit Style Menu ---
// Uses the orbitStyle prop to customize the ring appearance
export const CustomOrbitMenu = React.memo(({ centerLabel, items }) => {
    
    const customOrbitStyle = React.useCallback((defaultStyle) => ({
        ...defaultStyle,
        borderWidth: 4,
        borderStyle: 'dashed',
        borderColor: '#6f03fc',
        opacity: 0.7
    }), []);

    return (
        <div className="planet-container" style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 0, margin: 0 }}>
            <Planet
                centerContent={<PlanetCenter label={centerLabel} color="#8e44ad" />}
                open
                orbitRadius={130}
                orbitStyle={customOrbitStyle}
            >
                {items.map((item, index) => (
                    <Satellite 
                        key={index} 
                        color="#9b59b6" 
                        icon={index + 1} 
                    />
                ))}
            </Planet>
        </div>
    );
});
CustomOrbitMenu.displayName = 'CustomOrbitMenu';

// --- 4. Nested "Planetception" Menu ---
// Demonstrates a planet acting as a satellite for another planet
export const NestedPlanetMenu = React.memo(() => {
    return (
        <div className="planet-container" style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 0, margin: 0 }}>
            {/* Main Sun */}
            <Planet
                centerContent={<PlanetCenter label="Sun" color="#f1c40f" />}
                open
                orbitRadius={160}
                autoClose
            >
                <Satellite icon="Mer" color="#bdc3c7" />
                <Satellite icon="Ven" color="#e67e22" />
                
                {/* Earth as a Planet with its own Moon */}
                <Planet
                    centerContent={<Satellite icon="Earth" color="#2980b9" />}
                    open
                    orbitRadius={60}
                    hideOrbit // Hide Earth's orbit ring for cleaner look
                    autoClose
                >
                    <Satellite icon="Moon" color="#ecf0f1" />
                </Planet>
                
                <Satellite icon="Mars" color="#c0392b" />
            </Planet>
        </div>
    );
});
NestedPlanetMenu.displayName = 'NestedPlanetMenu';