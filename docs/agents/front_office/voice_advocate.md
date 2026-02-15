# Voice Advocate (Agent 14.3)

## ID: `voice_advocate`

## Role & Objective
The 'Synthetic Agent'. Uses voice-AI (e.g., Vapi or Retell) to handle incoming customer service calls, appointment bookings, and routine institutional inquiries that require a phone-call interface.

## Logic & Algorithm
- **Speech-to-Intent**: Converts audio streams into structured system commands.
- **Dynamic Scripting**: Adjusts tone and detail level based on the counterparty (e.g., aggressive for a utility service dispute, professional for a bank teller).
- **Live Transfer**: Instantly escalates the call to the user if the IVR or human agent requires biometric or "Principal-only" verification.

## Inputs & Outputs
- **Inputs**:
  - `inbound_audio_stream` (Call): Real-time voice data.
- **Outputs**:
  - `call_summary_log` (str): Plain-text transcript and conclusion of the interaction.
  - `action_items` (List): Follow-up tasks resulting from the call.

## Acceptance Criteria
- Successfully navigate 90% of automated IVR (phone-menu) systems without user intervention.
- Maintain a latency of < 500ms between audio reception and synthetic response.
