import { create } from 'zustand';
import axios from 'axios';

const useEducationStore = create((set, get) => ({
  isEducationMode: false,
  activeTutorial: null,
  currentStepIndex: 0,
  isPlaying: false,
  completedTutorials: [],

  // Toggle the global mode
  toggleEducationMode: () => set((state) => ({ 
    isEducationMode: !state.isEducationMode,
    // Reset current tutorial if turning off
    activeTutorial: state.isEducationMode ? null : state.activeTutorial 
  })),

  setEducationMode: (isActive) => set({ isEducationMode: isActive }),

  // Load progress from backend
  loadProgress: async () => {
    try {
        const userId = 'dev-user'; // TODO: Get from authStore
        const response = await axios.get(`/api/v1/education/progress?user_id=${userId}`);
        set({ completedTutorials: response.data.completed_tutorials });
    } catch (error) {
        console.error("Failed to load education progress:", error);
    }
  },

  // Start a specific tutorial sequence
  startTutorial: (tutorialId) => {
    // Optional: Check if already completed?
    // const { completedTutorials } = get();
    // if (completedTutorials.includes(tutorialId)) return;

    set({
      activeTutorial: tutorialId,
      currentStepIndex: 0,
      isPlaying: true
    });
  },

  stopTutorial: () => set({
    activeTutorial: null,
    currentStepIndex: 0,
    isPlaying: false
  }),

  nextStep: async (totalSteps) => {
    const { currentStepIndex, activeTutorial, completedTutorials } = get();
    
    if (currentStepIndex < totalSteps - 1) {
      set({ currentStepIndex: currentStepIndex + 1 });
    } else {
      // Tutorial finished
      // Call backend to persist
      try {
          const userId = 'dev-user'; 
          const response = await axios.post('/api/v1/education/complete', {
              user_id: userId,
              tutorial_id: activeTutorial
          });
          
          set({ 
            activeTutorial: null, 
            currentStepIndex: 0, 
            isPlaying: false,
            completedTutorials: response.data.completed_tutorials
          });
      } catch (error) {
          console.error("Failed to save progress:", error);
          // Fallback optimistic update
          set({ 
            activeTutorial: null, 
            currentStepIndex: 0, 
            isPlaying: false,
            completedTutorials: [...completedTutorials, activeTutorial]
          });
      }
    }
  },

  skipTutorial: () => set({
    activeTutorial: null,
    currentStepIndex: 0,
    isPlaying: false
  })
}));

export default useEducationStore;
