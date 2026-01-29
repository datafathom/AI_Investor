import { create } from 'zustand';
import io from 'socket.io-client';

const useEvolutionStore = create((set, get) => ({
    generation: 0,
    bestFitness: 0,
    fitnessHistory: [],
    geneFrequencies: [],
    fitnessSurface: [],
    isEvolving: false,
    mutationRate: 0.1,
    socket: null,

    initSocket: () => {
        if (get().socket) return;
        
        const socket = io('http://localhost:5050');
        
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

        socket.on('fitness_surface_update', (data) => {
            set({ fitnessSurface: data.surface });
        });

        set({ socket });
    },

    setEvolving: (evolving) => set({ isEvolving: evolving }),
    setMutationRate: (rate) => set({ mutationRate: rate }),
    
    startEvolution: async () => {
        try {
            const response = await fetch('/api/v1/evolution/start', { method: 'POST' });
            const data = await response.json();
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

    spliceAgents: async (p1, p2) => {
        try {
            const response = await fetch('/api/v1/evolution/splice', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    parent1_id: p1.id,
                    parent2_id: p2.id,
                    parent1_genes: p1.genes,
                    parent2_genes: p2.genes
                })
            });
            return await response.json();
        } catch (error) {
            console.error('Splicing failed:', error);
        }
    }
}));

export default useEvolutionStore;
