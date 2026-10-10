# ORION FreeCAD frame

See [SETUP.md](SETUP.md) for the brief printing and assembly guide.

Editable **fit prototype** built in the local FreeCAD 1.1.3 instance through FreeCAD MCP from `SPEC.md` revision 0.3. Open `ORION_frame.FCStd`; the saved assembly uses a 190 mm diagonal wheelbase.

**Screw assembly audit: FAIL.** The later audit of all 62 proposed screws found interference and blocked tool access that the original printed-part collision checks did not include. See `SCREW_AUDIT.md` and `screw_audit.json`. The current CAD and STL exports need fastening revisions before full-frame printing.

The model includes four replaceable linked arms, keyed center joints, four-hole Ø9 mm motor patterns, the official ESP32-P4 Nano STEP reference, a removable Nano holder, four top-mounted ESCs on center-integrated cable-tie fingers, a sliding battery cradle with two strap paths, an adjustable front camera frame, GPS/IMU supports, landing skids, component envelopes, finite cable-route guides and clearance objects.

**Manufacturing release is pending.** Geometry driven by unmeasured interfaces is explicitly Proposed; actual measurement aliases remain TBD. Prototype meshes are under `export/prototypes/`. No accepted production STLs are supplied at the spec's release paths.

## Parameters

Edit column B in the FreeCAD `Parameters` spreadsheet, then recompute. Each input has an alias, status and source. Keep unit suffixes such as `mm` or `deg`. For a negative length use a formula such as `=0 mm - 17 mm`; FreeCAD can otherwise store it as text.

- `wheelbase_mm`: 180, 190 or 200 mm. All four motor axes and arm lengths follow this input.
- `center_width_mm`: **70 mm**, revised from the specification's 55 mm layout seed to enclose both arm-joint screws and keyed seats. Center length remains 75 mm.
- `m2_clearance_mm`: 2.4 mm coupon candidate; calibrate on the actual printer.
- `motor_mount_plate_mm`: 4 mm prototype pad. With M2×6 and no washer this gives 2 mm arithmetic engagement; safe motor thread depth is still unknown.
- `holder_fit_clearance_mm`: specified layout allowance; holders also have their documented source dimensions in native Part features. Inspect those source dimensions when refining a holder.
- `battery_offset_x_mm`: planned adjustment from −5 to +5 mm. Straps, leads and connector access require actual fit verification.
- `camera_tilt_deg`: default −15° downward relative to +X, matching the requested forward lean. The revised mount was checked at −20°, −15°, 0°, 15° and 30° at each wheelbase. Pivot height is 20 mm. Top-entry pivot nut pockets and relocated uprights accommodate the trial M2×6 hardware; see `camera_mount_checks.json`. Actual lens, cable and hardware dimensions remain unverified.
- `layout_*` aliases: explicitly unmeasured packaging surrogates. They do not resolve the corresponding actual-hardware TBD aliases.

The primary center and arm sketches are fully constrained. Other manufactured shapes use editable native Part primitives, unions and cuts. No third-party workbench or Python proxy is required to open the model. Intermediate master shapes are hidden; assembly links remain visible. Showing `ArmSolid` also displays the unrotated master, which appears as an extra arm.

## References and clearance

The non-printable Type G camera reference is reconstructed from the official shared DWG. Its native FCStd, STEP and parameter provenance are in `references/camera_g_reconstructed/`. Board outline, mounting holes and optical center follow the drawing; full fisheye barrel, PCB thickness and rear connector depths remain proposed. A candidate rear FFC opening has been added to the camera frame. See that directory's README before using the reference for physical fit.

