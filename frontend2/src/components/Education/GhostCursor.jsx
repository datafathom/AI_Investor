
import React from 'react';
import { motion } from 'framer-motion';

const GhostCursor = ({ targetRect }) => {
  if (!targetRect) return null;

  // Center of the target
  const x = targetRect.left + targetRect.width / 2;
  const y = targetRect.top + targetRect.height / 2;

  return (
    <motion.div
      className="fixed pointer-events-none z-[10000]"
      initial={{ x: window.innerWidth / 2, y: window.innerHeight / 2, opacity: 0 }}
      animate={{ 
        x: x, 
        y: y, 
        opacity: 1,
        transition: { 
          type: "spring", 
          stiffness: 80, 
          damping: 15,
          mass: 0.8
        } 
      }}
      exit={{ opacity: 0 }}
    >
      {/* Simulation of a mouse cursor icon */}
      <svg
        width="32"
        height="32"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="text-cyan-400 drop-shadow-[0_0_10px_rgba(34,211,238,0.8)]"
        style={{ transform: "translate(-50%, -50%)" }} // Center the cursor tip? Usually tip is top-left.
        // Let's align tip to x,y. SVG default is usually tip at 0,0.
        // If we want tip at x,y, no translation needed if 'fixed' coords are x,y.
      >
        <path
          d="M3 3L10.07 19.97L12.58 12.58L19.97 10.07L3 3Z"
          fill="currentColor"
          stroke="black"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
      
      {/* Pulse effect on "click" or arrival */}
      <motion.div
        className="absolute top-0 left-0 w-8 h-8 rounded-full border-2 border-cyan-400"
        initial={{ scale: 0.5, opacity: 0 }}
        animate={{ 
          scale: [1, 2], 
          opacity: [1, 0] 
        }}
        transition={{ 
            duration: 1.5, 
            repeat: Infinity,
            ease: "easeOut"
        }}
        style={{ transform: "translate(-25%, -25%)" }} // Center pulse on cursor tip roughly
      />
    </motion.div>
  );
};

export default GhostCursor;
