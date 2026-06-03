# Spacesuit 3D Asset

## Overview

Create a Godot 4 compatible, animation-ready EVA spacesuit as a modular character asset. The suit should read clearly at gameplay distance while still holding up in close inspection: bulky pressurized fabric, rigid life-support hardware, a reflective helmet visor, sealed joints, gloves, boots, and mission-worn surface detail.

The target style is realistic hard science fiction, based on modern extravehicular suits rather than a slim fabric costume. The silhouette should feel heavy, pressurized, and engineered for vacuum survival.

## Asset Goals

- Engine: Godot 4.x
- Primary scene: `Spacesuit3D.tscn`
- Root node: `CharacterBody3D` or `Node3D`, depending on whether the asset is playable or display-only
- Export format: GLTF/GLB preferred for DCC handoff
- Scale: approximately 1.9 m tall including helmet and boots
- Use case: third-person astronaut, first-person inspection target, or static hangar prop
- Rendering target: Forward+ with PBR materials

## Silhouette

The model should have a strong, readable shape:

- Oversized helmet dome with dark gold visor
- Broad hard upper torso shell
- Large rectangular life-support backpack
- Thick cylindrical arms and legs with ribbed joint segments
- Heavy gloves with reinforced fingertips
- Wide boots with flat soles and ankle rings
- Utility connectors, hose loops, and latch details around the torso

The body proportions should not look like normal clothing. The suit volume should be inflated and rigid, especially around the arms, thighs, knees, and elbows.

## Model Structure

Recommended node layout:

```text
Spacesuit3D
|-- Skeleton3D
|-- BodySuit_Mesh
|-- HardTorso_Mesh
|-- HelmetRing_Mesh
|-- HelmetGlass_Mesh
|-- Visor_Mesh
|-- Backpack_Mesh
|-- ChestControl_Mesh
|-- Hose_Left_Mesh
|-- Hose_Right_Mesh
|-- Glove_L_Mesh
|-- Glove_R_Mesh
|-- Boot_L_Mesh
|-- Boot_R_Mesh
|-- Attachments
|   |-- Light_Left
|   |-- Light_Right
|   |-- TetherHook
|   `-- ToolMount
`-- CollisionShape3D
```

Keep the soft suit, rigid torso, helmet, visor, backpack, gloves, and boots as separate meshes. This makes rigging, material assignment, LOD creation, and gameplay attachment points easier.

## Major Components

### Helmet

The helmet is a clear pressure bubble seated into a rigid neck ring. Add a dark metallic-gold visor over the front with high roughness variation so it catches strong highlights without becoming a perfect mirror.

Details to include:

- Thick lower helmet collar
- Side hinge pivots
- Front visor frame
- Small camera or lamp mounts
- Interior shadowed head cavity

### Torso

The upper torso should be a rigid shell, not deforming cloth. It should connect the helmet ring, arm bearings, lower torso ring, chest control unit, and backpack.

Details to include:

- Rounded chest plate
- Shoulder bearing rings
- Waist connection ring
- Latches and fasteners
- Rectangular chest control panel with colored buttons
- Oxygen and comms ports

### Backpack

The life-support backpack should be large enough to dominate the rear view. Give it layered paneling rather than a plain box.

Details to include:

- Main rectangular housing
- Raised service panels
- Vents or radiator slits
- Circular access caps
- Small warning labels
- Side tanks or canisters
- Rear emergency handle

### Arms And Legs

The limbs should be pressurized fabric tubes with rigid joint controls. Use broad folds, ribbing, and restraint bands rather than soft drapery.

Details to include:

- Ribbed elbows and knees
- Reinforced fabric bands
- Subtle seam lines
- Wrist and ankle locking rings
- Thick forearms and calves
- Slight asymmetry in wrinkle placement

### Gloves

The gloves should look functional and bulky, with enough finger separation for animation readability.

Details to include:

- Dark gray palm pads
- White armored back plates
- Reinforced fingertips
- Wrist locking cuffs
- Small fabric wrinkles at knuckles

### Boots

The boots should be wide, stable, and heavy.

Details to include:

- Flat treaded soles
- Reinforced toe caps
- Ankle rings
- Side fasteners
- Scuffed contact edges

## Materials

Use Godot `StandardMaterial3D` or imported PBR materials.

### White Suit Fabric

