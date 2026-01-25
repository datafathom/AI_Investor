
import useSymbolLinkStore from '../symbolLinkStore';

describe('symbolLinkStore', () => {
  beforeEach(() => {
    useSymbolLinkStore.setState({
      groups: {
        'red': { symbol: 'SPY' },
        'blue': { symbol: 'QQQ' },
        'green': { symbol: 'IWM' }
      }
    });
  });

  it('updates group ticker', () => {
    const { setGroupTicker } = useSymbolLinkStore.getState();
    setGroupTicker('red', 'NVDA');
    
    const { groups } = useSymbolLinkStore.getState();
    expect(groups['red'].symbol).toBe('NVDA');
  });

  it('retrieves group ticker', () => {
    const { getGroupTicker } = useSymbolLinkStore.getState();
    expect(getGroupTicker('blue')).toBe('QQQ');
  });
});
