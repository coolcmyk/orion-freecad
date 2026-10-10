# ORION Frame — FreeCAD Specification

**Revision:** 0.3 · **Date:** 2026-10-10  
**Status:** Researched design specification with manufacturer drawings/CAD and user-supplied dimensions; assembly-specific interfaces require fit verification before manufacturing release.  
**Scope:** Parametric airframe, electronics holders, sensor mounts, and assembly packaging.

## 1. Objective

Design an editable, FDM-printable true-X quadcopter frame for ORION in FreeCAD. The frame must fit the actual purchased motors and provide removable holders for the ESP32-P4 Nano and four individual ESCs. It must also accommodate the battery, camera, GPS, IMU, onboard Wi-Fi antenna clearance, power distribution, and wiring.

Use the existing ORION/Darkstar2 work as a geometric reference where useful. Create an ORION-owned model rather than uniformly scaling an upstream model. This specification defines mechanical requirements; it does not establish flight readiness or firmware compatibility.

**Priority order:** measured component fit → propeller clearance → structural continuity → serviceability → mass reduction → appearance.

## 2. Hardware baseline and source precedence

| Component | Working design baseline | Required mechanical treatment |
| --- | --- | --- |
| Frame | Four-motor true-X; 190 mm diagonal wheelbase | Adjustable through a single master parameter; evaluate 180 and 200 mm variants |
| Motors | Four MAMBA TOKA 1103 10000KV; body Ø14.8 × 9.8 mm; shaft Ø1.5 mm; four M2 threads on Ø9 mm bolt circle [S3] | Use the bolt-circle coordinate table; verify internal screw clearance; standard fastener M2×6 |
| Propellers | Gemfan 2512 three-blade; specified disk Ø63.76 mm; 1.5 mm bore; 4 mm hub thickness | Keep 65 mm conservative CAD disk; distinguish hub thickness from blade sweep thickness |
| Controller / recorder | ESP32-P4 Nano; 50 × 50 × 1.60 mm PCB; four Ø2.70 mm holes at 45.10 × 45.10 mm spacing [S1] | Import official STEP reference; include connector overhang, underside components, and service access |
| ESCs | Four BLHeli 12 A mini ESCs; supplied size 25 × 20 × 7 mm, 9 g each | One removable, ventilated holder per ESC; verify whether listed envelope includes insulation and soldered leads |
| Battery | BETAFPV LAVA 2S 450 mAh 75C LiHV; 63 × 15.5 × 13.5 mm; 26.1 g | Adjustable cradle; two strap paths; separate XT30/16AWG and JST-XH2.54 connector access |
| Camera | Waveshare Raspberry Pi Camera Type G, OV5647; 25 × 24 mm board; four Ø2.2 mm holes on 21 × 13.5 mm pattern [S4]; 160° diagonal view | Offset hole pattern per local coordinate table; measure actual fisheye lens protrusion and flex-cable envelope |
| GPS | FlyFishRC M10 Mini candidate matching supplied dimensions: total 16.2 × 12.3 × 4.9 mm including antenna [S5]; 2.4 g nominal | Confirm actual module identity; removable upper/rear clip or foam support; retain antenna sky view and cable access |
| IMU | GY-91 MPU9250/BMP280; board 14.3 × 20.5 mm; 2.54 mm pin pitch | Mount near origin; define axes; populated height, header exits and mounting interface remain unresolved |
| Command reception | Onboard Wi-Fi through Nano’s ESP32-C6-MINI-1 coprocessor [S2]; user confirms no external receiver | Include antenna keep-out in Nano layout; no separate receiver bracket, cable, or mass allocation |
| Power distribution | Actual PDB or four-way harness plus regulator | Isolated support, connector access, strain relief, and ventilation |
| Storage | Actual microSD arrangement | Card insertion/removal space accessible with the frame assembled |

### 2.1 Latest component data takes precedence

The user's 2026-10-10 specifications, Wi-Fi-only command reception, and M2×6 screw preference supersede conflicting entries in earlier project documents. Where ambiguous listing text conflicts with a dimensioned manufacturer drawing, use the drawing and verify that the purchased hardware revision matches. The current mechanical baseline uses MAMBA TOKA motors, P4 Nano, four separate ESCs, Waveshare Type G OV5647, M10 Mini-class GPS, and GY-91.

- Treat supplied product dimensions as **Specified**, not physically measured values. They are sufficient for initial CAD envelopes; use a fit prototype to establish final printed tolerances.
- Keep the ESP32-P4 Nano plus individual ESC architecture. Do not reuse the old Darwin mounting pattern or 85 × 56 mm P4 development-board envelope.
- OV5640 remains an optional camera variant; this revision's required bracket is for the supplied OV5647 Type G. The mechanical change does not establish electrical or firmware compatibility.
- No external receiver is fitted. Command reception shares the Nano’s onboard ESP32-C6 radio; power-distribution packaging and regulator dimensions remain unresolved.
- **M2×6 mm is the selected standard screw length** for motor, frame, and holder joints. Keep M2×4 stock as unused spares in this baseline. Final quantities, head type, nut/insert interface, and motor engagement require a joint-specific bill of materials. Do not shorten screws or change length without documenting a design change.
- Supplied electrical ratings are outside this mechanical spec; do not infer complete propulsion compatibility from package dimensions.

### 2.2 Supplied dimensions and purchased fasteners

