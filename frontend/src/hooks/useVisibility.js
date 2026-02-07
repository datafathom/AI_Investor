import { useState, useEffect, useRef } from 'react';

/**
 * useVisibility - Hook to track if an element is visible in the viewport
 * and if the page tab itself is active.
 * 
 * @param {Object} options - IntersectionObserver options
 * @returns {Array} [elementRef, isVisible]
 */
export const useVisibility = (options = { threshold: 0.1 }) => {
  const [isVisible, setIsVisible] = useState(true);
  const [isTabActive, setIsTabActive] = useState(true);
  const elementRef = useRef(null);
  const optionsRef = useRef(options);

  useEffect(() => {
    // Ensure we use the same options for the life of the hook if not explicitly changed
    const currentOptions = optionsRef.current;
    const handleVisibilityChange = () => {
      setIsTabActive(document.visibilityState === 'visible');
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);

    // 2. Track Element Visibility (Viewport)
    const observer = new IntersectionObserver(([entry]) => {
      setIsVisible(entry.isIntersecting);
    }, currentOptions);

    if (elementRef.current) {
      observer.observe(elementRef.current);
    }

    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      if (elementRef.current) {
        observer.unobserve(elementRef.current);
      }
    };
  }, []); // Only setup once

  // Component is "actively visible" only if tab is active AND element is in viewport
  return [elementRef, isVisible && isTabActive];
};

export default useVisibility;
