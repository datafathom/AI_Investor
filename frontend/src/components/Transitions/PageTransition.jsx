import React from 'react';
import { useLocation } from 'react-router-dom';
import './PageTransition.css';

/**
 * Wraps page content with entrance/exit animations.
 * Uses location key to trigger re-animation on route change.
 */
const PageTransition = ({ children, variant = 'fade' }) => {
  const location = useLocation();
  
  return (
    <div 
      key={location.pathname} 
      className={`page-transition page-transition--${variant}`}
    >
      {children}
    </div>
  );
};

export default PageTransition;