| Item | Nominal input available for CAD | Remaining interface information |
| --- | --- | --- |
| Battery | 63 × 15.5 × 13.5 mm; 26.1 g; XT30 with 16AWG leads; JST-XH2.54 charge plug | Lead exits, plug bodies/removal travel, straps |
| ESC, each | 25 × 20 × 7 mm; 9 g | Solder/heat-shrink allowance and lead exit positions |
| Propeller, each | Ø63.76 mm; hub 4 mm thick; bore Ø1.5 mm; max blade width 9.5 mm; 0.8 g | Installed sweep Z envelope and flex allowance |
| Motor, each | Body Ø14.8 × 9.8 mm; shaft Ø1.5 mm with 5 mm projection; overall drawing height 14.8 mm; four M2 on Ø9 mm bolt circle; 4.8 g including wires [S3] | Underside protrusion, safe screw engagement, wire exit; verify drawing against actual motor |
| Camera | Board 25 × 24 mm; four Ø2.2 holes, 21 × 13.5 mm spacing, offset from board center [S4]; 160° diagonal view | Actual G fisheye lens/body height, flex exit/bend allowance |
| GPS | Manufacturer total 16.2 × 12.3 × 4.9 mm includes antenna; manual patch 11.7 × 11.7 mm [S5]; retain 12 × 12 mm conservative zone | Match physical module; solder and cable protrusions; retention interface |
| GY-91 | Board 14.3 × 20.5 mm; eight pins at 2.54 mm pitch | Populated/header height, axes, hole or clamp locations |
| P4 Nano | PCB 50 × 50 × 1.60 mm; four Ø2.70 holes; spacing 45.10 × 45.10 mm [S1]; STEP bounds derived below | Purchased board revision, attached cable/header envelopes and service travel |
| Fasteners | **Standard: M2×6 mm. Purchased: 12 × M2×6 and 12 × M2×4 (spares)** | Additional M2×6 quantity from final BOM; head/material, nuts/inserts, usable engagement |

The supplied nominal battery + four ESCs + four props subtotal is **65.3 g**. Adding four motors at the manufacturer’s 4.8 g each gives **84.5 g**. These subtotals exclude frame, Nano, camera, GPS/IMU, regulator, harness, straps, and fasteners; neither is all-up mass. Do not count a separate Wi-Fi receiver, since reception is part of the Nano assembly.

### 2.3 Nano drawing and official STEP interpretation

The attached older outline is 50 × 50 mm and labels 45.10 × 45.09 mm hole spacing. The current manufacturer archive [S1], containing `ESP32-P4-NANO-20260331.pdf`, its DXF, and `ESP32-P4-NANO.stp`, establishes **four Ø2.70 mm holes at 45.10 × 45.10 mm spacing** and **1.60 mm PCB thickness**. Use board-local coordinates `(±22.55, ±22.55)` mm relative to the PCB center. The 0.01 mm vertical difference from the supplied outline is a source/revision difference; verify the actual board. The `R2.00` outline callout is not a hole diameter.

Bounds calculated from the official STEP solids, in the model's original axes, are approximately **50.019 × 52.854 × 18.210 mm**. The PCB top is Z = 0, PCB underside Z = −1.60, highest component Z = +14.45, and lowest component Z = −3.76. Thus the model has **14.45 mm above the PCB top** and **2.16 mm below the PCB underside**. These are **Derived** CAD values, not physical measurements. Connector overhang makes the populated assembly larger than the 50 × 50 mm PCB.

Use the STEP model as a non-printable reference and a rounded **50.1 × 52.9 × 18.3 mm** global bounding box for early layout, before added fit/access clearance. A 51 × 51 mm open PCB cradle can still work if its walls avoid the protruding ports; a closed enclosure of that size cannot be assumed to fit. Cables, SD-card travel, headers, mounting screws, airflow and antenna clearance enlarge the required space beyond the STEP bounds.

### 2.4 Manufacturer mounting-coordinate records

**Motor [S3]:** Four M2 threads on a **Ø9 mm bolt circle**, not a 9 × 9 mm square. Relative to the motor axis, a cardinal orientation gives `(0,+4.5)`, `(+4.5,0)`, `(0,−4.5)`, `(−4.5,0)` mm. Rotating that pattern by 45° gives `(±3.182, ±3.182)` mm. Provide a placement angle so wires can face the arm; preserve the bolt-circle diameter when rotating. A square at `(±4.5, ±4.5)` would be incorrect.

**Camera [S4]:** In the shared E/F/G/H manufacturer DWG, use local U along the 25 mm edge and V along the 24 mm edge. Define `(0,0)` at the lower-left corner of the DWG plan view; +V points toward the edge nearest the upper hole row. Four board mounting holes are **Ø2.2 mm** at:

| Hole | U from left edge | V from bottom edge |
| --- | ---: | ---: |
| Upper left | 2 mm | 22 mm |
| Upper right | 23 mm | 22 mm |
| Lower left | 2 mm | 8.5 mm |
| Lower right | 23 mm | 8.5 mm |

This is a **21 × 13.5 mm** pattern whose center is at `(12.5,15.25)` mm, offset from the PCB center `(12.5,12)` mm. The optical center in the drawing is `(12.5,15.65)` mm. Two interior Ø1.8 mm lens-assembly holes are separate from the four board holes; do not substitute them for the mounting interface. The drawing is a shared plan view and does **not** establish the Type G fisheye lens's maximum diameter or protrusion. Verify orientation against the actual camera before placing its cable exit and lens envelope.

### 2.5 Wi-Fi-only command reception

The user's receiver function is handled by the Nano's onboard Wi-Fi. On this board Wi-Fi is supplied by **ESP32-C6-MINI-1**, connected to ESP32-P4 through SDIO [S2]. Include one populated Nano reference; no separate receiver Body, harness, antenna bracket, or component mass is required.

