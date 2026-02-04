/**
 * useWindowManager Hook
 * 
 * React hook for interacting with the Window Manager service.
 * Provides window operations and state management.
 */

import { useState, useEffect, useCallback } from 'react';
import windowManager from '../services/windowManager';

export function useWindowManager() {
  const [windows, setWindows] = useState(() => windowManager.getAllWindows());
  const [windowStack, setWindowStack] = useState(() => [...windowManager.windowStack]);

  // Update state when windows change
  useEffect(() => {
    const updateWindows = () => {
      setWindows(windowManager.getAllWindows());
      setWindowStack([...windowManager.windowStack]);
    };

    // Listen to window events
    windowManager.on('window:registered', updateWindows);
    windowManager.on('window:unregistered', updateWindows);
    windowManager.on('window:updated', updateWindows);
    windowManager.on('window:broughtToFront', updateWindows);
    windowManager.on('window:minimized', updateWindows);
    windowManager.on('window:maximized', updateWindows);
    windowManager.on('window:restored', updateWindows);
    windowManager.on('layout:loaded', updateWindows);

    return () => {
      windowManager.off('window:registered', updateWindows);
      windowManager.off('window:unregistered', updateWindows);
      windowManager.off('window:updated', updateWindows);
      windowManager.off('window:broughtToFront', updateWindows);
      windowManager.off('window:minimized', updateWindows);
      windowManager.off('window:maximized', updateWindows);
      windowManager.off('window:restored', updateWindows);
      windowManager.off('layout:loaded', updateWindows);
    };
  }, []);

  const registerWindow = useCallback((windowData) => {
    return windowManager.registerWindow(windowData);
  }, []);

  const unregisterWindow = useCallback((windowId) => {
    return windowManager.unregisterWindow(windowId);
  }, []);

  const getWindow = useCallback((windowId) => {
    return windowManager.getWindow(windowId);
  }, []);

  const updateWindow = useCallback((windowId, updates) => {
    return windowManager.updateWindow(windowId, updates);
  }, []);

  const bringToFront = useCallback((windowId) => {
    return windowManager.bringToFront(windowId);
  }, []);

  const sendToBack = useCallback((windowId) => {
    return windowManager.sendToBack(windowId);
  }, []);

  const minimizeWindow = useCallback((windowId) => {
    return windowManager.minimizeWindow(windowId);
  }, []);

  const maximizeWindow = useCallback((windowId) => {
    return windowManager.maximizeWindow(windowId);
  }, []);

  const restoreWindow = useCallback((windowId) => {
    return windowManager.restoreWindow(windowId);
  }, []);

  const toggleLock = useCallback((windowId) => {
    return windowManager.toggleLock(windowId);
  }, []);

  const snapToZone = useCallback((windowId, zone) => {
    return windowManager.snapToZone(windowId, zone);
  }, []);

  const createGroup = useCallback((groupId, windowIds) => {
    return windowManager.createGroup(groupId, windowIds);
  }, []);

  const getGroupWindows = useCallback((groupId) => {
    return windowManager.getGroupWindows(groupId);
  }, []);

  const saveLayout = useCallback((layoutName) => {
    return windowManager.saveLayout(layoutName);
  }, []);

  const loadLayout = useCallback((layoutName) => {
    return windowManager.loadLayout(layoutName);
  }, []);

  const getSavedLayouts = useCallback(() => {
    return windowManager.getSavedLayouts();
  }, []);

  const deleteLayout = useCallback((layoutName) => {
    return windowManager.deleteLayout(layoutName);
  }, []);

  return {
    windows,
    windowStack,
    registerWindow,
    unregisterWindow,
    getWindow,
    updateWindow,
    bringToFront,
    sendToBack,
    minimizeWindow,
    maximizeWindow,
    restoreWindow,
    toggleLock,
    snapToZone,
    createGroup,
    getGroupWindows,
    saveLayout,
    loadLayout,
    getSavedLayouts,
    deleteLayout,
  };
}

