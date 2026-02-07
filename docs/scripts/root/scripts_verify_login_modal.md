# Script: verify_login_modal.py

## Overview
`verify_login_modal.py` is an enhanced debugging tool for the authentication entry point.

## Core Functionality
- **Modal Interaction**: Specifically waits for the `auth-modal` to appear, enters credentials, and tracks the transition through the "Processing..." state to successful cleanup of the modal from the DOM.
- **Failure Diagnostics**: captures screenshots and full logs if the modal stalls or fails to submit, providing critical evidence for debugging "stuck on login" issues.

## Status
**Essential (Diagnostics)**: the primary tool for debugging authentication flow regressions.
