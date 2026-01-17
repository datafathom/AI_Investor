
import React from 'react';
import Dashboard from './Dashboard';
import './TerminalWorkspace.css';

/**
 * Terminal Workspace
 * Institutional-grade command center with multi-window support.
 */
const TerminalWorkspace = (props) => {
    return (
        <div className="terminal-workspace">
            <Dashboard {...props} />
        </div>
    );
};

export default TerminalWorkspace;
