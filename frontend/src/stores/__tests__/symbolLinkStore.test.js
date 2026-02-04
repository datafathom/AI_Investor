
import useSymbolLinkStore from '../symbolLinkStore';

describe('symbolLinkStore', () => {
  beforeEach(() => {
    useSymbolLinkStore.setState({
      links: {
        'red': 'SPY',
        'blue': 'QQQ',
        'green': 'IWM'
      }
    });
  });

  it('updates group ticker', () => {
    const { updateSymbol } = useSymbolLinkStore.getState();
    updateSymbol('red', 'NVDA');
    
    const { links } = useSymbolLinkStore.getState();
    expect(links['red']).toBe('NVDA');
  });

  it('retrieves group ticker', () => {
    const { getSymbol } = useSymbolLinkStore.getState();
    expect(getSymbol('blue')).toBe('QQQ');
  });
});