Espressif's end-product housing guidance recommends **at least 15 mm of clearance in all directions around the antenna** [S6]. Create a keep-out anchored to the actual C6 module antenna area, rather than expanding the whole Nano PCB. Avoid locating the battery, conductive fasteners/frame parts, other electronics, or bundled power wiring inside that zone; use an open nonconductive support around it. Existing components on the manufacturer's PCB are part of the supplied board, not components to relocate. Validate link range/throughput in the assembled orientation because material, cables and placement affect reception.

## 3. Coordinate system and frame size

Use millimeters and degrees throughout. Set the origin at the geometric center of the four motor axes, on the upper surface of the center baseplate.

- **+X:** forward / primary camera direction.
- **+Y:** left when looking forward.
- **+Z:** upward.
- Motor mounting faces share one nominal Z plane; the propeller sweep plane is a separate measured height.

Let `W` be the diagonal distance between opposite motor axes. For a true-X layout, let `a = W / (2 × sqrt(2))`.

| Mechanical location | X | Y |
| --- | ---: | ---: |
| Front-left | +a | +a |
| Front-right | +a | −a |
| Rear-left | −a | +a |
| Rear-right | −a | −a |

These are mechanical names, not firmware motor numbers. Record the eventual mixer mapping separately.

| Diagonal wheelbase W | Center → motor axis W/2 | Adjacent motor-axis spacing W/√2 | Each coordinate magnitude a |
| --- | ---: | ---: | ---: |
| 180 mm | 90 mm | 127.28 mm | 63.64 mm |
| **190 mm default** | **95 mm** | **134.35 mm** | **67.18 mm** |
| 200 mm | 100 mm | 141.42 mm | 70.71 mm |

Thus **10 cm from the center to each motor axis means a 200 mm diagonal wheelbase**. Arm solid length is shorter than this radius because the arm starts at a center joint. Wheelbase does not describe the overall printed outline or the propeller envelope.

At W = 190 mm and a 65 mm prop disk, the axis-aligned sweep footprint is approximately `W/√2 + 65 = 199.35 mm` in both X and Y. Including 5 mm radial clearance gives a 209.35 mm footprint. These are packaging bounds, not printer-bed dimensions.

## 4. Parameters and measurement records

Create an input Spreadsheet with internal object name `Parameters`. Give each numeric input a stable alias and explicit units. Use expressions such as `Parameters.wheelbase_mm` for dependent dimensions. Put derived values in the input sheet only when they depend solely on other inputs. Put geometry-derived measurements in a separate `Checks` object/sheet to avoid circular dependencies.

Use these statuses:

- **Baseline:** inherited working requirement, still subject to component verification.
- **Proposed:** modeling starting point; fit, print, and stiffness checks may change it.
- **Specified:** supplied product data or dimensioned drawing, with source/date; usable for initial CAD, pending fit verification.
- **Derived:** calculated from a specified drawing or manufacturer CAD; record method and source, pending actual-hardware verification.
- **Measured:** recorded from the actual hardware, with date and evidence.
- **TBD:** not available; do not substitute an assumed manufacturer dimension.

### 4.1 Initial geometric inputs

| Alias | Initial value | Status / interpretation |
| --- | ---: | --- |
| `wheelbase_mm` | 190 mm | Baseline; evaluate 180–200 mm |
| `prop_diameter_mm` | 65 mm | Conservative CAD envelope; specified physical diameter is 63.76 mm |
| `prop_nominal_diameter_mm` | 63.76 mm | Specified physical disk diameter |
| `prop_hub_thickness_mm` | 4 mm | Specified; not blade sweep thickness |
| `prop_bore_diameter_mm` | 1.5 mm | Specified |
| `prop_radial_clearance_mm` | 5 mm | Proposed radial clearance target |
| `prop_vertical_clearance_mm` | 5 mm | Proposed gap outside the measured blade sweep; verify blade flex allowance |
| `arm_width_mm` | 10 mm | Proposed, excluding larger root and motor pad |
| `arm_thickness_mm` | 4 mm | Proposed FDM starting thickness |
| `arm_root_fillet_mm` | 3 mm | Proposed; reduce only if geometry or fit requires |
| `center_length_mm` | 75 mm | Proposed X dimension; resize after electronics layout |
| `center_width_mm` | 55 mm | Proposed Y dimension; resize after electronics layout |
| `center_plate_thickness_mm` | 3 mm | Proposed |
| `holder_wall_mm` | 2 mm | Proposed starting wall thickness |
| `holder_fit_clearance_mm` | 0.5 mm | Proposed clearance per side; calibrate with the printer |
| `stack_separation_mm` | 20 mm | Proposed free space between bounding retention surfaces; Nano model alone is 18.21 mm high; cables/airflow may require more |
| `battery_length_mm` | 63 mm | Specified cell-pack envelope; excludes free leads/plugs |
| `battery_width_mm` | 15.5 mm | Specified |
| `battery_height_mm` | 13.5 mm | Specified |
| `p4_length_mm` | 50 mm | Supplied outline drawing |
| `p4_width_mm` | 50 mm | Supplied outline drawing |
| `p4_hole_spacing_u_mm` | 45.10 mm | Drawing, board-local horizontal axis |
| `p4_hole_spacing_v_mm` | 45.10 mm | Current manufacturer DXF/PDF; check purchased revision |
| `p4_hole_diameter_mm` | 2.70 mm | Manufacturer drawing [S1]; board hole, not printed holder clearance |
| `p4_pcb_thickness_mm` | 1.60 mm | Manufacturer drawing [S1] |
| `p4_component_above_pcb_mm` | 14.45 mm | Derived from STEP, PCB top datum [S1] |
| `p4_component_below_pcb_mm` | 2.16 mm | Derived from STEP, PCB underside datum [S1] |
| `p4_assembly_length_mm` | 50.1 mm | Rounded-up STEP X bound, before clearance |
| `p4_assembly_width_mm` | 52.9 mm | Rounded-up STEP Y bound, includes connector overhang |
| `p4_assembly_height_mm` | 18.3 mm | Rounded-up STEP Z bound, before clearance |
| `wifi_antenna_clearance_mm` | 15 mm | Espressif end-product recommendation [S6]; anchor to antenna area |
| `esc_length_mm` | 25 mm | Specified; check full insulated assembly |
| `esc_width_mm` | 20 mm | Specified |
| `esc_height_mm` | 7 mm | Specified |
| `motor_body_diameter_mm` | 14.8 mm | Specified overall diameter |
| `motor_body_height_mm` | 9.8 mm | Manufacturer drawing body height [S3] |
| `motor_overall_height_mm` | 14.8 mm | Drawing body plus 5 mm shaft projection [S3] |
| `motor_shaft_projection_mm` | 5 mm | Manufacturer drawing [S3] |
| `motor_mount_bcd_mm` | 9 mm | Four-hole bolt-circle diameter [S3] |
| `motor_mount_hole_count` | 4 | Dimensionless; four M2 threaded holes [S3] |
| `motor_mount_angle_deg` | 0° | Proposed cardinal orientation; rotate to suit lead exit |
| `standard_screw_length_mm` | 6 mm | User-selected M2×6 baseline; verify joint-specific engagement |
| `motor_thread_diameter_mm` | 2 mm | Specified M2 thread; not printed clearance-hole diameter |
| `motor_shaft_diameter_mm` | 1.5 mm | Specified |
| `camera_length_mm` | 25 mm | Specified board outline only |
| `camera_width_mm` | 24 mm | Specified board outline only |
| `camera_hole_diameter_mm` | 2.2 mm | Manufacturer board-hole drawing [S4] |
| `camera_hole_spacing_u_mm` | 21 mm | Manufacturer drawing [S4] |
| `camera_hole_spacing_v_mm` | 13.5 mm | Manufacturer drawing [S4]; offset pattern, see coordinates |
| `gps_length_mm` | 16.2 mm | Specified |
| `gps_width_mm` | 12.3 mm | Specified |
| `gps_height_mm` | 4.9 mm | Manufacturer total height including antenna [S5]; verify actual unit identity |
| `imu_length_mm` | 20.5 mm | Specified; longer side assigned to local length |
| `imu_width_mm` | 14.3 mm | Specified |
| `battery_slide_travel_mm` | 10 mm | Proposed fore/aft adjustment range |
| `strap_width_mm` | TBD | Actual strap width |
| `strap_thickness_mm` | TBD | Actual strap thickness |
| `strap_slot_extra_mm` | 1 mm | Proposed total extra width / height; calibrate |

