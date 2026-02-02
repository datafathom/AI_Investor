/**
 * ==============================================================================
 * FILE: frontend2/src/stores/incidentStore.js
 * ROLE: State Management
 * PURPOSE: Manages Ops incident monitoring and triggering.
 * ==============================================================================
 */

import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useIncidentStore = create((set) => ({
    incidents: [],
    loading: false,
    triggering: false,
    error: null,
    lastTriggered: null,

    fetchIncidents: async (mock = true) => {
        set({ loading: true, error: null });
        try {
            const response = await apiClient.get('/ops/incidents', { params: { mock } });
            set({ incidents: response.data, loading: false });
        } catch (error) {
            console.error('Fetch incidents failed:', error);
            set({ error: error.message, loading: false });
        }
    },

    triggerIncident: async (title, urgency = "high", mock = true) => {
        set({ triggering: true, error: null });
        try {
            const response = await apiClient.post('/ops/incidents/trigger', 
                { title, urgency },
                { params: { mock } }
            );
            
            set(state => ({ 
                incidents: [response.data, ...state.incidents],
                lastTriggered: response.data,
                triggering: false 
            }));
            return response.data;
        } catch (error) {
            console.error('Trigger incident failed:', error);
            set({ error: error.message, triggering: false });
        }
    }
}));

export default useIncidentStore;
