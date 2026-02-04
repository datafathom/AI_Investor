import { useEffect, useState } from 'react';
import useSymbolLinkStore from '../stores/symbolLinkStore';

/**
 * Hook to link a component to a symbol group
 * @param {string} initialGroup - 'red' | 'blue' | 'green' | 'none'
 * @param {Function} onSymbolChange - Callback when symbol changes in the group
 */
export const useSymbolLink = (initialGroup = 'none', onSymbolChange = null) => {
  const [group, setGroup] = useState(initialGroup);
  const { links, updateSymbol } = useSymbolLinkStore();
  
  const currentSymbol = group !== 'none' ? links[group] : null;

  useEffect(() => {
    if (onSymbolChange && currentSymbol) {
      onSymbolChange(currentSymbol);
    }
  }, [currentSymbol, onSymbolChange]);

  const setLinkGroup = (newGroup) => {
    setGroup(newGroup);
  };

  const changeSymbol = (symbol) => {
    if (group !== 'none') {
      updateSymbol(group, symbol);
    }
  };

  return {
    group,
    setLinkGroup,
    currentSymbol,
    changeSymbol
  };
};

export default useSymbolLink;
