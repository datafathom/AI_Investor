/**
 * ViewSource Component
 * 
 * Displays the source code for a widget component with syntax highlighting.
 */

import React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import './ViewSource.css';

export default function ViewSource({ source, onClose }) {
  if (!source) return null;

  return (
    <div className="view-source-overlay" onClick={onClose}>
      <div className="view-source-container" onClick={(e) => e.stopPropagation()}>
        <div className="view-source-header">
          <h3>Source Code</h3>
          <button className="view-source-close" onClick={onClose} aria-label="Close">
            
          </button>
        </div>
        <div className="view-source-content">
          <SyntaxHighlighter
            language="javascript"
            style={vscDarkPlus}
            customStyle={{
              margin: 0,
              padding: '1rem',
              borderRadius: '0.5rem',
              fontSize: '0.875rem',
              lineHeight: '1.5',
            }}
          >
            {source}
          </SyntaxHighlighter>
        </div>
      </div>
    </div>
  );
}

