
import { useEffect } from 'react';

/**
 * useHotkeys Hook
 * Registers global keyboard listeners for trading actions.
 * @param {Object} hotkeyMap - { key: callback } e.g. { 'Shift+B': handleBuy }
 */
export function useHotkeys(hotkeyMap) {
    useEffect(() => {
        const handleKeyDown = (event) => {
            // Build key string (e.g., "Shift+B", "Ctrl+S", "Escape")
            let keyStr = '';
            if (event.ctrlKey) keyStr += 'Ctrl+';
            if (event.shiftKey) keyStr += 'Shift+';
            if (event.altKey) keyStr += 'Alt+';

            const key = event.key.length === 1 ? event.key.toUpperCase() : event.key;
            keyStr += key;

            // Handle common cleanups for key strings
            const normalizedKey = keyStr.replace(/Shift\+Shift/, 'Shift').replace(/Ctrl\+Control/, 'Ctrl');

            if (hotkeyMap[normalizedKey]) {
                event.preventDefault();
                hotkeyMap[normalizedKey]();
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [hotkeyMap]);
}
