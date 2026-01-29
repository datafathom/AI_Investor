import React, { useMemo } from 'react';
import { useShallow } from 'zustand/react/shallow';
import useWindowStore from '../../stores/windowStore';
import useTaskbarStore from '../../stores/taskbarStore';
import TaskbarIcon from './TaskbarIcon';
import StartMenu from './StartMenu';
import KillSwitch from './KillSwitch';
import AgentMoodIcons from './AgentMoodIcons';
import TaskbarClock from './TaskbarClock';
import SystemHealthMeters from './SystemHealthMeters';
import FPSCounter from '../Common/FPSCounter';
import './Taskbar.css';

const Taskbar = () => {
    // Optimized: Only re-render if the set of window IDs changes
    const windowIds = useWindowStore(useShallow((state) => state.windows.map(w => w.id)));
    
    // Optimized: Select only what is needed from taskbar store
    const isStartMenuOpen = useTaskbarStore((state) => state.isStartMenuOpen);
    const activeWorkspace = useTaskbarStore((state) => state.activeWorkspace);
    const setWorkspace = useTaskbarStore((state) => state.setWorkspace);
    const closeStartMenu = useTaskbarStore((state) => state.closeStartMenu);
    const toggleStartMenu = useTaskbarStore((state) => state.toggleStartMenu);
    
    const handleStartClick = (e) => {
        e.stopPropagation();
        toggleStartMenu();
    };

    return (
        <div className="taskbar-container" onClick={() => isStartMenuOpen && closeStartMenu()}>
            <StartMenu />

            <div className="taskbar-left-section">
                <div 
                    className={`taskbar-start-button ${isStartMenuOpen ? 'active' : ''}`}
                    onClick={handleStartClick}
                >
                    <div className="start-icon">🐺</div> 
                </div>

                <div className="workspace-switcher">
                    {['Research', 'Strategy', 'Admin'].map(ws => (
                        <div 
                            key={ws} 
                            className={`ws-dot ${activeWorkspace === ws ? 'active' : ''}`}
                            onClick={(e) => { e.stopPropagation(); setWorkspace(ws); }}
                            title={`Workspace: ${ws}`}
                        />
                    ))}
                </div>
            </div>
            
            <div className="taskbar-apps">
                {windowIds.map((id) => (
                    <MemoizedTaskbarIconWrapper key={id} id={id} />
                ))}
            </div>
            
            <div className="taskbar-right-section">
                <FPSCounter />
                <AgentMoodIcons />
                <SystemHealthMeters />
                <KillSwitch />
                <TaskbarClock />
            </div>
        </div>
    );
};

// Internal wrapper to fetch window state by ID, preventing the entire Taskbar from re-rendering
const MemoizedTaskbarIconWrapper = React.memo(({ id }) => {
    // Select ONLY what is needed for the icon to avoid re-rendering on other window changes
    const windowState = useWindowStore(useShallow((state) => {
        const w = state.windows.find(win => win.id === id);
        return w ? { id: w.id, title: w.title, risk: w.risk, isMinimized: w.isMinimized, snapshot: w.snapshot, badgeCount: w.badgeCount } : null;
    }));
    
    const activeWindowId = useWindowStore((state) => state.activeWindowId);
    
    if (!windowState) return null;
    
    // Check active state here to keep TaskbarIcon simpler
    const isActive = activeWindowId === id && !windowState.isMinimized;
    
    return <TaskbarIcon window={windowState} isActive={isActive} />;
});

export default React.memo(Taskbar);
