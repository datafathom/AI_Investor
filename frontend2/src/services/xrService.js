/**
 * xrService.js
 * 
 * Manages WebXR session lifecycle and hardware detection.
 */

import apiClient from './apiClient';

export const xrService = {
    isSupported: async () => {
        if (!navigator.xr) return false;
        try {
            return await navigator.xr.isSessionSupported('immersive-vr');
        } catch (e) {
            return false;
        }
    },

    getSpatialData: async () => {
        try {
            const response = await apiClient.get('/spatial/portfolio');
            return response.data;
        } catch (error) {
            console.error('Error fetching spatial data:', error);
            throw error;
        }
    }
};

export default xrService;
