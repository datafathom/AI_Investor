# Phase 4: Options & Market Depth

> **Phases 46, 46.2, 47** | Status: `[ ]` Not Started  
> Last Updated: 2026-01-18

---

## Overview

Advanced trading widgets for options chain analysis, Level 2 market depth, and multi-sense symbol linking for synchronized analysis across windows.

---

## 46: Institutional Options Chain Widget

### 46.1 Vertical Strike Ladder

**Files to Create/Modify:**
- `[NEW]` `frontend2/src/widgets/OptionsChain/OptionsChainWidget.jsx`
- `[NEW]` `frontend2/src/widgets/OptionsChain/StrikeLadder.jsx`
- `[NEW]` `frontend2/src/widgets/OptionsChain/OptionsChain.css`

**Acceptance Criteria:**
- [ ] Vertical strike price ladder with Bid/Ask columns
- [ ] Updates in <100ms via internal pricing engine
- [ ] Call options left, Put options right
- [ ] ATM strike highlighted with distinct border
- [ ] Scrollable with current price centered

**Jest Tests Required:**
- [ ] `OptionsChainWidget.test.jsx`: Renders ladder, updates on price change
- [ ] `StrikeLadder.test.jsx`: Strike highlighting, scroll behavior

---

### 46.2 D3.js Volatility Smile & Greeks

**Files to Create/Modify:**
- `[NEW]` `frontend2/src/widgets/OptionsChain/VolatilitySmile.jsx`
- `[NEW]` `frontend2/src/widgets/OptionsChain/GreeksDisplay.jsx`

**Acceptance Criteria:**
- [ ] D3.js visualization of IV across strikes (smile curve)
- [ ] Greeks per contract: Delta (Δ), Gamma (Γ), Theta (Θ), Vega
- [ ] Color-coded by magnitude: high values = intense color
- [ ] Hover shows exact values

**Jest Tests Required:**
- [ ] `VolatilitySmile.test.jsx`: SVG renders, data updates
- [ ] `GreeksDisplay.test.jsx`: All Greeks display correctly

---

### 46.3 One-Click Order Entry

**Acceptance Criteria:**
- [ ] Click price cell → Pre-Trade Risk Modal opens
- [ ] Contract parameters pre-filled: Strike, Expiry, Type, Quantity
- [ ] Keyboard shortcut: Enter to confirm, Esc to cancel

---

### 46.4 IV Rank & IV Percentile

**Acceptance Criteria:**
- [ ] IV Rank: Current IV vs 52-week range (0-100%)
- [ ] IV Percentile: % of days IV was lower than current
- [ ] Displayed as dual gauge at top of widget
- [ ] "Overpriced Insurance" alert when IV Rank > 80

**Jest Tests Required:**
- [ ] `OptionsChainWidget.test.jsx`: IV metrics display

---

## 46.2: Level 2 Market Depth (DOM)

### 46.2.1 Vertical Price Ladder

**Files to Create/Modify:**
- `[NEW]` `frontend2/src/widgets/DOM/DOMWidget.jsx`
- `[NEW]` `frontend2/src/widgets/DOM/PriceLadder.jsx`
- `[NEW]` `frontend2/src/widgets/DOM/DOM.css`

**Acceptance Criteria:**
- [ ] Vertical ladder with histogram-based volume visualization
- [ ] Bid depth (left) vs Ask depth (right)
- [ ] Last trade price centered and highlighted
- [ ] 20 price levels visible by default

**Jest Tests Required:**
- [ ] `DOMWidget.test.jsx`: Renders ladder, volume histograms
- [ ] `PriceLadder.test.jsx`: Price centering logic

---

### 46.2.2 "The Gap" Visualization

**Acceptance Criteria:**
- [ ] Display mathematical center of order book as "The Gap"
- [ ] Updates in <50ms
- [ ] Visual gap highlight between best bid and best ask
- [ ] Gap width indicator in basis points

