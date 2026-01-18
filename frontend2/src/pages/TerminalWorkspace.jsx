
import React from 'react';
import Dashboard from './Dashboard';
import './TerminalWorkspace.css';
import CommandPalette from '../components/Terminal/CommandPalette';
import NotificationDrawer from '../components/Terminal/NotificationDrawer';
import WorkspaceMinimap from '../components/Terminal/WorkspaceMinimap';
import { Bell } from 'lucide-react';

/**
 * Terminal Workspace
 * Institutional-grade command center with multi-window support.
 */
const TerminalWorkspace = (props) => {
    const [showCommandPalette, setShowCommandPalette] = React.useState(false);
    const [showDrawer, setShowDrawer] = React.useState(false);
    const [showMinimap, setShowMinimap] = React.useState(false);

    React.useEffect(() => {
        const handleKeyDown = (e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                e.preventDefault();
                setShowCommandPalette(prev => !prev);
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, []);

    const handleCommand = (cmd) => {
        console.log('Command executed:', cmd);
        props.setToast({ message: `Executing: ${cmd.label}`, type: 'info' });
        // Implement actual command logic here if needed or delegate to props
        if (cmd.id === 'toggle-theme') {
            // Basic toggle theme mock or call prop if available
        }
    };

    return (
        <div className="terminal-workspace relative min-h-screen">
            <Dashboard {...props} />

            {/* Premium Overlays */}
            <CommandPalette
                isOpen={showCommandPalette}
                onClose={() => setShowCommandPalette(false)}
                onCommand={handleCommand}
            />

            <NotificationDrawer
                isOpen={showDrawer}
                onClose={() => setShowDrawer(false)}
            />

            <WorkspaceMinimap
                isOpen={showMinimap}
                toggle={() => setShowMinimap(!showMinimap)}
                widgetVisibility={props.widgetVisibility}
            />

            {/* Quick Actions Floating Bar (Optional, can be used to trigger Drawer) */}
            <div className="fixed bottom-4 left-4 z-[40] flex gap-2">
                <button
                    onClick={() => setShowDrawer(true)}
                    className="bg-slate-900/80 border border-slate-700 p-2 rounded-lg text-slate-400 hover:text-white hover:border-amber-500 transition-all shadow-lg"
                    title="System Notifications"
                >
                    <div className="relative">
                        <Bell size={20} />
                        <span className="absolute -top-1 -right-1 w-2 h-2 bg-amber-500 rounded-full animate-pulse"></span>
                    </div>
                </button>
            </div>

            {/* Hint for Command Palette */}
            <div className="fixed bottom-4 left-1/2 -translate-x-1/2 z-[40] pointer-events-none opacity-50 text-[10px] uppercase font-mono bg-black/50 px-2 py-1 rounded text-slate-500 border border-slate-800">
                Press <span className="text-slate-300">Cmd+K</span> for Commands
            </div>
        </div>
    );
};

export default TerminalWorkspace;
