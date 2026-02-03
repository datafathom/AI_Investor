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
     * Streams code generation progress (Mock stream for Sandbox visualization).
     */
    async streamCode(taskId, onUpdate, onComplete) {
        const fullCode = `
import pandas as pd
import numpy as np

def normalize_yield_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Optimized yield normalization using vector subtraction.
    """
    try:
        # Step 1: Calculate basis points shift
        df['bp_shift'] = df['yield'].diff() * 100
        
        # Step 2: Apply Gaussian smoothing
        df['smooth'] = df['bp_shift'].rolling(window=5).mean()
        
        return df.dropna()
    except Exception as e:
        logger.error(f"Normalization failed: {e}")
        raise

if __name__ == "__main__":
    # Integration test
    data = pd.DataFrame({'yield': [4.2, 4.25, 4.18, 4.31]})
    print(normalize_yield_data(data))
        `;
        
        let current = "";
        const lines = fullCode.split('\n');
        for (let line of lines) {
            current += line + '\n';
            onUpdate(current);
            await new Promise(r => setTimeout(r, 50));
        }
        onComplete();
    }
}

export const autoCoderService = new AutoCoderService();
export default autoCoderService;

