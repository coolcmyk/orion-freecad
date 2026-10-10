# ORION: print and assembly

**Current status:** fit prototype. Resolve the screw-tip, head/nut interference and blocked tool access in [SCREW_AUDIT.md](SCREW_AUDIT.md) before printing the complete frame. The sequence below applies after those fixes and renewed clearance checks.

## 1. Prepare

- Open `ORION_frame.FCStd` in FreeCAD; use the `Parameters` spreadsheet to select the wheelbase (default 190 mm).
- Measure the purchased components and screw heads/nuts. Record results in `measurements.csv`; finalize nut/insert interfaces in `fasteners.csv`. Existing 1.7 mm pilots are not verified threads or insert seats.
- Gather matching drivers, a nut tool, calipers, straps/cable ties and electrical insulation. The provisional BOM uses **62 M2×6 screws** (50 more than the 12 owned); M2×4 remain spares. Nut quantities/types depend on the corrected joints.
- Recompute and recheck the corrected model, including installed fasteners, tool paths and antenna clearance. Re-export the printable solids; existing `export/prototypes/` files contain the audited defects.

## 2. Print and fit-check

1. Import the separate STLs into the slicer in **millimeters at 100% scale**. Do not print the electronics, propeller disks or clearance objects.
2. Print `ORION_tolerance_coupon.stl` and one arm first. Start the arm flat; inspect layer direction, overhangs, pockets and support removal in the slicer. Export coordinates do not establish print orientation for the other parts.
3. Use the printer/filament's calibrated profile. Final material, layer height, walls, infill, temperatures and support settings are still TBD; record the tested settings rather than treating a generic preset as validated.
4. Remove supports and check the keyed joint, screw/nut fit and motor holes with actual hardware. A 4 mm motor pad gives 2 mm nominal M2×6 engagement without a washer; verify the motor's safe depth before tightening.
5. After fit and stiffness checks pass, print the remaining parts:

| STL (`ORION_` prefix) | Quantity |
|---|---:|
| `arm.stl` | 4 total |
| `esc_holder.stl` | 4 |
| `landing_skid.stl` | 2 |
| `center_base.stl`, `p4_holder.stl`, `battery_mount.stl` | 1 each |
| `gps_mount.stl`, `imu_mount.stl`, `power_mount.stl` | 1 each |
| `camera_mount.stl`, `camera_base_mount.stl` | 1 each |

## 3. Assemble

Keep the battery disconnected and propellers off during assembly.

1. **Arm modules:** attach each motor with four screws. Fit each ESC tray to its arm before joining the center if top access requires it. Strap the insulated ESC into the open tray; route motor leads through the two small cable-tie slots for strain relief.
2. **Frame:** seat the four keyed arm roots under the center plate. Fit their nuts and two screws per arm from below. Check seating and tighten without crushing the print.
3. **Supports:** attach the GPS support before the power tray, then the landing skids, battery cradle, IMU and power supports. Fit the GPS facing upward and the IMU in the orientation required by the firmware.
4. **Camera:** drop the pivot nuts into the rotating frame's top-entry hex pockets before fitting the PCB. Attach the PCB using its four board holes, fit the frame between the fixed ears, insert the two M2×6 pivot screws from the outside and attach the base. Default tilt is −15° (downward); sampled nominal range is −20° to +30°. Loosen both pivots to adjust, then retighten. Leave slack for the camera cable throughout its travel; actual hardware and cable fit still require checks.
5. **Nano:** preload and hold the board nuts inside the holder before it goes onto the center plate. Secure the Nano PCB, then mount the holder. Confirm arm fasteners remain serviceable and hardware/wiring stays outside the antenna keepout.
6. **Wiring and battery:** connect motor/ESC, power, camera and sensor wiring using verified component pinouts and a verified power/regulator plan. This mechanical guide does not define electrical pin assignments. Insulate joints, secure cables clear of moving parts and strap the battery into its cradle.

## 4. Final checks

Confirm every joint seats securely; ports/card access, camera motion and battery removal work; and cables cannot reach the blades. Check the actual installed propeller sweep with power disconnected. Remove props for initial powered checks; fit them only after motor direction and controls are verified. Record printed mass, balance, fit results and photos before accepting the assembly.
