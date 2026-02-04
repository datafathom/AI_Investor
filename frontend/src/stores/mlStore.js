import { create } from 'zustand';
import mlService from '../services/mlService';

const useMLStore = create((set, get) => ({
    // State
    trainingJobs: [],
    modelVersions: [],
    deployments: [],
    isLoading: false,
    error: null,
    
    // Actions
    fetchTrainingJobs: async (userId) => {
        set({ isLoading: true, error: null });
        try {
            const data = await mlService.getTrainingJobs(userId);
            set({ trainingJobs: data || [], isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
            console.error('Failed to fetch training jobs:', error);
        }
    },

    fetchModelVersions: async (userId) => {
        set({ isLoading: true, error: null });
        try {
            const data = await mlService.getModelVersions(userId);
            set({ modelVersions: data || [], isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
            console.error('Failed to fetch model versions:', error);
        }
    },

    fetchDeployments: async (userId) => {
        set({ isLoading: true, error: null });
        try {
            const data = await mlService.getDeployments(userId);
            set({ deployments: data || [], isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
            console.error('Failed to fetch deployments:', error);
        }
    },

    startTrainingJob: async (userId, modelType, dataset) => {
        set({ isLoading: true, error: null });
        try {
            await mlService.startTrainingJob({
                user_id: userId,
                model_type: modelType,
                dataset
            });
            // Refresh list
            await get().fetchTrainingJobs(userId);
            set({ isLoading: false });
            return true;
        } catch (error) {
            set({ error: error.message, isLoading: false });
            console.error('Failed to start training job:', error);
            return false;
        }
    },

    deployModel: async (userId, modelId) => {
        set({ isLoading: true, error: null });
        try {
            await mlService.deployModel({ model_id: modelId });
            // Refresh lists
            await get().fetchDeployments(userId);
            await get().fetchModelVersions(userId);
            set({ isLoading: false });
            return true;
        } catch (error) {
            set({ error: error.message, isLoading: false });
            console.error('Failed to deploy model:', error);
            return false;
        }
    }
}));

export default useMLStore;
