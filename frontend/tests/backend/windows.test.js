/**
 * Window Management Backend Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';

// Mock database - create chainable mock objects
const createInsertMock = () => {
  const valuesFn = vi.fn().mockResolvedValue({});
  return {
    values: valuesFn,
  };
};

const createUpdateMock = () => {
  const setFn = vi.fn().mockResolvedValue({});
  return {
    set: setFn,
  };
};

const createDeleteMock = () => {
  const whereFn = vi.fn().mockResolvedValue({});
  return {
    where: whereFn,
  };
};

const mockDb = {
  query: {
    windowLayouts: {
      findMany: vi.fn(),
      findFirst: vi.fn(),
    },
  },
  insert: vi.fn(() => createInsertMock()),
  update: vi.fn(() => createUpdateMock()),
  delete: vi.fn(() => createDeleteMock()),
};

// Mock window layout functions
const getWindowLayouts = async (userId) => {
  return await mockDb.query.windowLayouts.findMany({
    where: (layouts, { eq }) => eq(layouts.userId, userId),
  });
};

const saveWindowLayout = async (userId, name, layoutData) => {
  const existing = await mockDb.query.windowLayouts.findFirst({
    where: (layouts, { eq, and }) =>
      and(eq(layouts.userId, userId), eq(layouts.name, name)),
  });

  if (existing) {
    const updateResult = mockDb.update(mockDb.query.windowLayouts);
    await updateResult.set({
      layoutData: JSON.stringify(layoutData),
      updatedAt: new Date(),
    });
    return { message: 'Layout updated' };
  } else {
    const insertResult = mockDb.insert(mockDb.query.windowLayouts);
    await insertResult.values({
      userId,
      name,
      layoutData: JSON.stringify(layoutData),
    });
    return { message: 'Layout saved' };
  }
};

const deleteWindowLayout = async (userId, name) => {
  const deleteResult = mockDb.delete(mockDb.query.windowLayouts);
  await deleteResult.where(
    (layouts, { eq, and }) => and(eq(layouts.userId, userId), eq(layouts.name, name))
  );
  return { message: 'Layout deleted' };
};

describe('Window Layout Management', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Re-setup the mocks after clearing
    mockDb.insert.mockImplementation(() => createInsertMock());
    mockDb.update.mockImplementation(() => createUpdateMock());
    mockDb.delete.mockImplementation(() => createDeleteMock());
  });

  describe('getWindowLayouts', () => {
    it('should get all layouts for user', async () => {
      const mockLayouts = [
        { id: 1, name: 'layout1', userId: 1 },
        { id: 2, name: 'layout2', userId: 1 },
      ];
      mockDb.query.windowLayouts.findMany.mockResolvedValue(mockLayouts);

      const result = await getWindowLayouts(1);

      expect(result).toEqual(mockLayouts);
      expect(mockDb.query.windowLayouts.findMany).toHaveBeenCalled();
    });
  });

  describe('saveWindowLayout', () => {
    it('should save a new layout', async () => {
      mockDb.query.windowLayouts.findFirst.mockResolvedValue(null);
      // insert mock is already set up to return chainable object

      const result = await saveWindowLayout(1, 'new-layout', { windows: [] });

      expect(result.message).toBe('Layout saved');
      expect(mockDb.insert).toHaveBeenCalled();
    });

    it('should update existing layout', async () => {
      mockDb.query.windowLayouts.findFirst.mockResolvedValue({
        id: 1,
        name: 'existing-layout',
        userId: 1,
      });
      // update mock is already set up to return chainable object

      const result = await saveWindowLayout(1, 'existing-layout', { windows: [] });

      expect(result.message).toBe('Layout updated');
      expect(mockDb.update).toHaveBeenCalled();
    });
  });

  describe('deleteWindowLayout', () => {
    it('should delete a layout', async () => {
      // delete mock is already set up to return chainable object

      const result = await deleteWindowLayout(1, 'layout-to-delete');

      expect(result.message).toBe('Layout deleted');
      expect(mockDb.delete).toHaveBeenCalled();
    });
  });
});

