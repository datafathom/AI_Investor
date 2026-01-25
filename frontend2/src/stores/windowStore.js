import { create } from 'zustand';

// Generate unique ID
const nanoid = () => Math.random().toString(36).substr(2, 9);

const useWindowStore = create((set, get) => ({
  windows: [],
  activeWindowId: null,
  nextZIndex: 100,

  // Add a new window
  addWindow: (windowConfig) => {
    const newWindow = {
      id: windowConfig.id || nanoid(),
      title: windowConfig.title || 'Untitled',
      x: windowConfig.x || 100,
      y: windowConfig.y || 100,
      width: windowConfig.width || 400,
      height: windowConfig.height || 300,
      zIndex: get().nextZIndex,
      isMinimized: false,
      isMaximized: false,
      component: windowConfig.component || null, // Component string/type
      props: windowConfig.props || {},
      ...windowConfig
    };

    set((state) => ({
      windows: [...state.windows, newWindow],
      activeWindowId: newWindow.id,
      nextZIndex: state.nextZIndex + 1
    }));
    return newWindow.id;
  },

  // Close window
  closeWindow: (id) => set((state) => ({
    windows: state.windows.filter((w) => w.id !== id),
    activeWindowId: state.activeWindowId === id ? null : state.activeWindowId
  })),

  // Focus window (bring to front)
  focusWindow: (id) => set((state) => {
    if (state.activeWindowId === id) return {}; // Already active
    const maxZ = Math.max(...state.windows.map(w => w.zIndex), 99);
    return {
      activeWindowId: id,
      windows: state.windows.map(w => 
        w.id === id ? { ...w, zIndex: maxZ + 1 } : w
      ),
      nextZIndex: maxZ + 2
    };
  }),

  // Minimize window
  minimizeWindow: (id) => set((state) => ({
    windows: state.windows.map(w => 
      w.id === id ? { ...w, isMinimized: true } : w
    ),
    activeWindowId: null
  })),

  // Restore window
  restoreWindow: (id) => set((state) => ({
    windows: state.windows.map(w => 
      w.id === id ? { ...w, isMinimized: false } : w
    ),
    activeWindowId: id
  })),

  // Maximize/Normalize window
  toggleMaximize: (id) => set((state) => ({
    windows: state.windows.map(w => 
      w.id === id ? { ...w, isMaximized: !w.isMaximized } : w
    ),
    activeWindowId: id
  })),

  // Update window position/size
  updateWindow: (id, updates) => set((state) => ({
    windows: state.windows.map(w => 
      w.id === id ? { ...w, ...updates } : w
    )
  })),
  
  // Set full layout (for persistence)
  setWorkspace: (windows) => set({ 
    windows, 
    activeWindowId: null,
    nextZIndex: Math.max(...windows.map(w => w.zIndex || 100), 100) + 1
  })
}));

export default useWindowStore;
