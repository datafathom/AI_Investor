/**
 * Theme Engine
 * 
 * Runtime theme switching and management system.
 * Supports multiple themes with live switching without page reload.
 */

class ThemeEngine {
  constructor() {
    this.currentTheme = 'light';
    this.themes = new Map();
    this.listeners = new Set();
    this.cssVariables = new Map();
    
    // Load saved theme preference
    this.loadSavedTheme();
  }

  /**
   * Register a theme
   */
  registerTheme(themeData) {
    const {
      id,
      name,
      colors,
      spacing,
      typography,
      shadows,
      borderRadius,
      animations,
    } = themeData;

    if (!id || !name) {
      throw new Error('Theme must have id and name');
    }

    const theme = {
      id,
      name,
      colors: colors || {},
      spacing: spacing || {},
      typography: typography || {},
      shadows: shadows || {},
      borderRadius: borderRadius || {},
      animations: animations || {},
      registeredAt: new Date(),
    };

    this.themes.set(id, theme);
    this.emit('theme:registered', theme);
    return theme;
  }

  /**
   * Apply theme
   */
  applyTheme(themeId) {
    const theme = this.themes.get(themeId);
    if (!theme) {
      console.warn(`Theme ${themeId} not found`);
      return false;
    }

    this.currentTheme = themeId;
    this._applyThemeToDOM(theme);
    this._saveThemePreference(themeId);
    this.emit('theme:applied', theme);
    return true;
  }

  /**
   * Apply theme styles to DOM
   */
  _applyThemeToDOM(theme) {
    const root = document.documentElement;

    // Apply color variables
    if (theme.colors) {
      Object.entries(theme.colors).forEach(([key, value]) => {
        if (typeof value === 'object') {
          Object.entries(value).forEach(([subKey, subValue]) => {
            root.style.setProperty(`--color-${key}-${subKey}`, subValue);
          });
        } else {
          root.style.setProperty(`--color-${key}`, value);
        }
      });
    }

    // Apply spacing variables
    if (theme.spacing) {
      Object.entries(theme.spacing).forEach(([key, value]) => {
        root.style.setProperty(`--spacing-${key}`, `${value}px`);
      });
    }

    // Apply typography variables
    if (theme.typography) {
      Object.entries(theme.typography).forEach(([key, value]) => {
        if (typeof value === 'object') {
          Object.entries(value).forEach(([subKey, subValue]) => {
            root.style.setProperty(`--font-${key}-${subKey}`, subValue);
          });
        } else {
          root.style.setProperty(`--font-${key}`, value);
        }
      });
    }

    // Apply shadow variables
    if (theme.shadows) {
      Object.entries(theme.shadows).forEach(([key, value]) => {
        root.style.setProperty(`--shadow-${key}`, value);
      });
    }

    // Apply border radius variables
    if (theme.borderRadius) {
      Object.entries(theme.borderRadius).forEach(([key, value]) => {
        root.style.setProperty(`--radius-${key}`, `${value}px`);
      });
    }

    // Apply animation variables
    if (theme.animations) {
      Object.entries(theme.animations).forEach(([key, value]) => {
        if (typeof value === 'object') {
          Object.entries(value).forEach(([subKey, subValue]) => {
            root.style.setProperty(`--animation-${key}-${subKey}`, subValue);
          });
        } else {
          root.style.setProperty(`--animation-${key}`, value);
        }
      });
    }

    // Update body class for theme-specific styles
    document.body.className = document.body.className
      .replace(/theme-\w+/g, '')
      .trim();
    document.body.classList.add(`theme-${theme.id}`);
  }

  /**
   * Get current theme
   */
  getCurrentTheme() {
    return this.themes.get(this.currentTheme) || null;
  }

  /**
   * Get all themes
   */
  getAllThemes() {
    return Array.from(this.themes.values());
  }

  /**
   * Get theme by ID
   */
  getTheme(themeId) {
    return this.themes.get(themeId) || null;
  }

  /**
   * Create custom theme from current theme
   */
  createCustomTheme(name, overrides) {
    const current = this.getCurrentTheme();
    if (!current) {
      throw new Error('No current theme to base custom theme on');
    }

    const customId = `custom-${Date.now()}`;
    const customTheme = {
      ...current,
      id: customId,
      name,
      ...overrides,
    };

    this.registerTheme(customTheme);
    return customTheme;
  }

  /**
   * Export theme as JSON
   */
  exportTheme(themeId) {
    const theme = this.themes.get(themeId);
    if (!theme) {
      return null;
    }

    return JSON.stringify(theme, null, 2);
  }

  /**
   * Import theme from JSON
   */
  importTheme(jsonString) {
    try {
      const themeData = JSON.parse(jsonString);
      return this.registerTheme(themeData);
    } catch (error) {
      throw new Error(`Failed to import theme: ${error.message}`);
    }
  }

  /**
   * Save theme preference
   */
  _saveThemePreference(themeId) {
    try {
      localStorage.setItem('selected_theme', themeId);
    } catch (error) {
      console.warn('Failed to save theme preference:', error);
    }
  }

  /**
   * Load saved theme preference
   */
  loadSavedTheme() {
    try {
      const saved = localStorage.getItem('selected_theme');
      if (saved && this.themes.has(saved)) {
        this.currentTheme = saved;
      }
    } catch (error) {
      console.warn('Failed to load theme preference:', error);
    }
  }