Center dimensions and stack separation are layout seeds, not a claim that the Nano or soldered ESCs fit. A clearance failure requires changing the layout or parameters, never deleting a keep-out.

### 4.2 Remaining interface measurements and fit checks

Record inputs with value, units, source/date, status, and uncertainty where known. Dimensions already listed as Specified are no longer unknown; verify them through the relevant fit prototype. Leave genuinely unresolved dimensions as TBD. Block only the affected final part until its interface is resolved.

Initial proposed clear internal holder envelopes at 0.5 mm per-side fit clearance are **51 × 51 mm** for the Nano outline and **26 × 21 × 8 mm** for each ESC. The battery outline plus the same clearance is **64 × 16.5 × 14.5 mm**. The Nano figure describes PCB edge retention only; its populated STEP reference needs at least the separate 50.1 × 52.9 × 18.3 mm envelope before added clearance. These figures exclude attached cables, straps and service travel; ESC figures may also exclude added insulation and solder protrusions. An open cradle need not enclose the entire battery height.

| Subsystem | Required measurements / aliases |
| --- | --- |
| Motor | Fit-check Ø9 mm BCD/four M2 threads; measure safe screw engagement, underside protrusion and wire exit; choose `motor_mount_plate_mm` and washer thickness for M2×6 |
| Prop sweep | `prop_plane_z_mm`, `prop_sweep_thickness_mm`, fitted blade tips and hub, vertical movement/flex allowance |
| P4 Nano / Wi-Fi | Drawing and STEP resolve nominal holes, PCB thickness and populated envelope; verify actual revision, attached headers/cables, microSD/debug access and antenna-zone placement |
| Each ESC | Verify supplied envelope includes insulation; measure additional solder/heat-shrink extent, input/output wire exits; choose retention method |
| Battery | Verify supplied pack dimensions by fit; measure lead exit, XT30/JST-XH bodies and removal travel, strap dimensions |
| Camera | Drawing resolves board-hole coordinates/diameters; need actual G lens/body protrusion, PCB thickness, flex connector/cable envelope and bend allowance; confirm view at selected angle |
| GPS / IMU | Match GPS to FlyFishRC drawing; nominal total height includes antenna. Measure solder/wires, GY-91 populated/header height and axes, retention zones and connectors |
| Power components | Regulator, PDB/harness, capacitor if fitted, connectors, and insulated solder joints |
| Fasteners | Chosen diameter, head/washer/nut dimensions, clearance coupon result, screw engagement limits |

Represent irregular mounting patterns with a local hole-coordinate table, not one assumed square spacing. Measure the complete soldered assemblies where wiring changes their envelope.

## 5. FreeCAD document architecture

The authoritative source is `orion/ORION_frame.FCStd`. Use built-in Sketcher, Part Design, Part, and Spreadsheet tools where practical. Record the actual FreeCAD version used; do not require third-party workbenches for basic editing.

