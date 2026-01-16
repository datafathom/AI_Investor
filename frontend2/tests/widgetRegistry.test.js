/**
 * Widget Registry Tests
 */

import { describe, it, expect, beforeEach } from 'vitest';
import widgetRegistry from '../src/core/WidgetRegistry';

describe('WidgetRegistry', () => {
  beforeEach(() => {
    widgetRegistry.clear();
  });

  it('should register a widget', () => {
    const widget = widgetRegistry.register({
      id: 'test-widget',
      name: 'Test Widget',
      component: () => null,
    });

    expect(widget).toBeDefined();
    expect(widget.id).toBe('test-widget');
    expect(widgetRegistry.getAll().length).toBe(1);
  });

  it('should find widget by ID', () => {
    widgetRegistry.register({
      id: 'test',
      name: 'Test',
      component: () => null,
    });

    const widget = widgetRegistry.get('test');
    expect(widget).toBeDefined();
    expect(widget.name).toBe('Test');
  });

  it('should search widgets', () => {
    widgetRegistry.register({
      id: 'widget-1',
      name: 'Chart Widget',
      description: 'A chart widget',
      component: () => null,
    });

    widgetRegistry.register({
      id: 'widget-2',
      name: 'Table Widget',
      description: 'A table widget',
      component: () => null,
    });

    const results = widgetRegistry.search('chart');
    expect(results.length).toBe(1);
    expect(results[0].id).toBe('widget-1');
  });

  it('should check dependencies', () => {
    widgetRegistry.register({
      id: 'dep-widget',
      name: 'Dependency',
      component: () => null,
    });

    widgetRegistry.register({
      id: 'main-widget',
      name: 'Main',
      component: () => null,
      dependencies: ['dep-widget'],
    });

    const check = widgetRegistry.checkDependencies('main-widget');
    expect(check.satisfied).toBe(true);
    expect(check.missing.length).toBe(0);
  });
});

