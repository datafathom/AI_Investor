import { create } from 'zustand';
import io from 'socket.io-client';
import apiClient from '../services/apiClient';

const useEvolutionStore = create((set, get) => ({
    generation: 0,
    bestFitness: 0,
    fitnessHistory: [],
    geneFrequencies: [],
    fitnessSurface: [],
    isEvolving: false,
    mutationRate: 0.1,
    socket: null,
    hallOfFame: [],
    genePulse: null,
    playbackResult: null,
    isPlaybackRunning: false,

    initSocket: () => {
        if (get().socket) return;
        
        const socket = io('http://localhost:5050', { transports: ['polling'] });
        
        socket.on('connect', () => {
            console.log('Evolution Socket Connected');
            socket.emit('subscribe', { channel: 'evolution' });
        });

        socket.on('evolution_status_update', (data) => {
            if (data.command === 'pause') set({ isEvolving: false });
            if (data.command === 'resume') set({ isEvolving: true });
        });

        socket.on('mutation_rate_changed', (data) => {
            set({ mutationRate: data.rate });
        });

        socket.on('gene_frequency_update', (data) => {
            set({ geneFrequencies: data.frequencies });
        });

        socket.on('hall_of_fame_update', (data) => {
            set({ hallOfFame: data.agents });
        });

        socket.on('fitness_surface_update', (data) => {
            set({ fitnessSurface: data.surface });
        });

        set({ socket });
    },

    setEvolving: (evolving) => set({ isEvolving: evolving }),
    setMutationRate: (rate) => set({ mutationRate: rate }),
    
    startEvolution: async () => {
        try {
            const data = await apiClient.post('/evolution/start');
            if (data.status === 'success') {
                set({ 
                    isEvolving: true, 
                    generation: data.current_generation,
                    fitnessHistory: data.history 
                });
            }
        } catch (error) {
            console.error('Failed to start evolution:', error);
        }
    },

    spliceAgents: async (p1, p2, resolvedGenes = null) => {
        try {
            const data = await apiClient.post('/evolution/splice', {
                parent1_id: p1.id,
                parent2_id: p2.id,
                parent1_genes: p1.genes,
                parent2_genes: p2.genes,
                resolved_genes: resolvedGenes
            });
            return data;
        } catch (error) {
            console.error('Splicing failed:', error);
        }
    },

    runPlayback: async (agentId, genes) => {
        set({ isPlaybackRunning: true, playbackResult: null });
        try {
            // Mocking price data for playback demo
            const mockPriceData = Array.from({ length: 100 }, (_, i) => ({
                timestamp: Date.now() - (100 - i) * 3600000,
                close: 100 + Math.sin(i / 5) * 10 + (Math.random() - 0.5) * 5
            }));

            const data = await apiClient.post('/evolution/playback', {
                agent_id: agentId,
                genes: genes,
                price_data: mockPriceData
            });

            if (data.status === 'success') {
                set({ playbackResult: data.data });
            }
        } catch (error) {
            console.error('Playback failed:', error);
        } finally {
            set({ isPlaybackRunning: false });
        }
    },

    fetchGenePulse: async (agentId, genes) => {
        try {
            const data = await apiClient.post(`/evolution/pulse/${agentId}`, { genes });
            if (data.status === 'success') {
                set({ genePulse: data.data });
            }
        } catch (error) {
            console.error('Pulse fetch failed:', error);
        }
    }
}));

export default useEvolutionStore;
