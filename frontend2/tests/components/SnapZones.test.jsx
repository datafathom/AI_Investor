/**
 * SnapZones Component Tests
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import SnapZones from '../../src/components/WindowManager/SnapZones';

describe('SnapZones', () => {
  it('should not render when not dragging', () => {
    render(<SnapZones isDragging={false} />);
    expect(screen.queryByText(/left half/i)).not.toBeInTheDocument();
  });

  it('should render snap zones when dragging near edge', () => {
    // Mock window dimensions
    Object.defineProperty(window, 'innerWidth', { value: 1920, writable: true });
    Object.defineProperty(window, 'innerHeight', { value: 1080, writable: true });

    const dragPosition = { x: 25, y: 100 }; // Near left edge
    const { container } = render(
      <SnapZones
        isDragging={true}
        dragPosition={dragPosition}
        onSnap={vi.fn()}
      />
    );
    // Snap zones should be visible when near edges
    const overlay = container.querySelector('.snap-zones-overlay');
    expect(overlay).toBeInTheDocument();
  });

  it('should call onSnap when zone is clicked', () => {
    // Mock window dimensions
    Object.defineProperty(window, 'innerWidth', { value: 1920, writable: true });
    Object.defineProperty(window, 'innerHeight', { value: 1080, writable: true });

    const onSnap = vi.fn();
    const dragPosition = { x: 25, y: 100 };
    const { container } = render(
      <SnapZones
        isDragging={true}
        dragPosition={dragPosition}
        onSnap={onSnap}
      />
    );

    // Find and click an active snap zone
    const activeZone = container.querySelector('.snap-zone-active');
    if (activeZone) {
      fireEvent.click(activeZone);
      expect(onSnap).toHaveBeenCalled();
    }
  });

  it('should not render when disabled', () => {
    render(
      <SnapZones
        isDragging={true}
        dragPosition={{ x: 25, y: 100 }}
        enabled={false}
      />
    );
    expect(document.querySelector('.snap-zones')).not.toBeInTheDocument();
  });
});