| Object / group | Purpose |
| --- | --- |
| `Parameters` | Input values, aliases, statuses, and input-only formulas |
| `ReferenceGeometry` | Origin axes, four motor axes, frame datum planes |
| `ComponentEnvelopes` | Named non-printable boxes/solids for every fitted component |
| `Keepouts` | Prop sweep cylinders, port access, connector travel, cable bend zones, sensor views |
| `CenterBase` | Center plate with arm joints, holder interfaces, and strap paths |
| `MasterArm` | One fully editable arm and motor mounting end |
| `ArmInstances` | Four linked/transformed instances derived from `MasterArm` |
| `P4Holder` | Removable Nano holder |
| `MasterESCHolder` | One editable holder; instance four times where identical |
| `SensorMounts` | Camera, GPS and IMU brackets; Wi-Fi clearance belongs to Nano layout |
| `BatteryCradle` | Retention and fore/aft adjustment interface |
| `CableRoutes` | Wire centerlines plus diameter/bend envelopes and tie points |
| `Checks` | Geometry measurements, collision results, and release status |

Each separately manufactured component must have its own editable Body or equivalent source object. Four separate arms must remain separate assembly objects; do not force disconnected arms into one Part Design Body. Reuse a master part through links/placements or an appropriate built-in duplication method that keeps changes synchronized.

Fully constrain primary dimensioned sketches. Prefer origin planes and named datum geometry over references to generated edge/face numbers. Apply fillets and cosmetic details after the main interfaces are stable. Keep printable bodies, reference geometry, and envelopes visually distinguishable and independently hideable.

## 6. Mechanical requirements

### 6.1 Center plate and arm joints

**FR-01:** Four motor axes must be symmetric and coplanar, driven by `wheelbase_mm`.

**FR-02:** Use four replaceable arms attached to a center plate. Prefer a keyed seating face plus two fasteners per arm joint, sized from selected hardware, so positioning does not rely solely on friction around one screw. A monolithic variant may be explored separately, but does not replace the serviceable baseline.

**FR-03:** Include smooth arm-root transitions and a continuous load path. Do not place cable holes, strap slots, or decorative cutouts through the narrowest arm-root section. Choose fastener edge distances from the actual material and coupon results.

**FR-04:** Replacing an arm must not require removing the P4 board. Motor/ESC wiring may need an accessible disconnect or documented unsoldering step; mechanical replaceability does not imply electrically tool-free replacement.

### 6.2 Actual motor mounts

**FR-05:** Use the MAMBA TOKA manufacturer's four M2 threads on Ø9 mm bolt circle, with the coordinates and placement angle in §2.4. Create printed through-holes from a calibrated M2 clearance parameter, not from the motor's thread diameter. Model the motor-body and screw-tip envelopes; provide screwdriver and underside protrusion clearance. Match the actual motor before export.

**FR-06:** Use **M2×6 mm** as the standard motor fastener. For a conventional under-head length, `engagement = 6 mm − motor-pad thickness − washer thickness`. Select pad/washer thickness so engagement lies within the actual motor's minimum holding depth and maximum safe thread depth. A 4 mm pad without a washer gives 2 mm nominal engagement; this is an arithmetic example, not evidence that 2 mm is safe. The manufacturer drawing does not give maximum safe insertion depth. Screw tips must remain outside winding/rotor interference zones. Countersunk heads need their own length convention; specify head type before finalizing the pad.

**FR-06a:** Standardize frame and holder fastening on M2×6 where the measured joint permits it; choose compatible nuts/inserts and clamped thickness accordingly. The user owns 12 M2×6 and 12 M2×4; **M2×4 are spares and are not allocated in this baseline**. Four screws at each of four motors require **16 M2×6**, already **four more than current stock**. Eight preferred arm-joint fasteners bring that subtotal to **24 M2×6**, twelve more than stock, before holders. Record the final joint-by-joint quantity and additional hardware required. A two- or three-screw motor variant requires a deliberate retention/stiffness decision and testing; do not silently omit mounting screws to match stock.

**FR-07:** Provide strain relief for phase wires before they leave the motor mounting area. The motor-pad diameter and any insert geometry must be derived from the actual motor and fasteners.

### 6.3 ESP32-P4 Nano holder

**FR-08:** Use a removable holder near the frame center, mounted through the four documented Ø2.70 mm board holes or edge clamps in verified component-free zones. For M2×6 retention, choose standoff/nut geometry to provide engagement through the 1.60 mm PCB without loading components. Do not squeeze connectors, antennas, or exposed components.

**FR-09:** Reserve underside clearance, insulation, airflow, camera-cable exits, debug/programming access, and microSD insertion/removal travel. The board must be removable without cutting cable ties that also secure propulsion wiring.

**FR-10:** Separate the electronics retention surface from primary frame fasteners where practical. Optional upper protection must be removable and must pass propeller clearance checks.

### 6.4 Four ESC holders

**FR-11:** Provide four independently removable holders, initially on the inner arm sections or adjacent center quadrants. Exact placement follows measured ESC length and the clearance model.

**FR-12:** Account for heat-shrink, solder bulges, wires, and insulation. Use an open tray with an adjustable retention strap/clip; do not embed or completely seal an ESC in a printed cavity. Verify temperatures on the assembled hardware before fixing the final cover design.

**FR-13:** Provide separate strain relief at power and phase lead exits. Routing must avoid the blade sweep, arm joint fasteners, sharp edges, and battery strap paths.

### 6.5 Battery, sensors, and power components

**FR-14:** Retain the battery with two strap paths and a non-slip support. Allow at least the proposed fore/aft adjustment travel, subject to clearance. Removal and XT30 unplugging must not require dismantling the electronics stack.

