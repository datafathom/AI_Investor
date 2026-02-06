import apiClient from './apiClient';

class AutoCoderService {
    constructor() {
        this.baseUrl = '/dev';
    }

    /**
     * Triggers AI code generation for a specific task.
     */
    async generateCode(task) {
        try {
            const response = await apiClient.post(`${this.baseUrl}/generate`, { task });
            return response.code;
        } catch (error) {
            console.error('AutoCoder Store Error [generate]:', error);
            throw error;
        }
    }

    /**
     * Validates generated code against the execution environment.
     */
    async validateCode(code) {
        try {
            const response = await apiClient.post(`${this.baseUrl}/validate`, { code });
            return response.is_valid;
        } catch (error) {
            console.error('AutoCoder Store Error [validate]:', error);
            return false;
        }
    }

    /**
     * Deploys validated code to the active registry.
     */
    async deployModule(name, code) {
        try {
            const response = await apiClient.post(`${this.baseUrl}/deploy`, { name, code });
            return response.data;
        } catch (error) {
            console.error('AutoCoder Store Error [deploy]:', error);
            throw error;
        }
    }

    /**
     * Gets the current status of the AutoCoder registry.
     */
    async getStatus() {
        try {
            const response = await apiClient.get(`${this.baseUrl}/status`);
            return response.data;
        } catch (error) {
            console.error('AutoCoder Store Error [status]:', error);
            return { status: 'offline', modules: [] };
        }
    }
    /**
     * Gets pending optimization tasks for the sandbox.
     */
    getTasks() {
        return [
            { id: 't1', name: 'Data Normalizer', description: 'Optimize pandas vectorized operations for 10Y yield data.' },
            { id: 't2', name: 'API Shield', description: 'Implement rate limiting and JWT validation for high-traffic endpoints.' },
            { id: 't3', name: 'Sentiment Engine', description: 'Refactor social media NLP pipeline for lower latency.' },
            { id: 't4', name: 'Port Scanner', description: 'Automated auditing of open internal services.' }
        ];
    }

    /**
     * Streams code generation progress (Simulated stream over real API result).
     */
    async streamCode(taskId, onUpdate, onComplete) {
        const task = this.getTasks().find(t => t.id === taskId);
        if (!task) return onComplete();

        try {
            const code = await this.generateCode(task.description);
            
            let current = "";
            const lines = code.split('\n');
            for (let line of lines) {
                current += line + '\n';
                onUpdate(current);
                await new Promise(r => setTimeout(r, 30)); // Typing effect
            }
            onComplete();
        } catch (err) {
            onUpdate(`# ERROR: Generation failed\n# ${err.message}`);
            onComplete();
        }
    }
}

export const autoCoderService = new AutoCoderService();
export default autoCoderService;

