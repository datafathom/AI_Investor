/**
 * Worker Manager
 * Singleton service to manage Web Worker instances and communication.
 */

class WorkerManager {
    constructor() {
        this.worker = null;
        this.pendingCallbacks = new Map();
        this.requestId = 0;
    }

    initialize() {
        if (!this.worker) {
            this.worker = new Worker(new URL('../workers/calculationWorker.js', import.meta.url), { type: 'module' });
            this.worker.onmessage = this.handleMessage.bind(this);
            this.worker.onerror = this.handleError.bind(this);
            console.log('WorkerManager: Worker initialized');
        }
    }

    handleMessage(event) {
        const { type, id, payload, error } = event.data;
        
        if (this.pendingCallbacks.has(id)) {
            const { resolve, reject } = this.pendingCallbacks.get(id);
            this.pendingCallbacks.delete(id);

            if (type === 'SUCCESS') {
                resolve(payload);
            } else {
                reject(new Error(error));
            }
        }
    }

    handleError(error) {
        console.error('WorkerManager: Worker error', error);
    }

    runTask(type, payload) {
        if (!this.worker) this.initialize();

        const id = ++this.requestId;
        
        return new Promise((resolve, reject) => {
            this.pendingCallbacks.set(id, { resolve, reject });
            this.worker.postMessage({ type, payload, id });
        });
    }

    // Specific Task Wrapper
    async runMonteCarlo(params) {
        return this.runTask('MONTE_CARLO', params);
    }

    async optimizePortfolio(params) {
        return this.runTask('OPTIMIZE_PORTFOLIO', params);
    }

    terminate() {
        if (this.worker) {
            this.worker.terminate();
            this.worker = null;
            this.pendingCallbacks.clear();
        }
    }
}

export const workerManager = new WorkerManager();
