# Godot MCP Study

## Question

Would exposing every public Godot API as MCP services help build better models and create better games?

## Short Answer

Not directly. Exposing every raw Godot public API would help less than a curated, typed Godot MCP service layer.

A full API mirror would be too large, version-fragile, hard to type safely, high-latency, and easy to misuse. The better approach is to expose high-level inspection, verification, preview, runtime probing, and asset-audit tools, with a limited raw-call escape hatch only for debugging.

For this project, MCP should support the existing workflow:

- Python is the application/model authoring source.
- Generated Object-Forth is an output, not a hand-edited source.
- The Object-Forth VM/transpiler should stay generic.
- Application-specific logic should not move into MCP, GDScript, the VM, or the transpiler.

## Why A Full Godot API Mirror Is Not Ideal

Godot has a large API surface. Mirroring every public class, method, property, signal, and enum through MCP creates several problems:

- Too many tools to search and choose from.
- Weak semantic guidance about which API sequence is correct.
- Extra latency for multi-step scene edits.
- Object lifetime issues when nodes are freed or scenes reload.
- Version drift whenever Godot changes public APIs.
- Hard-to-debug side effects from generic setters and raw method calls.
- Higher risk of accidentally creating app-specific runtime behavior outside the Python source.
- Poor fit for visual tasks where the real need is inspection, screenshots, and verification.

Raw Godot access is still useful, but it should be an escape hatch, not the main interface.

## What Would Actually Help

The most useful Godot MCP services are high-level, typed, and task-oriented.

### Scene Inspection

Expose tools that answer what is actually in the running scene.

- List scene tree nodes by path, name, type, and visibility.
- Query a node transform in world and local coordinates.
- Query node bounds, mesh bounds, and global AABB.
- List materials assigned to a node or mesh.
- List cameras, lights, viewports, and active camera state.
- Find nodes by name pattern or resource path.

This would directly help catch problems like:

- Model placed on the wrong tab.
- Spaceship or marker existing on Moon/Earth canvas instead of Game canvas.
- Object invisible because parent is hidden.
- Wrong transform after grid recentering.

### Visual Capture And Comparison

Expose reliable render capture tools.

- Capture a viewport or SubViewport to a PNG.
- Capture front/side/top model previews from model-viewer.
- Capture the Game tab after a scripted setup.
- Compare two screenshots for brightness, blank frames, or major movement.
- Report average luminance, dark-area ratio, and non-background pixel bounds.

This would help avoid subjective or false claims about:

- Game canvas background color.
- Dark terrain lighting.
- Whether a model is visible.
- Whether grid chunks assemble correctly.
- Whether a marker aligns with a target.

### Runtime Probes

Expose tools that query spatial truth from Godot.

- Raycast from camera center.
- Raycast from screen coordinate.
- Project world position to screen coordinate.
- Unproject screen coordinate to a ground/surface point.
- Sample terrain height at world/local X/Z.
- Query camera frustum visibility for a node.
- Query whether an object is behind the camera.

This would directly improve:

- Player forward movement alignment.
- Object placement on terrain.
- Marker-to-object alignment.
- Camera eye-height validation.
- Avoiding views through the backside of terrain.

### Asset And Model Quality Audit

Expose tools for model/resource diagnostics.

- Count nodes, meshes, vertices, triangles, and material slots.
- Check normals, degenerate triangles, duplicate vertices, and bounds.
- Check texture paths and texture sizes.
- Identify transparent materials.
- Detect missing resources.
- Compute model footprint and height.
- Capture standardized model preview images.

This would improve model creation by catching:

- Overly rough meshes.
- Blank model-viewer results.
- Wrong model scale.
- Missing textures.
- Materials that look transparent by mistake.
- Too many nodes causing performance problems.

### Input And Gameplay Simulation

Expose controlled runtime interaction tools.

- Press/release keys.
- Mouse wheel zoom.
- Mouse drag with button selection.
- Right-click context menu invocation.
- Run the game for N frames or seconds.
- Record node transforms over time.
- Capture before/after screenshots.

This would help verify:

- Arrow keys control the player role, not the camera.
- Forward movement follows player yaw.
- Turning changes yaw without changing location.
- Grid boundary crossing recenters the 3x3 map.
- Cart and spacesuit walker update over time.

### Performance Inspection

Expose lightweight runtime performance data.

