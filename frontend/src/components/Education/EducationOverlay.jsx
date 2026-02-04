
import React, { useEffect, useState, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import useEducationStore from '../../stores/educationStore';
import { getTutorialForPath } from '../../data/tutorialContent';
import GhostCursor from './GhostCursor';

const EducationOverlay = () => {
  const location = useLocation();
  const { 
    isEducationMode, 
    activeTutorial, 
    currentStepIndex, 
    startTutorial, 
    stopTutorial, 
    nextStep 
  } = useEducationStore();

  const [targetRect, setTargetRect] = useState(null);
  const [currentStep, setCurrentStep] = useState(null);
  
  // Initialize tutorial when route changes or mode enabled
  useEffect(() => {
    if (!isEducationMode) {
        stopTutorial();
        return;
    }

    const steps = getTutorialForPath(location.pathname);
    if (steps && steps.length > 0) {
      startTutorial(location.pathname); // Use path as ID for now
    } else {
      stopTutorial();
    }
  }, [location.pathname, isEducationMode]);

  // Track target element for current step
  const observerRef = useRef(null);

  useEffect(() => {
    if (!activeTutorial) {
        setTargetRect(null);
        setCurrentStep(null);
        return;
    }

    const steps = getTutorialForPath(activeTutorial);
    if (!steps || !steps[currentStepIndex]) return;

    const step = steps[currentStepIndex];
    setCurrentStep(step);

    const findTarget = () => {
      const el = document.querySelector(step.target);
      if (el) {
        const rect = el.getBoundingClientRect();
        setTargetRect({
          top: rect.top,
          left: rect.left,
          width: rect.width,
          height: rect.height
        });
      } else {
        // Retry logic logic could go here, or just wait
        console.warn(`Education Mode: Target ${step.target} not found`);
      }
    };

    // Initial check
    findTarget();

    // Set up polling interval to track moving elements or late loading
    const interval = setInterval(findTarget, 500);

    return () => clearInterval(interval);

  }, [activeTutorial, currentStepIndex]);

  if (!isEducationMode || !activeTutorial || !currentStep) return null;

  return (
    <div className="fixed inset-0 pointer-events-none z-[9999] overflow-hidden">
      {/* Ghost Cursor Animation */}
      <AnimatePresence>
        {targetRect && <GhostCursor targetRect={targetRect} />}
      </AnimatePresence>

      {/* Tooltip Card */}
      <AnimatePresence mode="wait">
        {targetRect && (
          <motion.div
            key={currentStepIndex}
            initial={{ opacity: 0, y: 20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="absolute pointer-events-auto bg-black/80 backdrop-blur-md border border-cyan-500/50 rounded-xl p-4 w-80 shadow-[0_0_30px_rgba(6,182,212,0.2)]"
            style={{
              // Position tooltip relative to target, but keep on screen
              top: Math.min(window.innerHeight - 200, Math.max(20, targetRect.top + targetRect.height + 20)),
              left: Math.min(window.innerWidth - 340, Math.max(20, targetRect.left))
            }}
          >
            <div className="flex justify-between items-center mb-2">
                <h3 className="text-cyan-400 font-bold text-sm uppercase tracking-wider">
                    {currentStep.title}
                </h3>
                <span className="text-xs text-gray-500">
                    Step {currentStepIndex + 1}
                </span>
            </div>
            
            <p className="text-gray-300 text-sm mb-4 leading-relaxed">
                {currentStep.content}
            </p>

            <div className="flex justify-between items-center">
                <button 
                    onClick={stopTutorial}
                    className="text-xs text-gray-500 hover:text-white transition-colors"
                >
                    Skip
                </button>
                <button
                    onClick={() => {
                        const steps = getTutorialForPath(activeTutorial);
                        nextStep(steps.length);
                    }}
                    className="bg-cyan-500/20 hover:bg-cyan-500/40 text-cyan-400 text-xs px-3 py-1.5 rounded-lg border border-cyan-500/50 transition-all"
                >
                    Next
                </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
      
      {/* Target Highlight Ring */}
       {targetRect && (
        <motion.div
             className="absolute border-2 border-cyan-400/50 rounded-lg pointer-events-none"
             initial={{ opacity: 0 }}
             animate={{ 
                 opacity: 1,
                 top: targetRect.top - 4,
                 left: targetRect.left - 4,
                 width: targetRect.width + 8,
                 height: targetRect.height + 8
             }}
             transition={{ duration: 0.3 }}
        />
       )}
    </div>
  );
};

export default EducationOverlay;
