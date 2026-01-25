# Phase 01: Education Mode Engine
> **Phase ID**: 01
> **Status**: Completed
> **Date**: 2026-01-19

## Overview
Implement a system-wide "Education Mode" that provides interactive, route-specific tutorials. When enabled, this mode guides the user through the UI using a simulated "Ghost Cursor" and step-by-step tooltips, explaining the purpose and functionality of each page as they navigate.

## User Story
As a new user or investor, I want to toggle "Education Mode" so that when I visit a complex page like "Macro" or "Compliance", the system automatically demonstrates how to use it, highlighting key features with a cursor animation and explanations.

## Component Architecture

### 1. State Management (`educationStore.js`)
- **State**:
    - `isEducationMode`: boolean (Global toggle)
    - `activeTutorial`: string (ID of current tutorial)
    - `currentStep`: number
    - `isPlaying`: boolean (Pause/Play tutorial)
    - `completedTutorials`: array<string> (History)
- **Actions**: `toggleEducationMode`, `startTutorial(route)`, `nextStep`, `skipTutorial`.

### 2. The Core Engine (`EducationOverlay.jsx`)
- A global overlay rendered in `App.jsx` (Z-index: 9999).
- Listens to route changes (React Router `useLocation`).
- Looks up the route in `TutorialRegistry`.
- If match & Education Mode ON & not completed (optional), triggers the tutorial sequence.

### 3. Ghost Cursor (`GhostCursor.jsx`)
- An SVG pointer that animates using `framer-motion` or `react-spring`.
- Interpolates position from the current step's target element (using `document.querySelector`) to the next.
- simulating "click" animations.

### 4. Tutorial Registry (`tutorialContent.js`)
- A centralized dictionary mapping Routes -> Step definitions.
- **Structure**:
  ```json
  {
    "/strategist/estate": [
      {
        target: "#estate-deadman-switch",
        title: "Dead Man's Switch",
        content: "If you fail to check in for 30 days, this protocol triggers asset transfer.",
        action: "hover"
      },
      ...
    ]
  }
  ```

## Implementation Steps

### Files to Create
- [ ] `frontend2/src/stores/educationStore.js`
- [ ] `frontend2/src/components/Education/EducationOverlay.jsx`
- [ ] `frontend2/src/components/Education/GhostCursor.jsx`
- [ ] `frontend2/src/components/Education/Tooltip.jsx`
- [ ] `frontend2/src/data/tutorialContent.js`
- [ ] `frontend2/src/components/Education/EducationToggle.jsx`

### Files to Modify
- [ ] `frontend2/src/App.jsx`: Mount `<EducationOverlay />`
- [ ] `frontend2/src/components/MenuBar.jsx`: Add `<EducationToggle />`

## Acceptance Criteria
1. **Toggle Switch**: A dedicated button in the MenuBar toggles Education Mode on/off.
2. **Route Detection**: Navigating to a page (e.g., `/strategist/estate`) automatically loads the relevant tutorial configuration.
3. **Ghost Animation**: The cursor visually moves from its resting position to the first prioritized UI element.
4. **Step Progression**: The user can click "Next" on the tooltip, or the system auto-advances after a set duration.
5. **DOM Resilience**: If a target element is missing (e.g., loading state), the engine waits or skips gracefully without crashing.
6. **Persistence**: The toggle state persists across reloads (localStorage).

## Verification Plan

### Automated Tests
- **Jest/React Testing Library**:
    - Verify `educationStore` toggles state correctly.
    - Verify `EducationOverlay` renders when `isEducationMode` is true.
    - Test `TutorialRegistry` lookup logic.

### Manual Verification
1. Enable "Education Mode" in MenuBar.
2. Navigate to `/strategist/estate`.
3. observe the Ghost Cursor move to the "Heartbeat" widget.
4. Verify the tooltip text matches the `tutorialContent.js`.
5. Navigate to `/guardian/compliance`.
6. Verify the tutorial switches to the Compliance context.