`OfficialNanoSTEP` is a non-printable compound derived from the [manufacturer STEP archive](https://files.waveshare.com/wiki/ESP32-P4-NANO/ESP32-P4-Nano.zip); its original archive, STEP, PDF and DXF are retained in `references/`. The imported assembly has 864 solids, consolidated to avoid thousands of nested tree objects. It is placed with the PCB underside at Z=8 mm and PCB top at Z=9.6 mm.

The Wi-Fi housing keepout is anchored to the antenna copper geometry in the official STEP, with 15 mm clearance around its CAD bounds. It is not an expansion of the entire board. The purchased board revision still needs verification. **Some proposed fastening locations are inside this zone.** Conductive fastener placement must be revised, or a tested nonconductive M2×6 interface selected, before release.

Propeller disks and inflated sweeps are reference objects. The sweep uses a Proposed 10 mm Z center and 4 mm sweep thickness, with 5 mm radial/vertical allowances. Actual installed sweep position, thickness and blade flex remain TBD. Nominal clearance checks cannot establish final blade clearance.

USB/debug/card access, battery connector travel and cable routes are Proposed reservations. Cable guides have finite diameter; they do not establish actual soldered lead exits or bend limits. The camera lens, IMU populated height and strap dimensions include surrogate envelopes, not manufacturer measurements. The former regulator/harness placeholder was removed on this branch. The optical guide does not represent a 160° horizontal or vertical cone.

## Checks and prototype exports

`cad_checks.json` records recompute, motor-axis coordinates, shape validity and collision results for 180/190/200 mm variants. `Checks` records release limitations inside FreeCAD. `export/prototypes/manifest.json` maps each prototype mesh to its editable source, quantity, bounds and mesh validation. Screenshots include assembly, underside, side, exploded, access and clearance views.

The model checks separate printed-part collisions, specified/proposed component envelopes, the detailed Nano STEP and provisional prop sweeps. The camera pivot was checked at 0°, 15° and 30° with zero axis error and no printed-part collisions. Battery positions at −5, 0 and +5 mm also clear the printed parts. The three Nano underside reliefs remove the detailed STEP overlap with 0.5 mm component allowance. The independent saved-file reopen/recompute passed; evidence is in `reopen_check.json`. Physical fit, fastener material/engagement, port travel, installed wiring, antenna performance, stiffness, print settings, actual mass and CG remain unverified. No wheelbase is manufacturing-approved yet.

## Fasteners and assembly

The candidate joint list in `fasteners.csv` uses M2×6 throughout. It totals **52 screws if all proposed joints are retained**, including four screws per motor and two per arm joint. Against 12 purchased M2×6 this is 40 additional screws. M2×4 stock is unallocated spare hardware. This is a provisional joint plan; final head, nut/insert, material and engagement choices can change holder joints and quantities.

Small 1.7 mm pilot holes in several mounts are proposed retention interfaces, not verified printed threads or insert specifications. Measure and revise them before manufacturing. The two small rectangular slots near each motor pad are cable-tie strain-relief paths.

1. Print the tolerance coupon and one arm; check holes, motor seating and safe M2×6 engagement on the purchased motor.
2. Fit the keyed arm roots to the center plate. Install four motor screws and two root screws per arm.
3. Insulate and tie the four top-mounted ESCs to the integrated center-plate fingers, two per side. Electrical disconnection or unsoldering may still be required during arm replacement.
4. Install landing skids, battery cradle and underside IMU/power supports. Fit the battery straps, connectors and adjustment range.
5. Install GPS and camera supports, then the Nano holder and board. Verify actual components, insulation, cable bends, ports/card removal and antenna clearance.
6. Validate clearance with installed props, and record physical fit, print settings, mass and balance before any manufacturing release.

The intended arm removal direction is from below through its two recessed joint screws. The screw audit shows the existing holder reliefs are insufficient for the inner joints, and inner ESC screw tool access is blocked with the arms installed. The assembly order above is therefore provisional and does not establish independent service access. Frame screws may remain captive only after actual nut-retention fit is established.

Printing orientations, supports, material, wall count and infill remain TBD. The prototype export script translates each part to a local nonnegative bounding box; this is an export coordinate convention, not an accepted slicer orientation.

## Source scripts

The native FCStd is authoritative. `scripts/build_orion.py` creates the initial native model after the official STEP import. `scripts/finalize_orion.py` records the subsequent attachment-interface changes. `scripts/check_orion.py` checks the live document; `scripts/export_orion.py` writes prototype meshes and screenshots. Build/finalization scripts are one-time construction transcripts and use the live builder namespace; do not rerun them over the completed document. Normal edits use native objects and the parameter sheet.

## Top ESC branch revision

On `feat/top-esc-retention`, the four separate ESC trays, their eight mounting screws and arm holes, and the proposed power package/tray with its two mounting holes are removed. Two ESCs sit at X=±13 mm, Y=+42.5 mm; the other pair sits at X=±13 mm, Y=−51 mm, beyond the modeled antenna keepout. Each 25 × 20 × 7 mm ESC has a proposed 0.5 mm insulating pad and two nylon ties through narrow fingers integrated into the center plate. No separate ESC holder STL is required.

`top_esc_checks.json` records nominal envelope clearance at 180/190/200 mm, including the Nano bounds, antenna keepout and prop sweeps. The 180 mm layout has limited prop margin; actual leads, heat-shrink, ties, blade flex and retention strength need physical checks. `scripts/revise_top_esc.py` records this revision after the camera revisions; historical build scripts alone produce the older layout. The power tray deletion does not eliminate the need for power distribution and a suitable regulator. Other frame fastener defects remain; prior overall collision/reopen reports describe earlier geometry.

Updated printable volume is approximately **49.20 cm³**, excluding the coupon: about **61.0 g at solid PLA density 1.24 g/cm³**, versus 72.1 g before this revision. That is approximately **11.1 g less printed plastic**, including the removed power tray and filled old holes; actual slicer/printed mass and tie/pad weight differ.
