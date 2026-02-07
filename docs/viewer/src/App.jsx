import React, { useState, useEffect, useMemo, useRef, useCallback } from 'react';
import { 
  BrowserRouter as Router, 
  Routes, 
  Route, 
  useNavigate, 
  useLocation 
} from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { 
  Folder, 
  FileText, 
  ChevronRight, 
  ChevronDown, 
  Cpu, 
  BookOpen,
  ArrowLeft
} from 'lucide-react';

const API_BASE = "http://127.0.0.1:5055/api";

// Utility to resolve relative paths
const resolveRelativePath = (currentPath, relativePath) => {
  // If it's a root-relative link (starts with /), treat it as relative to the docs root
  if (relativePath.startsWith('/')) {
    let path = relativePath.substring(1);
    // Ensure it has an extension for the API
    if (!path.endsWith('.md') && !path.endsWith('.txt')) {
      // We'll let the server handle the extension search, but we can append .md as default
      // Or just leave it as is if the server can handle it.
      // For now, let's just return it and fix the server to be smart.
    }
    return path;
  }

  if (!currentPath) return relativePath;
  
  const parts = currentPath.split('/');
  parts.pop(); // Remove current filename
  
  const relParts = relativePath.split('/');
  for (const part of relParts) {
    if (part === '.') continue;
    if (part === '..') {
      parts.pop();
    } else {
      parts.push(part);
    }
  }
  return parts.join('/');
};

