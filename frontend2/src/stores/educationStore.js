import { create } from 'zustand';
import apiClient from '../services/apiClient';

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

  // State for Dashboard
  courses: [],
  userProgress: null,
  certifications: [],
  loading: false,
  error: null,

  // Actions for Dashboard
  fetchCourses: async () => {
    set({ loading: true, error: null });
    try {
      const response = await apiClient.get('/education/courses');
      set({ courses: response.data?.data || response.data || [], loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },

  fetchUserProgress: async (userId) => {
    set({ loading: true, error: null });
    try {
      const response = await apiClient.get('/education/progress', { params: { user_id: userId } });
      set({ userProgress: response.data?.data || response.data || null, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },

  fetchCertifications: async (userId) => {
    set({ loading: true, error: null });
    try {
      const response = await apiClient.get('/education/certifications', { params: { user_id: userId } });
      set({ certifications: response.data?.data || response.data || [], loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },

  enrollInCourse: async (userId, courseId) => {
    set({ loading: true, error: null });
    try {
      await apiClient.post('/education/enroll', { user_id: userId, course_id: courseId });
      await get().fetchUserProgress(userId); // Refresh progress
      set({ loading: false });
      return true;
    } catch (error) {
      set({ error: error.message, loading: false });
      return false;
    }
  },

  // Load progress from backend (Legacy/Tutorials)
  loadProgress: async () => {
    try {
        const userId = 'dev-user'; // TODO: Get from authStore
        const response = await apiClient.get('/education/progress', { params: { user_id: userId } });
        const result = response.data?.data || response.data || {};
        set({ completedTutorials: result.completed_tutorials || [] });
    } catch (error) {
        console.error("Failed to load education progress:", error);
    }
  },

  // Start a specific tutorial sequence
  startTutorial: (tutorialId) => {
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
      // Tutorial finished - Call backend to persist
      try {
          const userId = 'dev-user'; 
          const response = await apiClient.post('/education/complete', {
              user_id: userId,
              tutorial_id: activeTutorial
          });
          
          const result = response.data?.data || response.data || {};
          set({ 
            activeTutorial: null, 
            currentStepIndex: 0, 
            isPlaying: false,
            completedTutorials: result.completed_tutorials || completedTutorials
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