**FR-15:** Make the Waveshare Type G OV5647 front bracket removable and angle-adjustable, using the 25 × 24 mm board envelope and offset four-hole coordinate table in §2.4. Use M2×6 with a measured spacer/nut stack through the Ø2.2 mm PCB holes; preserve clearance to components and traces. Record the selected angle relative to +X and model lens protrusion, flex-cable bends, and optical access. The supplied 160° is a diagonal fisheye field of view; do not treat it as 160° horizontally and vertically or as an exact pinhole cone. Validate the usable image with the bracket installed.

**FR-16:** Place the GY-91 near the origin, with its marked axes recorded relative to the frame axes. Include an optional soft-mount interface; stiffness/isolation settings require vibration testing rather than a fixed assumed optimum.

**FR-17:** Give the GPS an upward-facing antenna zone, initially above or behind the center assembly. Keep it as far from switching power components and high-current wiring as packaging allows; record actual separation distances for later electrical evaluation.

**FR-18:** Use onboard Wi-Fi reception only. Anchor the 15 mm housing antenna keep-out to the Nano’s C6 antenna zone and check it against battery, frame hardware, added electronics and cable routes. Model the regulator, PDB/harness, capacitor, and all connectors as retained, insulated components, not loose space reservations.

**FR-19:** Add accessible cable-tie/clip points with rounded contact edges. Power and sensor routes should be physically separable where practical. No wire may rely on glue alone for blade-clearance retention.

## 7. Clearance model

For each motor, model a non-printable blade sweep cylinder:

- Physical radius: `prop_diameter_mm / 2`.
- Radial keep-out radius: `prop_diameter_mm / 2 + prop_radial_clearance_mm` (37.5 mm initially).
- Z center: measured `prop_plane_z_mm`.
- Z extent: measured `prop_sweep_thickness_mm` plus twice the vertical clearance allowance.

**Use 3D clearance.** Arms and motor pads are intentionally below the propeller sweep and will overlap a prop circle in top view. That overlap alone is acceptable when their complete solids remain below the inflated Z envelope. The propeller hub/shaft occupies its intended interface; document that narrow exception. No arm, holder, payload, connector, fastener, or cable may occupy the blade region at sweep height.

Top-view circles are conservative layout aids for components that reach sweep height. They are not a blanket ban on motor supports beneath the rotor. This corrects the older PRD's physically impossible requirement that every printed solid avoid every prop circle in plan view.

**CLR-01:** Expanded prop sweep volumes must be mutually disjoint at all supported wheelbases.

**CLR-02:** Printable parts and component/cable envelopes must have no unplanned intersections. Explicitly list intended interfaces: arm seats, fasteners, board supports, straps, and motor mounting faces.

**CLR-03:** Port access and connector mating/removal paths must remain clear in the assembled configuration.

**CLR-04:** Camera viewing zones, GPS and onboard Wi-Fi antenna zones, cable bends, and battery adjustment positions must be checked throughout their intended range.

**CLR-05:** Check a cable as a finite-diameter envelope with strain relief, not only as a mathematical line. Capture both top and side evidence for prop clearance.

## 8. Printing and assembly

- Use one flat-printed arm as the first structural/fit prototype. Select final material, orientation, wall count, infill, and temperatures after testing the intended filament and printer; the starting dimensions are not strength guarantees.
- Print a small hole/slot/holder-clearance coupon before finalizing fastener and board fits. Record measured clearance rather than applying one offset to every feature.
- Keep supports off motor seating faces and critical joint interfaces where practical. Split holders or revise geometry if support removal would damage them.
- Avoid excess mass from decorative shells, dense covers, and unused legacy hardware mounts. Record slicer estimates and actual printed masses separately.
- Size each exported part for the actual printer bed, including brim/support allowance. The assembled sweep footprint is not the footprint of each modular print.
- Assemble frame joints and motor mounts first, then ESC holders and power retention, battery cradle, P4 holder, sensors, and cable restraints. Confirm all connectors and fasteners remain accessible after each step.
- Provide landing contact points that protect the lowest battery/electronics parts. Their height remains TBD until the complete underside layout is known.

## 9. Modeling and verification sequence

1. **Measurement:** Identify the actual motor and boards; complete the hole-coordinate and soldered-envelope records.
2. **Skeleton:** Create the parameter sheet, datum planes, four motor axes, and 180/190/200 mm layout references.
3. **Packaging:** Position component envelopes, prop sweep volumes, service access paths, and cable routes before detailed brackets.
4. **Primary structure:** Model center plate, one arm, keyed arm joints, actual motor mounts, and linked arm instances.
5. **Holders:** Model Nano holder and one ESC holder; derive all four ESC placements from assembly parameters.
6. **Payload:** Add battery adjustment, camera bracket, IMU mount, GPS support, onboard Wi-Fi keep-out, and power-component supports.
7. **CAD checks:** Recompute; inspect shape validity, collisions, access, and symmetry at each evaluated wheelbase. Record a failing size as unsupported until redesigned.
8. **Fit prototypes:** Print one arm/motor mount, one ESC holder, Nano-holder interface, and tolerance coupon. Update parameters from fit results.
9. **Full assembly:** Print the remaining accepted parts, fit actual hardware, weigh the assembly, and measure balance.
10. **Release:** Save the final model and export only the selected printable solids. Record actual settings and remaining limitations.

Keep CAD recompute results, physical fit results, and flight tests separate. No CAD model or tests have been produced by this specification itself.

## 10. Acceptance criteria

