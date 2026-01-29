import apiClient from './apiClient';

/**
 * Search Service
 * Handles client-side indexing and server-side search fallback.
 */
class SearchService {
    constructor() {
        this.index = {
            symbols: [],
            agents: [],
            clients: []
        };
        this.lastIndexUpdate = null;
    }

    /**
     * Refreshes the local index from the server.
     */
    async refreshIndex() {
        try {
            const response = await apiClient.get('/search/index');
            if (response.success) {
                this.index = response.data;
                this.lastIndexUpdate = new Date();
                return true;
            }
            return false;
        } catch (error) {
            console.error('Failed to refresh search index:', error);
            return false;
        }
    }

    /**
     * Performs a local search against the index.
     * @param {string} query 
     */
    localSearch(query) {
        if (!query) return [];
        const q = query.toLowerCase();
        
        const results = [];
        
        // Search Symbols
        this.index.symbols.forEach(s => {
            if (s.label.toLowerCase().includes(q)) {
                results.push(s);
            }
        });

        // Search Agents
        this.index.agents.forEach(a => {
            if (a.label.toLowerCase().includes(q)) {
                results.push(a);
            }
        });

        // Search Clients
        this.index.clients.forEach(c => {
            if (c.label.toLowerCase().includes(q)) {
                results.push(c);
            }
        });

        return results;
    }

    /**
     * Performs an async server-side search for deep queries.
     * @param {string} query 
     */
    async serverSearch(query) {
        if (!query || query.length < 3) return [];
        try {
            const response = await apiClient.get('/search/query', { params: { q: query } });
            return response.success ? response.data : [];
        } catch (error) {
            console.error('Server search failed:', error);
            return [];
        }
    }
}

export const searchService = new SearchService();
export default searchService;
