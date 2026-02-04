/**
 * useTheme Hook
 * 
 * React hook for theme management and switching.
 */

import { useState, useEffect } from 'react';
import themeEngine from '../themes/ThemeEngine.js';

export function useTheme() {
  const [currentTheme, setCurrentTheme] = useState(() => themeEngine.getCurrentTheme());
  const [themes, setThemes] = useState(() => themeEngine.getAllThemes());

  useEffect(() => {
    const updateTheme = () => {
      setCurrentTheme(themeEngine.getCurrentTheme());
      setThemes(themeEngine.getAllThemes());
    };

    themeEngine.on('theme:applied', updateTheme);
    themeEngine.on('theme:registered', updateTheme);

    return () => {
      themeEngine.off('theme:applied', updateTheme);
      themeEngine.off('theme:registered', updateTheme);
    };
  }, []);

  const applyTheme = (themeId) => {
    themeEngine.applyTheme(themeId);
  };

  const registerTheme = (themeData) => {
    return themeEngine.registerTheme(themeData);
  };

  const createCustomTheme = (name, overrides) => {
    return themeEngine.createCustomTheme(name, overrides);
  };

  const exportTheme = (themeId) => {
    return themeEngine.exportTheme(themeId);
  };

  const importTheme = (jsonString) => {
    return themeEngine.importTheme(jsonString);
  };

  return {
    currentTheme,
    themes,
    applyTheme,
    registerTheme,
    createCustomTheme,
    exportTheme,
    importTheme,
  };
}

