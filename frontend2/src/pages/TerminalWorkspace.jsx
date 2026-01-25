import React from 'react';
import Dashboard from './Dashboard';
import './TerminalWorkspace.css';
import CommandPalette from '../components/Terminal/CommandPalette';
import { useToast } from '../context/ToastContext';

/**
 * Terminal Workspace
 * Institutional-grade command center with multi-window support.
 */
const TerminalWorkspace = (props) => {
    const { showToast } = useToast();
    const [showCommandPalette, setShowCommandPalette] = React.useState(false);

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
        showToast(`Executing: ${cmd.label}`, 'info');
        if (cmd.id === 'toggle-theme') {
            // Context will handle this
        }
    };

    return (
        <div className="terminal-workspace page-shell-os">
            <Dashboard {...props} />

            {/* Command Palette Overlay (Ctrl+K) */}
            <CommandPalette
                isOpen={showCommandPalette}
                onClose={() => setShowCommandPalette(false)}
                onCommand={handleCommand}
            />
        </div>
    );
};

export default TerminalWorkspace;
