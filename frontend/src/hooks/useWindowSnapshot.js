import { useCallback } from 'react';
import html2canvas from 'html2canvas';
import useWindowStore from '../stores/windowStore';

/**
 * Hook to capture a snapshot of a window for taskbar previews.
 * Uses html2canvas to generate a data URL and updates the window store.
 */
const useWindowSnapshot = () => {
    const updateSnapshot = useWindowStore((state) => state.updateSnapshot);

    const captureSnapshot = useCallback(async (windowId, element) => {
        if (!element) return;

        try {
            // Optimization: Use a slightly smaller scale for the preview to save memory/perf
            const canvas = await html2canvas(element, {
                scale: 0.5, // 50% scale is plenty for a small hover preview
                logging: false,
                useCORS: true,
                backgroundColor: null,
                // Don't capture scrollbars
                ignoreElements: (el) => el.classList.contains('simplebar-scrollbar')
            });

            const dataUrl = canvas.toDataURL('image/webp', 0.5); // WebP with 50% quality
            updateSnapshot(windowId, dataUrl);
            console.log(`[useWindowSnapshot] Captured snapshot for ${windowId}`);
            
            // Cleanup canvas
            canvas.width = 0;
            canvas.height = 0;
        } catch (error) {
            console.error('[useWindowSnapshot] Failed to capture snapshot:', error);
        }
    }, [updateSnapshot]);

    return { captureSnapshot };
};

export default useWindowSnapshot;