  /**
   * Event listener management
   */
  on(event, callback) {
    this.listeners.add({ event, callback });
  }

  off(event, callback) {
    this.listeners.forEach(listener => {
      if (listener.event === event && listener.callback === callback) {
        this.listeners.delete(listener);
      }
    });
  }

  emit(event, ...args) {
    this.listeners.forEach(listener => {
      if (listener.event === event) {
        listener.callback(...args);
      }
    });
  }
}

// Singleton instance
const themeEngine = new ThemeEngine();

// Register default themes
themeEngine.registerTheme({
  id: 'light',
  name: 'Light',
  colors: {
    burgundy: {
      primary: '#5a1520',
      dark: '#3d0e15',
      darker: '#2a0a0f',
      light: '#6b1d2a',
      accent: '#7a2230',
    },
    cream: {
      light: '#fffef0',
      primary: '#fefae8',
      medium: '#faf5d8',
      dark: '#f5ecc8',
      darker: '#ede2b8',
      border: '#ddd4a8',
    },
    text: {
      primary: '#2a0a0f',
      secondary: '#5a4a3a',
      light: '#fffef0',
      on_burgundy: '#fffef0',
      on_cream: '#2a0a0f',
    },
    backgrounds: {
      main: '#fffef0',
      card: '#fefae8',
      hover: '#faf5d8',
      active: '#f5ecc8',
      code: '#3d0e15',
      code_text: '#fffef0',
    },
    borders: {
      primary: '#5a1520',
      secondary: '#ddd4a8',
      subtle: '#ede2b8',
    },
    shadows: {
      light: 'rgba(90, 21, 32, 0.1)',
      medium: 'rgba(90, 21, 32, 0.2)',
      dark: 'rgba(61, 14, 21, 0.3)',
    },
  },
  spacing: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
    xxl: 48,
  },
  typography: {
    fontFamily: {
      primary: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
      heading: "'Dancing Script', cursive",
      mono: "'Fira Code', 'Courier New', monospace",
    },
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      md: '1rem',
      lg: '1.25rem',
      xl: '1.5rem',
      xxl: '2rem',
    },
    fontWeight: {
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
  },
  shadows: {
    sm: '0 1px 2px rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px rgba(0, 0, 0, 0.1)',
    xl: '0 20px 25px rgba(0, 0, 0, 0.15)',
  },
  borderRadius: {
    sm: 4,
    md: 8,
    lg: 12,
    xl: 16,
    full: 9999,
  },
  animations: {
    duration: {
      fast: '150ms',
      normal: '200ms',
      slow: '300ms',
    },
    easing: {
      default: 'cubic-bezier(0.4, 0, 0.2, 1)',
      easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
      easeOut: 'cubic-bezier(0, 0, 0.2, 1)',
    },
  },
});

themeEngine.registerTheme({
  id: 'dark',
  name: 'Dark',
  colors: {
    burgundy: {
      primary: '#7a2230',
      dark: '#5a1520',
      darker: '#3d0e15',
      light: '#8b2d3a',
      accent: '#9a3440',
    },
    cream: {
      light: '#2a2520',
      primary: '#3a3528',
      medium: '#4a4538',
      dark: '#5a5548',
      darker: '#6a6558',
      border: '#7a7568',
    },
    text: {
      primary: '#fffef0',
      secondary: '#ddd4a8',
      light: '#fffef0',
      on_burgundy: '#fffef0',
      on_cream: '#2a0a0f',
    },
    backgrounds: {
      main: '#1a1510',
      card: '#2a2520',
      hover: '#3a3528',
      active: '#4a4538',
      code: '#0a0500',
      code_text: '#fffef0',
    },
    borders: {
      primary: '#7a2230',
      secondary: '#5a5548',
      subtle: '#4a4538',
    },
    shadows: {
      light: 'rgba(0, 0, 0, 0.3)',
      medium: 'rgba(0, 0, 0, 0.5)',
      dark: 'rgba(0, 0, 0, 0.7)',
    },
  },
  spacing: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
    xxl: 48,
  },
  typography: {
    fontFamily: {
      primary: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
      heading: "'Dancing Script', cursive",
      mono: "'Fira Code', 'Courier New', monospace",
    },
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      md: '1rem',
      lg: '1.25rem',
      xl: '1.5rem',
      xxl: '2rem',
    },
    fontWeight: {
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
  },
  shadows: {
    sm: '0 1px 2px rgba(0, 0, 0, 0.3)',
    md: '0 4px 6px rgba(0, 0, 0, 0.5)',
    lg: '0 10px 15px rgba(0, 0, 0, 0.5)',
    xl: '0 20px 25px rgba(0, 0, 0, 0.7)',
  },
  borderRadius: {
    sm: 4,
    md: 8,
    lg: 12,
    xl: 16,
    full: 9999,
  },
  animations: {
    duration: {
      fast: '150ms',
      normal: '200ms',
      slow: '300ms',
    },
    easing: {
      default: 'cubic-bezier(0.4, 0, 0.2, 1)',
      easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
      easeOut: 'cubic-bezier(0, 0, 0.2, 1)',
    },
  },
});

// Apply saved theme on load
if (typeof window !== 'undefined') {
  themeEngine.loadSavedTheme();
  const savedTheme = themeEngine.getCurrentTheme();
  if (savedTheme) {
    themeEngine.applyTheme(savedTheme.id);
  } else {
    themeEngine.applyTheme('light');
  }
}

export default themeEngine;