| ID | Pass condition | Evidence |
| --- | --- | --- |
| AC-01 | FCStd opens and recomputes without broken dependencies | FreeCAD version and recompute log/screenshot |
| AC-02 | Motor axes match the true-X formulas; placement error ≤ 0.1 mm in CAD | Coordinate/distance report at 190 mm |
| AC-03 | 180, 190, and 200 mm variants recompute; clearance status recorded for each | Variant check table; passing sizes explicitly identified |
| AC-04 | Final motor mount matches actual holes and internal screw limits | Measurement record and single-mount physical fit |
| AC-05 | P4 Nano fits with underside clearance, port access, and removable retention | Fit photo and port/SD access demonstration |
| AC-06 | All four soldered ESC assemblies fit their holders with strain relief and airflow | Envelope check and assembled fit photos |
| AC-07 | No unapproved intersection with expanded prop sweep volumes | Top and side views plus interference check results |
| AC-08 | Battery is retained, adjustable, and removable with the electronics assembled | Strap/connector clearance and physical fit |
| AC-09 | Camera, GPS, IMU and power parts are retained with clear access/routing; onboard Wi-Fi antenna placement follows the recorded keep-out | Assembly photos, sensor axes, antenna clearance report and assembled link check |
| AC-10 | An arm and an ESC holder can be replaced without removing the Nano board | Documented removal sequence |
| AC-11 | Every STL corresponds to an editable source object; reference objects excluded | Export object list and valid closed mesh checks |
| AC-12 | Mass, installed component masses, and balance are recorded | Scale readings and CG report |
| AC-13 | All required measured inputs for a released part are resolved | Measurement table with no relevant TBD entries |

Target assembled CG within 5 mm horizontally of the origin as a proposed starting criterion, using battery position for adjustment. Record actual CG and component masses; this target does not establish control stability. Structural suitability and payload capacity remain subject to measured propulsion and hardware tests.

If 180 mm fails packaging, retain it as an evaluated but unsupported variant. A 190 mm default is acceptable only after it passes the same checks; increasing to 200 mm is a documented design change, not an automatic clearance guarantee.

## 11. Required project deliverables

| Path | Required contents |
| --- | --- |
| `orion/SPEC.md` | This specification and revision history |
| `orion/ORION_frame.FCStd` | Authoritative editable model |
| `orion/README.md` | FreeCAD version, parameter guide, assembly sequence, materials/settings, supported variants |
| `orion/measurements.csv` | Component dimensions, hole coordinates, masses, sources/dates, unresolved values |
| `orion/export/ORION_arm.stl` | Accepted master arm geometry; print quantity four |
| `orion/export/ORION_center_base.stl` | Accepted center structure |
| `orion/export/ORION_p4_holder.stl` | Accepted Nano holder |
| `orion/export/ORION_esc_holder.stl` | Accepted common ESC holder; print quantity four if identical |
| `orion/export/ORION_*_mount.stl` | Accepted camera, GPS, IMU and battery parts as applicable |
| `orion/screenshots/` | Top, bottom, side, exploded, port-access, and clearance evidence |

Only `SPEC.md` is delivered at this stage. The remaining paths define subsequent CAD implementation outputs. Preserve upstream Darkstar2 files as references; do not overwrite them or treat STL meshes as the editable master.

## 12. Release limits and references

Research resolves the nominal motor bolt circle/body/shaft geometry, Nano holes/PCB thickness and populated STEP bounds, camera board-hole pattern, GPS total antenna-inclusive height, battery size and propeller dimensions. The Wi-Fi-only architecture removes the external receiver interface.

The remaining physical inputs are safe motor thread engagement and underside clearance; Nano revision and attached cable/header envelopes; ESC solder/insulation/wire extent; installed propeller sweep and flex; camera lens/body depth, PCB thickness and actual FFC route; GY-91 populated/header height and mounting/axis details; battery connector/strap geometry; regulator/PDB/harness packaging; M2×6 head/material/nut dimensions and final quantity; printer/material settings, mass and propulsion margin. None can be established reliably from a generic model name alone.

The final frame print is blocked until its measurement and fit criteria pass. Flight release is separate and requires verified electrical integration, control/failsafe operation, no-prop bring-up, and physical structural/vibration checks. This frame spec makes no claim about ESP32-P4 flight-controller firmware maturity, hover capability, payload capacity, flight time, or crash resistance.

Project references used for this revision:

- User-supplied component specifications, 2026-10-10 — latest nominal dimensions, motor/camera identity, component masses, and purchased screw quantities.
- `image(20261010-112726).png` — user-supplied ESP32-P4 Nano outline drawing; 50 × 50 mm board and 45.10 × 45.09 mm hole spacing.
- `image(20261010-115550).png` — user-supplied MAMBA TOKA 1103 10000KV manufacturer drawing, corroborating source S3 and its four M2 threads on Ø9 mm bolt circle.
- User clarification, 2026-10-10 — onboard Wi-Fi reception, no external receiver; selected standard M2×6 screw length.

- `ORION_Darkstar2_Frame_PRD.md` — 190 mm parametric frame baseline and legacy hardware layout.
- `ORION_ESP32_P4_ESC_Wiring_Guide.docx` — Nano and four individual ESC architecture; its motor entry is superseded by the supplied MAMBA TOKA specification.
- `RyanAdidaru_2306266994_Despro2_Week6.pdf` — later Nano, OV5640, M10 Mini, and GY-91 progress content. Its internal week/date labels are inconsistent; use it for component context rather than a precise chronology.

### 12.1 Research sources and limits (checked 2026-10-10)

