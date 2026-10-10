# Reconstructed Waveshare RPi Camera (G)

Open `Waveshare_Camera_G.FCStd` for editable native FreeCAD geometry, or import `Waveshare_Camera_G.step` into another CAD application. This is a **non-printable component reference**, reconstructed from the manufacturer's shared E/F/G/H DWG and provisional packaging dimensions. It is not a manufacturer-supplied 3D model.

Edit the `CameraGParameters` spreadsheet. Columns C and D distinguish specified drawing dimensions from proposed dimensions. The same reference is installed under ORION's `CameraTiltAssembly → CameraReference → CameraGReconstruction`; its own parameter sheet is independent of the standalone asset.

## Verified drawing geometry

- PCB outline: 25 × 24 mm.
- Four Ø2.2 mm holes: (2, 8.5), (23, 8.5), (2, 22), (23, 22) mm.
- Two Ø1.8 mm lens-mount holes: (3.5, 15.65), (21.5, 15.65) mm.
- Optical center: (12.5, 15.65) mm, measured from the PCB's lower-left corner.
- Shared central square footprint: 8.5 × 8.5 mm. It does not define the complete Type G fisheye housing.

The DWG's **18 mm dimension is the spacing between the two lens-mount holes**, not the Type G barrel diameter. `extracted_geometry.json` and `dwg_front_view.png` in the adjacent `camera_mechanical/` directory preserve the decoded source geometry.

## Provisional geometry

PCB thickness (1.6 mm), barrel diameter (18 mm), forward lens depth (14 mm), sensor height and rear connector/latch dimensions are estimates. Barrel diameter and depth retain the earlier ORION envelope; they were not measured from the photo or inferred from the DWG. Optical surface shape and focus mechanics are illustrative. The protective lens cap, ribbon cable and individual rear electronics are omitted.

The assembly includes a proposed rear FFC opening in the camera frame. Check the actual connector and cable bend before printing. Changing this reference does not automatically resize the frame opening or resolve the other frame fastener defects.

`provenance.json` records parameter values, status and source. `scripts/recreate_camera_g.py` records the construction process. The source DWG conversion used GNU LibreDWG 0.14; dimension and circle coordinates were checked directly after conversion. This source only contains a front view for the camera.
