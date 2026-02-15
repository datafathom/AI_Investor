# Video Director (Agent 19.3)

## ID: `video_director`

## Role & Objective
The 'Showrunner'. Orchestrates the creation of video clips, animation sequences, and data visualizations for institutional presentations and social updates.

## Logic & Algorithm
- **Storyboard Generation**: Breaks down a video request into individual "Scenes" with specific visual and auditory requirements.
- **Asset Sequencing**: Coordinates with the Visual Aesthetics agent to generate backgrounds and overlays.
- **Timeline Assembly**: Uses FFmpeg or similar libraries to stitch assets into a coherent 10-60 second video clip.

## Inputs & Outputs
- **Inputs**:
  - `video_brief` (Text): "Create a 30-second wrap-up for the week's trading."
- **Outputs**:
  - `video_clip` (MP4): Fully rendered and encoded output.

## Acceptance Criteria
- Correctly sequence 100% of defined scenes from the brief.
- Output video in standard 1080p/60fps format.
