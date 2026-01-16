/**
 * Window Manager Tests
 */

import { describe, it, expect, beforeEach } from 'vitest';
import windowManager from '../src/services/windowManager';

describe('WindowManager', () => {
  beforeEach(() => {
    windowManager.clear();
  });

  it('should register a window', () => {
    const window = windowManager.registerWindow({
      id: 'test-window',
      title: 'Test Window',
      component: 'TestComponent',
    });

    expect(window).toBeDefined();
    expect(window.id).toBe('test-window');
    expect(window.title).toBe('Test Window');
    expect(windowManager.getAllWindows().length).toBe(1);
  });

  it('should bring window to front', () => {
    const w1 = windowManager.registerWindow({ id: 'w1', title: 'Window 1', component: 'C1' });
    const w2 = windowManager.registerWindow({ id: 'w2', title: 'Window 2', component: 'C2' });

    const initialZIndex = w1.zIndex;
    windowManager.bringToFront('w1');

    const updatedW1 = windowManager.getWindow('w1');
    expect(updatedW1.zIndex).toBeGreaterThan(initialZIndex);
  });

  it('should minimize and restore window', () => {
    windowManager.registerWindow({
      id: 'test',
      title: 'Test',
      component: 'C',
      size: { width: 400, height: 300 },
    });

    windowManager.minimizeWindow('test');
    const minimized = windowManager.getWindow('test');
    expect(minimized.state).toBe('minimized');
    expect(minimized.size.height).toBe(28);

    windowManager.restoreWindow('test');
    const restored = windowManager.getWindow('test');
    expect(restored.state).toBe('normal');
  });

  it('should save and load layout', () => {
    windowManager.registerWindow({ id: 'w1', title: 'W1', component: 'C1' });
    windowManager.registerWindow({ id: 'w2', title: 'W2', component: 'C2' });

    const layout = windowManager.saveLayout('test-layout');
    expect(layout).toBeDefined();
    expect(layout.windows.length).toBe(2);

    windowManager.clear();
    const loaded = windowManager.loadLayout('test-layout');
    expect(loaded).toBeDefined();
    expect(windowManager.getAllWindows().length).toBe(2);
  });
});