- FPS and frame time.
- Node count.
- Mesh count.
- Draw calls if available.
- Resource load time.
- Process callback frequency.
- Memory/resource counts.

This would help diagnose:

- Slow boundary crossing.
- Excess rock placement overhead.
- Too many tiny model parts.
- Expensive per-frame Object-Forth callbacks.
- Runtime stalls caused by resource loading.

## Recommended MCP Service Groups

### `godot_scene`

Scene tree and transform queries.

Suggested tools:

- `list_nodes(root_path, depth, filter)`
- `get_node(path)`
- `get_transform(path, space)`
- `get_bounds(path, recursive)`
- `find_nodes(pattern, type_filter)`
- `get_visibility(path)`

### `godot_viewport`

Capture, camera, and screen-space tools.

Suggested tools:

- `capture_viewport(viewport_path, output_path)`
- `capture_active_window(output_path)`
- `get_active_camera(viewport_path)`
- `project_position(camera_path, node_or_position)`
- `raycast_screen(camera_path, x, y, collision_mask)`
- `brightness_report(image_path)`

### `godot_assets`

Resource and model diagnostics.

Suggested tools:

- `load_resource(path)`
- `inspect_scene_resource(path)`
- `inspect_mesh(path_or_node)`
- `inspect_materials(path_or_node)`
- `check_missing_resources(scene_path)`
- `standard_model_preview(scene_path, output_dir)`

### `godot_runtime`

Frame stepping and input simulation.

Suggested tools:

- `run_for_frames(count)`
- `run_for_seconds(seconds)`
- `send_key(key, pressed)`
- `send_mouse_button(button, pressed, x, y)`
- `send_mouse_motion(x, y, relative_x, relative_y)`
- `watch_transform(path, duration)`

### `godot_performance`

Runtime performance and resource counters.

Suggested tools:

- `get_fps()`
- `get_frame_time()`
- `get_node_count()`
- `get_resource_count()`
- `get_render_stats()`
- `profile_block(label, seconds)`

### `godot_raw`

Optional low-level escape hatch.

Suggested tools:

- `call_method(node_path, method, args)`
- `get_property(node_path, property)`
- `set_property(node_path, property, value)`

This group should be disabled by default or clearly marked as diagnostic-only.

## Guardrails For This Project

MCP should not become a new place for app-specific game logic.

Allowed:

- Inspect running Godot scene state.
- Capture visual evidence.
- Run deterministic gameplay checks.
- Validate generated models.
- Report performance.
- Trigger existing app actions.

Not allowed:

- Hand-author application behavior inside MCP.
- Bypass Python/Object-Forth source generation.
- Add moon-game-specific logic to the Object-Forth VM.
- Treat generated `.fth` files as source.
- Patch `.gd` app behavior directly unless it is a generated viewer/helper artifact owned by a Python generator.

## Best Architecture

Use a two-layer design.

Layer 1: typed high-level MCP tools.

- Stable, task-specific, safe.
- Easy for an AI agent to call correctly.
- Good for visual verification and debugging.

Layer 2: narrow raw Godot bridge.

- Used only when no typed tool exists.
- Requires explicit node paths and arguments.
- Should log every call.
- Should not be used for normal app implementation.

## Expected Benefits

A curated Godot MCP service layer would help most with:

- Reducing false visual claims.
- Finding why a model is invisible.
- Checking if a model is on the correct canvas.
- Verifying object placement on terrain.
- Validating player movement and camera alignment.
- Auditing model scale, mesh density, and material quality.
- Diagnosing performance regressions.
- Producing repeatable screenshot evidence.

For this project, the most valuable first tools are:

1. `capture_game_tab(output_path)`
2. `list_visible_game_nodes()`
3. `get_node_screen_position(node_path)`
4. `raycast_game_camera_center()`
5. `sample_game_terrain_height(x, z)`
6. `inspect_model_scene(scene_path)`
7. `capture_model_preview(scene_path, output_path)`
8. `run_input_sequence(sequence, capture_path)`
9. `get_runtime_performance_report()`

## Final Recommendation

Do not expose every public Godot API as MCP first.

Build a curated Godot MCP layer focused on inspection, capture, model audit, runtime probes, input simulation, and performance. Add a limited raw API bridge only as a fallback. This would help build better models and games while preserving the current Python/Object-Forth source-of-truth workflow.
