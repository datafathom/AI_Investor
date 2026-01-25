/**
 * Data Cruncher Web Worker
 * Performs heavy time-series analysis in a background thread
 */

self.onmessage = (e) => {
    const { type, data } = e.data;

    if (type === 'PROCESS_PORTFOLIO') {
        // High-intensity calculation simulation
        console.time('Worker Process');
        const processed = data.map(item => ({
            ...item,
            calcValue: item.value * Math.random(),
            timestamp: Date.now()
        }));
        
        // Block for a split second to simulate load
        const start = Date.now();
        while(Date.now() - start < 50) {} 

        console.timeEnd('Worker Process');
        self.postMessage({ type: 'SUCCESS', payload: processed });
    }
};
