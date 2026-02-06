# PHASE 8 IMPLEMENTATION PLAN: THE GLOBAL HQ (GROWTH & ADMIN)
## FOCUS: VENTURE HUNTING, DEFENSE, RELATIONS, AND TOTAL ADMIN AUTOMATION

---

## 1. PROJECT OVERVIEW: PHASE 8
Phase 8 is the final stage of "Sovereignty." It focuses on external growth through the **Hunter (Dept 10)** and the final administrative polish of the **Envoy, Talent, and Front Office (Depts 12-14)**. This is the stage where the system handles all "Noise" and lets the CEO focus purely on high-level growth. It is the "Conglomerate Management" stage.

---

## 2. GOALS & ACCEPTANCE CRITERIA
- **G1**: Automated Venture deal ingestion and Cap-Table modeling (Hunter).
- **G2**: "Travel-Mode" security geofencing (Sentry) between mobile and laptop.
- **G3**: Total Inbox management with a target of "Zero Noise" (Front Office).
- **G4**: Personalized "Talent" reviews for the human CEO to prevent burnout.

---

## 3. FULL STACK SPECIFICATIONS

### 3.1 FRONTEND (The Global HQ)
- **Description**: Implementation of the Command Center with D3 Orbital layouts showing the entire 84-agent workforce.
- **Acceptance Criteria**:
    - **C1: Orbital Navigation**: Smoooth zooming from "Conglomerate Overview" down to a specific "Agent Log" in < 500ms.
    - **C2: Redacted Portal**: Sub-portal for external partners displays 0% PII while allowing secure document upload/download.
    - **C3: Focus Indicator**: HUD shows the CEO's current "Focus Score" based on calendar events and inbox noise levels.

### 3.2 BACKEND (Growth & Admin Automation)
- **Description**: The Cap-Table modeler, Inbox classifier, and geofencing middleware.
- **Acceptance Criteria**:
    - **C1: Waterfall Logic**: Cap-table math handles up to 5 rounds of dilution and preference overrides with 100% mathematical accuracy.
    - **C2: Inbox Classifier**: Accuracy of 95% on "Promo" vs "Actionable Invoice" classification using local LLM (Phi-3 or similar).
    - **C3: Geofence Interlock**: System lock triggers in < 15s if the distance between laptop and mobile coordinates > 500m.

### 3.3 INFRASTRUCTURE (Privacy & Relations)
- **Description**: Managing the external partner portal and the travel-mode GPS bridge.
- **Acceptance Criteria**:
    - **C1: Network Tunneling**: Geofence data is sent via an encrypted P2P tunnel between devices, avoiding central server storage of location data.
    - **C2: Partner Isolation**: Partner portals are served via a "Public-Face" container that has no direct RW access to the core `bunker_net`.
    - **C3: LLM Hosting**: Dedicated GPU container for local inference (Admin classification) to ensure PII never leaves the host machine.

### 3.4 TESTING & VERIFICATION
- **Description**: End-to-end "Life Management" testing and security geofencing Audit.
- **Acceptance Criteria**:
    - **T1: Deal Ingestion**: System parses 10 "Messy" pitch-decks and identifies "Max Dilution" with 100% accuracy in the stress-test suite.
    - **T2: Geofence Stress**: Trigger a fake "Divergence" in the test suite; verify the Biometric lockout state persists until Re-Sync.
    - **T3: E2E HQ Flow**: User receives a "Venture Deal" email -> Gatekeeper promotes it -> Hunter summarizes it -> User signs off in < 5 minutes total.

---

## 4. AGENT CONTRACTS

##### 👤 AGENT 10.2: The Cap-Table Modeler
- **Acceptance Criteria**: Correctly calculates "Net Exit Value" after 30% dilution and 2x preference triggers across 3 venture rounds.

##### 👤 AGENT 11.3: THE "TRAVEL-MODE" GUARD
- **Acceptance Criteria**: Verified system-lock occurs within 30s of location divergence (>500m).

##### 👤 AGENT 14.1: The Inbox Gatekeeper
- **Acceptance Criteria**: Filters 100% of "Marketing" mail while promoting bills > $1k to the Orchestrator HUD.

---

## 5. MILESTONES & TIMELINE
- **Week 1**: Hunter Deal-Scraper + Cap-Table Waterfall engine.
- **Week 2**: Sentry Geofencing (GPS Bridge) + Travel-Mode Lockout logic.
- **Week 3**: Front Office Inbox Gatekeeper (LLM Classifer) + Twilio Voice Advocate.
- **Week 4**: Global HQ Command Center UI + Final Conglomerate Acceptance Test.

---
**END OF PHASE 8 IMPLEMENTATION PLAN**
