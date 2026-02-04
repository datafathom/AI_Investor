import React, { createContext, useContext, useState, useCallback } from 'react';
import { X, CheckCircle, AlertTriangle, AlertCircle, Info } from 'lucide-react';
import './EnhancedToast.css';

const ToastContext = createContext(null);

const TOAST_TYPES = {
  success: { icon: CheckCircle, className: 'toast--success' },
  warning: { icon: AlertTriangle, className: 'toast--warning' },
  error: { icon: AlertCircle, className: 'toast--error' },
  info: { icon: Info, className: 'toast--info' },
};

export const EnhancedToastProvider = ({ children }) => {
  const [toasts, setToasts] = useState([]);

  const addToast = useCallback(({ 
    type = 'info', 
    title, 
    message, 
    duration = 5000,
    action,
    actionLabel = 'Undo',
    persistent = false
  }) => {
    const id = Date.now() + Math.random();
    
    setToasts(prev => [...prev, { 
      id, type, title, message, duration, action, actionLabel, persistent,
      createdAt: Date.now()
    }]);

    if (!persistent && duration > 0) {
      setTimeout(() => {
        removeToast(id);
      }, duration);
    }

    return id;
  }, []);

  const removeToast = useCallback((id) => {
    setToasts(prev => prev.map(t => 
      t.id === id ? { ...t, exiting: true } : t
    ));
    
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id));
    }, 300);
  }, []);

  const toast = {
    success: (title, message, opts) => addToast({ type: 'success', title, message, ...opts }),
    warning: (title, message, opts) => addToast({ type: 'warning', title, message, ...opts }),
    error: (title, message, opts) => addToast({ type: 'error', title, message, ...opts }),
    info: (title, message, opts) => addToast({ type: 'info', title, message, ...opts }),
    dismiss: removeToast,
  };

  return (
    <ToastContext.Provider value={toast}>
      {children}
      <div className="toast-container" role="region" aria-label="Notifications">
        {toasts.map(t => (
          <Toast key={t.id} {...t} onDismiss={() => removeToast(t.id)} />
        ))}
      </div>
    </ToastContext.Provider>
  );
};

const Toast = ({ 
  id, type, title, message, duration, action, actionLabel, 
  persistent, exiting, createdAt, onDismiss 
}) => {
  const { icon: Icon, className } = TOAST_TYPES[type] || TOAST_TYPES.info;

  const handleAction = () => {
    if (action) action();
    onDismiss();
  };

  return (
    <div 
      className={`toast ${className} ${exiting ? 'toast--exiting' : ''}`}
      role="alert"
      aria-live="polite"
    >
      <div className="toast__icon">
        <Icon size={20} />
      </div>
      
      <div className="toast__content">
        {title && <div className="toast__title">{title}</div>}
        {message && <div className="toast__message">{message}</div>}
      </div>

      <div className="toast__actions">
        {action && (
          <button className="toast__action-btn" onClick={handleAction}>
            {actionLabel}
          </button>
        )}
        <button className="toast__close" onClick={onDismiss} aria-label="Dismiss">
          <X size={16} />
        </button>
      </div>

      {!persistent && duration > 0 && (
        <div 
          className="toast__progress" 
          style={{ animationDuration: `${duration}ms` }}
        />
      )}
    </div>
  );
};

export const useEnhancedToast = () => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useEnhancedToast must be used within EnhancedToastProvider');
  }
  return context;
};

export default EnhancedToastProvider;
