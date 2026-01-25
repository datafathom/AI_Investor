/**
 * ==============================================================================
 * FILE: frontend2/src/stores/incidentStore.js
 * ROLE: State Management
 * PURPOSE: Manages Ops incident monitoring and triggering.
 * ==============================================================================
 */

import { create } from 'zustand';

const useIncidentStore = create((set) => ({
    incidents: [],
    loading: false,
    triggering: false,
    error: null,
    lastTriggered: null,

    fetchIncidents: async (mock = true) => {
        set({ loading: true, error: null });
        try {
            const response = await fetch(`/api/v1/ops/incidents?mock=${mock}`);
            if (!response.ok) throw new Error('Failed to fetch incidents');
            const data = await response.json();
            set({ incidents: data, loading: false });
        } catch (error) {
            console.error('Fetch incidents failed:', error);
            set({ error: error.message, loading: false });
        }
    },

    triggerIncident: async (title, urgency = "high", mock = true) => {
        set({ triggering: true, error: null });
        try {
            const response = await fetch(`/api/v1/ops/incidents/trigger?mock=${mock}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title, urgency })
            });
            
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to trigger incident');
            
            set(state => ({ 
                incidents: [data, ...state.incidents],
                lastTriggered: data,
                triggering: false 
            }));
            return data;
        } catch (error) {
            console.error('Trigger incident failed:', error);
            set({ error: error.message, triggering: false });
        }
    }
}));

export default useIncidentStore;
