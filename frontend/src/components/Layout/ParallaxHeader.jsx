import React, { useState, useEffect, useRef } from 'react';
import './ParallaxHeader.css';

/**
 * Parallax header with scroll-based effects.
 * 
 * @param {React.ReactNode} children - Header content
 * @param {string} backgroundImage - Optional background image URL
 * @param {number} intensity - Parallax intensity (0-1)
 * @param {number} height - Header height in px
 */
const ParallaxHeader = ({ 
  children, 
  backgroundImage,
  intensity = 0.3,
  height = 300,
  className = ''
}) => {
  const [scrollY, setScrollY] = useState(0);
  const [opacity, setOpacity] = useState(1);
  const headerRef = useRef(null);

  useEffect(() => {
    const handleScroll = () => {
      if (!headerRef.current) return;
      
      const rect = headerRef.current.getBoundingClientRect();
      const scrolled = -rect.top;
      const headerHeight = rect.height;
      
      // Only apply effects when header is in view
      if (scrolled >= 0 && scrolled <= headerHeight) {
        setScrollY(scrolled * intensity);
        setOpacity(1 - (scrolled / headerHeight) * 0.6);
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, [intensity]);

  return (
    <div 
      ref={headerRef}
      className={`parallax-header ${className}`}
      style={{ height }}
    >
      {backgroundImage && (
        <div 
          className="parallax-header__bg"
          style={{
            backgroundImage: `url(${backgroundImage})`,
            transform: `translateY(${scrollY}px) scale(1.1)`,
          }}
        />
      )}
      
      <div className="parallax-header__overlay" />
      
      <div 
        className="parallax-header__content"
        style={{
          opacity,
          transform: `translateY(${scrollY * 0.5}px)`,
        }}
      >
        {children}
      </div>
      
      <div className="parallax-header__fade" />
    </div>
  );
};

export default ParallaxHeader;
