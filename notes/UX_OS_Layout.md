# UX OS Layout: The Gold Standard

This document defines the mandatory layout and scrolling patterns for the AI Investor platform. All future LLMs and developers must strictly adhere to these rules to prevent layout regressions (widget stacking, bottom-cutoff, and content-bleeding).

---

## 1. Page-Level Registry (CRITICAL)
Every OS-style page (Pages using `ResponsiveGridLayout`) MUST be registered in `frontend2/src/App.jsx`.

- **Registry Target**: `isOSStylePage` array.
- **Why**: Registering a route here applies the `.os-bleed` class to the `main` container.
- **Effect**: Locks the page height to `100vh - headers`, provides a clean flex context, and prevents global page scrolling in favor of internal component scrolling.

## 2. Page Hierarchy
A successful OS page follows this exact nested structure:

```jsx
<div className="options-analytics-page full-bleed-page">
    <header className="page-header-flex">...</header>
    
    <div className="scrollable-content-wrapper">
        <ResponsiveGridLayout 
            draggableHandle=".glass-panel-header"
            rowHeight={80}
            margin={[16, 16]}
            {...props}
        >
            {/* Widget Items */}
        </ResponsiveGridLayout>
        
        {/* Anti-Overlap Buffer */}
        <div className="scroll-buffer-200" /> 
    </div>
</div>
```

## 3. Widget Anatomy (The "Seal")
To prevent the **"Bleed-Stack Syndrome"** (where widgets hover above each other because content is spilling out), every widget MUST be sealed with an internal scroll context.

### Standard Widget Implementation:
```jsx
<div key="my-widget" className="widget-container">
    <div className="glass-panel glass-premium h-full flex flex-col">
        
        {/* 1. Standardized Drag Handle */}
        <div className="glass-panel-header p-3 border-b border-white/10 flex justify-between cursor-move">
            <h3 className="text-xs font-bold uppercase">Widget Title</h3>
        </div>

        {/* 2. Mandatory Internal Scroll Wrapper */}
        <div className="flex-1 p-6 overflow-y-auto">
            <MyInternalComponent hideHeader={true} />
        </div>

    </div>
</div>
```

### Critical Rules for Widgets:
1.  **Headless Mode**: Internal widgets (e.g., `KafkaStreamMonitor`) must support a `hideHeader` prop. The Dashboard provides the dragging header; the component provides the data.
2.  **No Hidden Overflows**: NEVER use `overflow: hidden` on the primary content container if the data is dynamic. Always use `overflow-y-auto`.
3.  **Flex-Base**: The `.flex-col` + `.flex-1` pattern ensures the content area takes up all remaining space inside the widget's defined height.

## 4. CSS Failsafes (index.css)
The following global rules are enforced in `index.css` to prevent browser-level layout collapse:

- **`.react-grid-item`**: Standardized with `position: absolute !important`. This prevents items from stacking in block flow if the layout engine is delayed.
- **`.flex`, `.flex-col`, `.overflow-y-auto`**: Standard utility classes are defined with `!important` to ensure they override any local component legacy styles.

## 5. Troubleshooting Layouts
If widgets are overlapping or "disappearing":
1.  **Reset LocalStorage**: Increment the `STORAGE_KEY` (e.g., `layout_v3` -> `layout_v4`) in the JSX file.
2.  **Check Registration**: Confirm the route is in the `App.jsx` registry.
3.  **Check Row Height**: Modern widgets require `rowHeight={80}` for sufficient vertical density.

---
**Standard REFERENCE PAGE**: `frontend2/src/pages/DebateRoom.jsx` or `OptionsStrategyDashboard.jsx`.