- Albedo: warm off-white, not pure white
- Roughness: high
- Metallic: 0
- Normal map: woven fabric, broad folds, seam stitching
- Ambient occlusion: strong in folds and between hardware pieces

Suggested values:

- Base color: `#d8d5c8`
- Roughness: `0.85`
- Specular: `0.35`

### Hard Torso And Rings

- Albedo: slightly cleaner white or light gray
- Roughness: medium-high
- Metallic: low or 0
- Add edge wear around latches and rings

Suggested values:

- Base color: `#e6e1d5`
- Roughness: `0.55`
- Specular: `0.45`

### Visor

- Albedo: dark amber-gold
- Metallic: high
- Roughness: low-medium
- Transparency: optional, depending on gameplay need

Suggested values:

- Base color: `#9b6a24`
- Metallic: `0.8`
- Roughness: `0.18`

### Backpack

- Albedo: light gray panels with darker vents
- Roughness: medium
- Add grime around panel seams

Suggested values:

- Base color: `#c8c9c4`
- Roughness: `0.65`

### Dark Rubber

Use for palms, soles, hose segments, and flexible joint seals.

Suggested values:

- Base color: `#17191a`
- Roughness: `0.75`
- Metallic: `0`

## Texture Set

Recommended texture maps:

- `spacesuit_albedo.png`
- `spacesuit_normal.png`
- `spacesuit_orm.png`
- `spacesuit_emission.png` for small panel lights
- `visor_albedo.png`
- `visor_normal.png`
- `visor_orm.png`

Pack occlusion, roughness, and metallic into an ORM map for Godot:

- Red: ambient occlusion
- Green: roughness
- Blue: metallic

## Rigging

The rig should preserve the suit's rigid-and-soft construction.

Suggested bones:

- Root
- Pelvis
- Spine
- Chest
- Neck
- Head
- UpperArm.L / LowerArm.L / Hand.L
- UpperArm.R / LowerArm.R / Hand.R
- Thigh.L / Shin.L / Foot.L
- Thigh.R / Shin.R / Foot.R
- Backpack
- ChestControl
- Helmet

Rigid pieces such as the helmet, torso shell, backpack, chest panel, rings, and boots should be weighted almost entirely to their nearest bone. Fabric limbs can use smoother weighting but should retain volume at elbows and knees.

## Collision

Use simple collision rather than mesh collision.

Recommended setup:

- One capsule for the full character body
- Optional small shapes for backpack and helmet if gameplay needs precise interaction
- Avoid per-finger or per-hose collision unless required

## Animation Notes

Movement should feel constrained:

- Shorter walking stride than an unsuited character
- Limited shoulder lift
- Slower arm swing
- Slight torso stiffness
- Heavy boot placement
- Gloves held slightly open and curved

Useful animation set:

- Idle
- Walk
- Slow turn
- Tool reach
- Inspect wrist
- Grab handle
- Helmet light toggle

## Godot Scene Setup

Recommended lighting for inspection:

- `WorldEnvironment` with ACES tonemapping
- One strong directional key light
- Weak fill light from the opposite side
- Reflection probe or sky reflection for visor highlights

Suggested scene nodes:

```text
SpacesuitPreview
|-- WorldEnvironment
|-- DirectionalLight3D
|-- OmniLight3D
|-- Camera3D
`-- Spacesuit3D
```

Camera framing:

- Position: `(0, 1.45, 4.0)`
- Look at: `(0, 1.15, 0)`
- FOV: `45`

## Quality Checklist

- The model reads as a spacesuit from front, side, and rear.
- Helmet, backpack, gloves, and boots are recognizable at small size.
- The torso shell and backpack do not deform during animation.
- Fabric folds follow pressurized suit logic, not loose clothing logic.
- Visor catches bright highlights without hiding its shape.
- White fabric keeps visible detail under strong lighting.
- The asset is centered at the origin with feet on the ground plane.
- The final scene imports cleanly into Godot without missing textures.

## Prompt For Model Creation

Use this concise prompt when generating or directing the asset:

```text
A realistic modular EVA spacesuit for Godot 4, full body, bulky pressurized white fabric, rigid hard upper torso, large rectangular life-support backpack, gold reflective helmet visor, ribbed elbow and knee joints, wrist and ankle locking rings, reinforced gloves, heavy treaded boots, hoses, latches, chest control panel, subtle grime and fabric weave, game-ready PBR materials, centered at origin, animation-ready proportions.
```
