# Script: deep_verify_app.py

## Overview
`deep_verify_app.py` is a sophisticated verification script for the high-fidelity "Strategy" dashboard. It uses low-level browser commands to ensure complex 3D rendering and real-time stability indicators are functioning correctly.

## Core Functionality
- **Early Injection (CDP)**: Uses the Chrome DevTools Protocol (CDP) to inject authentication bypass scripts `Page.addScriptToEvaluateOnNewDocument`. this ensures the mock session is active before the React application even begins its boot sequence.
- **Canvas Verification**: Specifically searches for `<canvas>` elements to verify that the Three.js or WebGL-based strategy visualizations are actively rendering.
- **Text Stability Check**: Parses the rendered DOM for the string "TESTING STABILITY" to confirm that internal health-monitoring components are active.
- **Modal Suppression**: Forcefully hides UI modals that might block visual verification of the main dashboard content.

## Usage
```bash
python scripts/deep_verify_app.py
```

## Status
**Essential (Visual Verification)**: Validates the most visually and technically complex area of the application. Failure of this script often indicates a WebGL context crash or a failure in the browser-side auth state.
