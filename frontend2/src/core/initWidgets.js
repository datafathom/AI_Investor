
import widgetRegistry from './WidgetRegistry';
import { lazy } from 'react';

// Lazy load widgets
// Lazy load widgets
const OptionsChainWidget = lazy(() => import('../widgets/OptionsChain/OptionsChainWidget.jsx'));
const DOMWidget = lazy(() => import('../widgets/DOM/DOMWidget.jsx'));

export const initWidgets = () => {
  widgetRegistry.register({
    id: 'options-chain-view',
    name: 'Options Chain',
    version: '1.0.0',
    description: 'Real-time options chain explorer with Greeks and volatility analysis',
    category: 'Analytics',
    icon: '📊',
    component: OptionsChainWidget,
    permissions: ['market_data']
  });

  widgetRegistry.register({
    id: 'market-depth-view',
    name: 'Level 2 Market Depth',
    version: '1.0.0',
    description: 'DOM (Depth of Market) visualization with bid/ask ladders',
    category: 'Market Data',
    icon: '📉',
    component: DOMWidget,
    permissions: ['market_data', 'l2_access']
  });

  console.log('[WidgetRegistry] Core widgets registered');
};