---

### 46.2.3 Institutional Whale Filter

**Acceptance Criteria:**
- [ ] Highlight orders exceeding user-defined thresholds
- [ ] Volume/OI heuristics for "Whale" detection
- [ ] Whale icon (🐋) badge on large orders
- [ ] Filter toggle: Show only whales

**Jest Tests Required:**
- [ ] `DOMWidget.test.jsx`: Whale filter applies correctly

---

### 46.2.4 Drag-and-Drop Order Placement

**Acceptance Criteria:**
- [ ] Drag limit order to new price level
- [ ] Visual "ghost" order preview during drag
- [ ] Drop updates order in Zustand store
- [ ] Confirmation toast on successful move

---

## 47: Multi-Sense Symbol Linking

### 47.1 Color-Group Linking

**Files to Create/Modify:**
- `[NEW]` `frontend2/src/stores/symbolLinkStore.js`
- `[NEW]` `frontend2/src/hooks/useSymbolLink.js`
- `[NEW]` `frontend2/src/components/SymbolLinkBadge.jsx`

**Acceptance Criteria:**
- [ ] Three color groups: Red, Blue, Green
- [ ] Symbol change propagates to all linked windows in <50ms
- [ ] Zustand `useSymbolLinkStore` with `{ red: 'AAPL', blue: 'TSLA', green: null }`
- [ ] Each window subscribes to its assigned color group

**Jest Tests Required:**
- [ ] `symbolLinkStore.test.js`: Symbol propagation logic
- [ ] `useSymbolLink.test.js`: Hook subscription behavior

---

### 47.2 Visual Group Badges

**Files to Create/Modify:**
- `[MODIFY]` `frontend2/src/components/WindowManager/WindowHeader.jsx`

**Acceptance Criteria:**
- [ ] Color-coded circle badge in top-right of each window
- [ ] Click badge to change group assignment
- [ ] Dropdown: Red, Blue, Green, Unlinked (gray)

**Jest Tests Required:**
- [ ] `SymbolLinkBadge.test.jsx`: Color display, dropdown behavior

---

### 47.3 Global Hotkeys

**Files to Create/Modify:**
- `[NEW]` `frontend2/src/hooks/useGlobalHotkeys.js`

**Acceptance Criteria:**
- [ ] `Shift+B`: Buy current symbol
- [ ] `Shift+S`: Sell current symbol
- [ ] `ESC`: Global Cancel/Kill all pending orders
- [ ] Hotkeys work from any focused window

**Jest Tests Required:**
- [ ] `useGlobalHotkeys.test.js`: Key combinations trigger actions

---

### 47.4 Persistent Group Assignments

**Acceptance Criteria:**
- [ ] Group assignments persisted in localStorage
- [ ] Restored on browser session resume
- [ ] Workspace save includes link configurations

---

## Widget Registry Entries

```javascript
{
  id: 'options-chain',
  name: 'Options Chain',
  component: OptionsChainWidget,
  category: 'Trading',
  defaultSize: { width: 600, height: 500 }
},
{
  id: 'dom-ladder',
  name: 'Level 2 DOM',
  component: DOMWidget,
  category: 'Trading',
  defaultSize: { width: 350, height: 600 }
}
```

---

## Test Coverage Requirements

| Component | Unit Tests | Integration Tests |
|-----------|------------|-------------------|
| OptionsChainWidget | ✓ | ✓ |
| StrikeLadder | ✓ | - |
| VolatilitySmile | ✓ | - |
| GreeksDisplay | ✓ | - |
| DOMWidget | ✓ | ✓ |
| PriceLadder | ✓ | - |
| symbolLinkStore | ✓ | - |
| useSymbolLink | ✓ | - |
| useGlobalHotkeys | ✓ | - |
| SymbolLinkBadge | ✓ | - |

**Minimum Coverage Target:** 80%

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Initial specification |