const TreeItem = ({ item, level = 0, onSelect, currentPath }) => {
  const [isOpen, setIsOpen] = useState(false);
  const isActive = currentPath === item.path;

  // Auto-open parent folders if active file is inside
  useEffect(() => {
    if (currentPath && currentPath.startsWith(item.path + '/')) {
      setIsOpen(true);
    }
  }, [currentPath]);

  const toggle = (e) => {
    e.stopPropagation();
    if (item.type === 'directory') {
      setIsOpen(!isOpen);
    } else {
      onSelect(item.path);
    }
  };

  return (
    <div className="tree-item">
      <div 
        className={`tree-node ${isActive ? 'active' : ''}`}
        style={{ paddingLeft: `${level * 10 + 10}px` }} // Denser indentation
        onClick={toggle}
      >
        {item.type === 'directory' ? (
          <>
            {isOpen ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
            <Folder size={14} className="text-accent-blue" />
          </>
        ) : (
          <FileText size={14} className="text-text-secondary" />
        )}
        <span>{item.name.replace(/\.(md|txt)$/, '')}</span>
      </div>
      
      {item.type === 'directory' && isOpen && (
        <div className="tree-children">
          {item.children.map((child, idx) => (
            <TreeItem 
              key={idx} 
              item={child} 
              level={level + 1} 
              onSelect={onSelect} 
              currentPath={currentPath}
            />
          ))}
        </div>
      )}
    </div>
  );
};

function DocsApp() {
  const [tree, setTree] = useState([]);
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [sidebarWidth, setSidebarWidth] = useState(260);
  const [isResizing, setIsResizing] = useState(false);
  
  const navigate = useNavigate();
  const location = useLocation();
  const sidebarRef = useRef(null);

  // Resize logic
  const startResizing = useCallback((e) => {
    e.preventDefault();
    setIsResizing(true);
  }, []);

  const stopResizing = useCallback(() => {
    setIsResizing(false);
  }, []);

  const resize = useCallback((e) => {
    if (isResizing) {
      const newWidth = e.clientX;
      if (newWidth >= 200 && newWidth <= 600) {
        setSidebarWidth(newWidth);
      }
    }
  }, [isResizing]);

  useEffect(() => {
    if (isResizing) {
      window.addEventListener('mousemove', resize);
      window.addEventListener('mouseup', stopResizing);
    } else {
      window.removeEventListener('mousemove', resize);
      window.removeEventListener('mouseup', stopResizing);
    }
    return () => {
      window.removeEventListener('mousemove', resize);
      window.removeEventListener('mouseup', stopResizing);
    };
  }, [isResizing, resize, stopResizing]);

  const currentFile = useMemo(() => {
    const path = location.pathname.substring(1);
    return path ? decodeURIComponent(path) : null;
  }, [location.pathname]);

  useEffect(() => {
    fetch(`${API_BASE}/tree`)
      .then(res => res.json())
      .then(data => setTree(data))
      .catch(err => console.error("Failed to fetch tree:", err));
  }, []);

  useEffect(() => {
    if (currentFile) {
      setLoading(true);
      fetch(`${API_BASE}/content/${currentFile}`)
        .then(res => {
          if (!res.ok) throw new Error("File not found");
          return res.json();
        })
        .then(data => setContent(data.content))
        .catch(err => {
          console.error("Failed to fetch content:", err);
          setContent(`# Error\nCould not load documentation at \`${currentFile}\`.`);
        })
        .finally(() => setLoading(false));
    } else {
      setContent('');
    }
  }, [currentFile]);

  const handleSelect = (path) => {
    navigate(`/${path}`);
  };

  // Custom components for ReactMarkdown to handle links
  const MarkdownComponents = {
    a: ({ node, ...props }) => {
      const href = props.href || '';
      const isInternal = href && !href.startsWith('http') && !href.startsWith('//') && !href.startsWith('mailto:');
      
      if (isInternal) {
        return (
          <a
            {...props}
            onClick={(e) => {
              e.preventDefault();
              const newPath = resolveRelativePath(currentFile, href);
              handleSelect(newPath);
            }}
            className="cursor-pointer text-accent-cyan hover:underline"
          />
        );
      }
      return <a {...props} target="_blank" rel="noopener noreferrer" className="text-accent-blue hover:underline" />;
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside 
        className="sidebar" 
        style={{ width: `${sidebarWidth}px` }}
        ref={sidebarRef}
      >
        <div className="sidebar-header" onClick={() => navigate('/')} style={{ cursor: 'pointer' }}>
          <Cpu className="text-accent-cyan" size={18} />
          <h1>Docs Portal</h1>
        </div>
        
        <div className="tree-container">
          {tree.map((item, idx) => (
            <TreeItem 
              key={idx} 
              item={item} 
              onSelect={handleSelect} 
              currentPath={currentFile}
            />
          ))}
        </div>

        <div 
          className={`sidebar-resize-handle ${isResizing ? 'resizing' : ''}`}
          onMouseDown={startResizing}
        />
      </aside>

      {/* Main Content */}
      <main className="content-main">
        {currentFile ? (
          <div className={`content-glass ${loading ? 'opacity-50' : ''}`}>
            <button 
              onClick={() => navigate(-1)} 
              className="mb-6 flex items-center gap-2 text-text-secondary hover:text-accent-cyan transition-colors"
              style={{ background: 'transparent', border: 'none', cursor: 'pointer', font: 'inherit', color: 'inherit' }}
            >
              <ArrowLeft size={14} /> Back
            </button>
            <div className="markdown-body">
              <ReactMarkdown 
                remarkPlugins={[remarkGfm]}
                components={MarkdownComponents}
              >
                {content}
              </ReactMarkdown>
            </div>
          </div>
        ) : (
          <div className="placeholder">
            <BookOpen size={48} />
            <h2>Sovereign OS Documentation</h2>
            <p>Select a file from the sidebar to begin.</p>
            <div className="mt-6 flex gap-3">
              <button 
                onClick={() => handleSelect('frontend/routes/All_Pages_Summary.md')}
                className="px-5 py-2 border border-accent-cyan text-accent-cyan hover:bg-accent-cyan hover:text-bg-color transition-all rounded text-sm"
                style={{ cursor: 'pointer' }}
              >
                View System Map
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <DocsApp />
    </Router>
  );
}
