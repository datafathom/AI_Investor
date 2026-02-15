# Visual Aesthetics Agent (Agent 19.2)

## ID: `visual_aesthetics_agent`

## Role & Objective
The 'Art Director'. Generates and refines high-fidelity images, UI mockups, and visual branding assets for the system's external and internal interfaces.

## Logic & Algorithm
- **Prompt Engineering**: Converts high-level visual descriptions into optimized diffusion model prompts.
- **Style Consistency**: Ensures all generated assets adhere to the current "Institutional Design Tokens" (Dark mode, glassmorphism, accent colors).
- **Asset Upscaling**: Manages the resolution and file-type conversion for different deployment targets (Web, Mobile, Print).

## Inputs & Outputs
- **Inputs**:
  - `image_request` (Text): "Generate a professional banner for the Banker department."
- **Outputs**:
  - `visual_asset` (URI): Path to the generated and optimized image.

## Acceptance Criteria
- Generate a preview mockup in < 20 seconds.
- 100% adherence to the defined color palette (HEX/HSL).
