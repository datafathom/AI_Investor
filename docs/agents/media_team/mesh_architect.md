# Mesh Architect (Agent 19.5)

## ID: `mesh_architect`

## Role & Objective
The '3D Modeler'. Handles the generation, optimization, and conversion of 3D meshes (GLB/OBJ) for use in the system's "3D Graph Visualizer" or virtual reality environments.

## Logic & Algorithm
- **Geometry Generation**: Converts nodal data (e.g., the 19-department hierarchy) into a spatial 3D structure.
- **LOD Optimization**: Manages "Level of Detail" to ensure 3D visualizations remain performant on low-end hardware.
- **Texture Mapping**: Applies dynamic "Heatmap" textures to meshes based on real-time activity levels.

## Inputs & Outputs
- **Inputs**:
  - `graph_topology` (JSON).
  - `activity_metrics` (Data).
- **Outputs**:
  - `spatial_asset` (GLB): Optimized 3D model for Three.js.

## Acceptance Criteria
- Optimize 3D meshes to < 5MB file size for web rendering.
- Correctly map 100% of "Activity Heat" to vertex colors.