| ID | Source | Information used / limit |
| --- | --- | --- |
| S1 | [Waveshare Nano hardware resources](https://docs.waveshare.com/ESP32-P4-NANO/Resources-And-Documents); [official drawing/STEP ZIP](https://files.waveshare.com/wiki/ESP32-P4-NANO/ESP32-P4-Nano.zip) | 20260331 PDF/DXF hole geometry and PCB thickness; STEP solid bounds calculated locally. Confirm purchased revision; attached cables not modeled. |
| S2 | [Waveshare Nano hardware description](https://docs.waveshare.com/ESP32-P4-NANO) | ESP32-C6-MINI-1 onboard Wi-Fi coprocessor over SDIO; ports and service access. |
| S3 | [MAMBA/TOKA 1103-10000KV manufacturer engineering graphic](https://cdn.shopify.com/s/files/1/0914/9972/5181/files/1103-10000kv.jpg?v=1754254574), republished by [Unmanned Tech](https://www.unmannedtechshop.co.uk/products/diatone-mamba-toka-1103-2-3s-brushless-motor-6500kv-8500kv) | Branded drawing: four M2 on Ø9 BCD, Ø14.8 body, 9.8 body height, 5 shaft projection, 4.8 g including wires. The hosting page title mentions other KV variants; use the graphic labeled 10000KV. No safe insertion depth. |
| S4 | [Waveshare Camera G wiki](https://www.waveshare.com/wiki/RPi_Camera_(G)); [shared E/F/G/H mechanical ZIP](https://www.waveshare.com/w/upload/8/8a/RPi_Camera_E_F_G_H_Mechanical.zip); [Camera G product](https://www.waveshare.com/rpi-camera-g.htm) | DWG plan view: 25 × 24 board, Ø2.2 mounting holes, 21 × 13.5 spacing and offsets. The shared plan view does not resolve the G fisheye lens's full Z envelope. |
| S5 | [FlyFishRC M10 Mini manufacturer manual](https://cdn2.mantisfpv.com.au/wp-content/uploads/2023/08/FlyFishRC-M10-Mini-GPS-Module-Manual.pdf), hosted by MantisFPV | Explicit total 12.3 × 16.2 × 4.9 mm, patch 11.7 × 11.7 mm, nominal 2.4 g. Dimensions match user's listing; actual module identity remains a fit check. No dimensioned screw pattern. |
| S6 | [Espressif ESP32-C6 PCB layout / end-product guidance](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c6/pcb-layout-design.html) | At least 15 mm antenna clearance inside end-product housing and assembled radio evaluation. Existing Nano PCB is supplied hardware. |
| S7 | [BETAFPV LAVA 450 mAh battery](https://betafpv.com/products/lava-2s-3s-4s-450mah-75c-battery-2pcs) | Confirms 2S 63 × 15.5 × 13.5 mm, 26.1 g, XT30/16AWG and listed balance plug. Lead/plug travel absent. |
| S8 | [Gemfan 2512 Hurricane PC three-blade](https://www.gemfanhobby.com/2512-hurricane-pc-3-blade.html) | Confirms disk Ø63.76, hub 4 mm and bore Ø1.5. Does not establish installed blade sweep Z or flex. |

**Interfaces that still need the purchased hardware:** The generic BLHeli 12A/SIL F330 description and GY-91 name do not identify a unique manufacturer PCB revision with a reliable mechanical drawing. Retain the user's 25 × 20 × 7 mm ESC and 20.5 × 14.3 mm IMU outlines as Specified; leave populated heights, solder bulges and retention zones unresolved. Chip package drawings do not establish the breakout board envelope. Do not use another GY-91 seller's hole spacing or another 12A ESC's dimensions as measured data.

**Connectors and cable bends:** “XT30” does not identify one exact connector housing variant. Reserve adjustable plug access until the actual mated pair and insulation are measured. BETAFPV lists “JST-XH2.54”; genuine [JST XH](https://www.jst-mfg.com/product/pdf/eng/eXH.pdf) is a 2.50 mm-pitch family, so the listing name alone must not define a precise plug pocket. Camera cable length/contact orientation and connector adaptation must match the actual Nano/camera connection; the [Waveshare camera manual](https://files.waveshare.com/upload/6/61/RPi-Camera-User-Manual.pdf) advises avoiding sharp bends but supplies no numeric minimum bend radius. Use a measured route, not an invented rated radius.

**Research method:** Inspect original dimension graphics, extract DWG/DXF dimensions and coordinates, and calculate global bounds from STEP solids. Reseller prose is not used to override manufacturer geometry. Manufacturer CAD values remain Specified/Derived until hardware fit checks; no physical dimensions have been measured in this revision. These sources support mechanical packaging, not an all-up propulsion or electrical compatibility claim.

FreeCAD implementation references:

- [Official Spreadsheet Workbench documentation](https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Spreadsheet_Workbench.md) — aliases and spreadsheet-driven dimensions.
- [Official Expressions documentation](https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Expressions.md) — expression references and dependency handling.

### Revision history

| Revision | Date | Change |
| --- | --- | --- |
| 0.1 | 2026-10-10 | Initial Nano / four-ESC frame specification; explicit size definitions, measurement gates, and 3D prop-clearance model |
| 0.2 | 2026-10-10 | Added supplied battery/ESC/prop/motor/sensor dimensions, Nano drawing, OV5647 Type G baseline, nominal mass subtotal, and M2×4/M2×6 inventory; narrowed remaining measurements |
| 0.3 | 2026-10-10 | Researched manufacturer drawings/CAD; corrected motor Ø9 bolt circle, Nano holes/heights, camera mounting coordinates and GPS total height; onboard Wi-Fi only; standardized M2×6 fastening and noted additional screw quantities |

### Branch design revision — 2026-10-11

User-authorized on `feat/top-esc-retention`: replace FR-11’s separate arm-mounted ESC holders with four insulated ESCs secured by two nylon ties each to top-side fingers integrated into the center plate. Keep ESCs individually removable by cutting/replacing ties. Remove the provisional regulator/PDB envelope, its printed power tray and two mounting joints; retain the requirement for verified electrical power distribution, regulation, insulation and cable retention once actual hardware is selected. This supersedes the separate-ESC-holder and candidate-power-tray geometry for this branch only. Remaining mechanical and electrical verification requirements still apply.
