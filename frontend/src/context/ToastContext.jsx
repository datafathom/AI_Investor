import React, { createContext, useContext, useState, useCallback } from 'react';
import { Info, CheckCircle, AlertTriangle, XCircle, AlertOctagon, X } from 'lucide-react';
import './Toast.css';

const ToastContext = createContext();

export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
};

export const ToastProvider = ({ children }) => {
  const [toasts, setToasts] = useState([]);

  const showToast = useCallback((message, type = 'info', duration = null) => {
    const id = Math.random().toString(36).substr(2, 9);
    
    // Severity-based durations
    // INFO: 5s, WARN: 10s, CRITICAL: manual only
    let finalDuration = duration;
    if (finalDuration === null) {
      if (type === 'critical' || type === 'error') finalDuration = 0; // Manual only
      else if (type === 'warning') finalDuration = 10000;
      else finalDuration = 5000; // info/success
    }

    const newToast = { id, message, type, duration: finalDuration };
    
    setToasts(prev => {
      const updated = [...prev, newToast];
      // Stack up to 5 notifications
      if (updated.length > 5) return updated.slice(1);
      return updated;
    });
    
    if (finalDuration > 0) {
      setTimeout(() => {
        setToasts(prev => prev.filter(t => t.id !== id));
      }, finalDuration);
    }
  }, []);

  const removeToast = useCallback((id) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  }, []);

  const getIcon = (type) => {
    switch (type) {
      case 'success': return <CheckCircle size={18} className="text-green-400" />;
      case 'warning': return <AlertTriangle size={18} className="text-yellow-400" />;
      case 'error': return <XCircle size={18} className="text-red-400" />;
      case 'critical': return <AlertOctagon size={18} className="text-red-500 animate-pulse" />;
      case 'info':
      default: return <Info size={18} className="text-blue-400" />;
    }
  };

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      <div className="toast-container">
        {toasts.map(toast => (
          <div key={toast.id} className={`toast ${toast.type}`} onClick={() => removeToast(toast.id)}>
            <div className="toast-icon">
              {getIcon(toast.type)}
            </div>
            <div className="toast-message">{toast.message}</div>
            <button className="toast-close" onClick={(e) => {
              e.stopPropagation();
              removeToast(toast.id);
            }}>
              <X size={16} />
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
};
