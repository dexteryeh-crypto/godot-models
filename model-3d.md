# Model 3D Specification: Procedural High-Fidelity Spacesuit

Date: 2026-06-06

This file is the local `model-3d.md` specification for the spacesuit rebuild requested in this workspace. It consolidates the available detailed source document `./spacesuit-3d.md` into concrete requirements for the generated Godot model.

## Required Asset

- Build `res://games/the-moon/Spacesuit3D.tscn` as a fresh procedural Godot 4 spacesuit model.
- The model must be generated from code, not from the removed legacy `spacesuit_*` material/resource pile.
- The first visible output must be the actual spacesuit model, not a placeholder, marketing page, or empty scene.

## Procedural Geometry

- Use Godot 4 `SurfaceTool` for procedural mesh construction.
- Extract mesh arrays with `commit_to_arrays()`.
- Create renderable geometry with `ArrayMesh.add_surface_from_arrays()`.
- Use indexed geometry through `Mesh.ARRAY_INDEX`.
- Generate and store normals, tangents, and UVs for each mesh surface.
- Avoid `SphereMesh.new()`, `CylinderMesh.new()`, `ImporterMesh`, and automatic `generate_lods` shortcuts.
- Use a normalized cube-sphere helmet bubble instead of a UV sphere.
- Generate custom closed limb, hose, boot, ring, torso, panel, PLSS, and HLOD meshes.
- Boots must have closed soles and visible tread/toe reinforcement.

## Rigging and Animation Readiness

- Include a `Skeleton3D` with root, torso, neck, head, backpack, upper-arm, forearm, hand, thigh, calf, and foot bones.
- Mesh arrays must include 4-weight skin blocks.
- Vertex weights must be normalized.
- Knees and elbows must include two-bone blended vertices, including midpoint transition vertices suitable for rotation.
- Include `BoneAttachment3D` mount points for backpack, torso ports, and neck/helmet attachment use.
- Generate hoses after at least one frame of deferred synchronization.
- Include an explicit human-activity composition layer with local anatomical pivots for torso, neck/head, shoulders, elbows, wrists/hands, hips, knees, ankles/feet, PLSS, and chest panel.
- Provide a runtime pose API capable of applying at least breathing, walk-preview, and reach-preview activity poses, with transforms propagating through the local hierarchy.

## Materials and Rendering

- Use PBR `StandardMaterial3D` materials for fabric, hard shell, rubber, metal, visor, transparent helmet glass, panel glass, labels, and status lenses.
- Fabric/hard shell materials must use local triplanar mapping with `uv1_triplanar = true` and `uv1_world_triplanar = false`.
- Fabric/hard shell materials must use a procedural `NoiseTexture2D` normal map generated at initialization.
- The visor must be gold/iridium-like: metallic, low roughness, and clearcoated.
- The helmet bubble must be transparent and clearcoated.
- Include a `ReflectionProbe` for visor and helmet reflections.

## EVA Suit Features

- Helmet bubble, visible head/face inside helmet, upper sun visor, helmet pivots, and visor latches.
- Neck bearing ring and accordion neck seals.
- Hard upper torso and soft pressure garment body.
- Embedded chest display/control panel with buttons and utility ports.
- Torso restraint bands and longitudinal limb seams.
- PLSS backpack attached to the body, with contact pad, radiator slats, access doors, service panel, bolts, warning labels, side quick-disconnects, regulator knobs, top handle, and bottom coupling.
- Oxygen and helmet vent hoses with collars.
- Shoulder rings, wrist rings, elbow bellows, knee bearing bellows, knee pivot discs, front bearing caps.
- Gloves with palm, fingers, and knuckle pads.
- Boots with closed uppers, sealed soles, tread blocks, ankle buckles, and toe reinforcement.

## Optimization and Verification

- Detailed meshes must use visibility ranges, margins, and fade modes.
- Generate HLOD far-proxy meshes for torso, helmet, arms, legs, and joint silhouette.
- Include a collision proxy for standing character bounds.
- Provide single front render `/home/dexter/steam/model.png`.
- Provide multi-view renders:
  - `/home/dexter/steam/model_front.png`
  - `/home/dexter/steam/model_back.png`
  - `/home/dexter/steam/model_left.png`
  - `/home/dexter/steam/model_right.png`
- Provide audit scripts for mesh arrays, runtime/spec coverage, and rig readiness.
- Provide an audit script that proves the human-activity rig moves hands, feet, and torso through the pose API.
- A successful model must pass all audits with zero failures.

## Current Verification Commands

```sh
/home/dexter/steam/games/godot/Godot_v4.6.3-stable_linux.x86_64 --headless --path /home/dexter/steam --script res://tools/audit_spacesuit_rebuild_mesh_arrays.gd
/home/dexter/steam/games/godot/Godot_v4.6.3-stable_linux.x86_64 --headless --path /home/dexter/steam --script res://tools/audit_spacesuit_rebuild_runtime.gd
/home/dexter/steam/games/godot/Godot_v4.6.3-stable_linux.x86_64 --headless --path /home/dexter/steam --script res://tools/audit_spacesuit_rebuild_spec.gd
/home/dexter/steam/games/godot/Godot_v4.6.3-stable_linux.x86_64 --headless --path /home/dexter/steam --script res://tools/audit_spacesuit_rebuild_rig_readiness.gd
/home/dexter/steam/games/godot/Godot_v4.6.3-stable_linux.x86_64 --headless --path /home/dexter/steam --script res://tools/audit_spacesuit_activity_rig.gd
```
