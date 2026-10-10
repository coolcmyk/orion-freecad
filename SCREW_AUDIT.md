> Current tower also obstructs two rear Nano-holder driver paths (about 9.57 mm³ per trial driver at 190 mm). Install the Nano holder before the shared sensor tower; independent access is unresolved. The earlier statement below that driver paths were clear predates this tower revision.

> Shared-sensor revision: old underside IMU mount removed; GPS posts/mounts moved to Y±14 mm. Current provisional count is 50 screws. Battery floor raised 10 mm. The current JSON report supersedes the historical count/layout below.

> Arm-top revision: integral motor pads are raised 5 mm, with recessed underside head wells preserving 4 mm nominal grip and 2 mm M2×6 engagement. Current gauge checks clear these revised motor joints; real head size, safe motor depth and printed-pad strength remain unverified.

> Branch revision 2026-10-11: the eight ESC-tray screws and two power-tray screws are removed (52 remaining). Those old obstructions are historical; `screw_audit.json` is the current geometry report. The detailed table below records the earlier 62-joint audit. The refreshed audit has no shaft-pair collisions or driver obstructions at any tested wheelbase; remaining recorded collisions are four inner arm tip/nut contacts with the Nano holder, four Nano-holder nut contacts with battery supports, and four battery screw-head contacts with the Nano holder. Actual hardware/thread/antenna suitability remains unverified.

# Screw assembly audit — 2026-10-10

**Result: FAIL. The current model is not ready for full-frame printing.**

**Camera revision:** the original camera defects listed below have since been revised. The new mount passes trial shaft/head/nut/driver gauges at five sampled angles (−20° through +30°) and all three wheelbases. See `camera_mount_checks.json` and the refreshed `screw_audit.json`. Actual hardware remains unverified; other frame fastening defects remain.

All 62 proposed M2×6 screw locations were checked in an independent FreeCAD process at 180, 190 and 200 mm wheelbase, using a snapshot of the live `ORION_frame` document. The live CAD geometry was not changed. `scripts/audit_screws.py` produces the per-screw results in `screw_audit.json`.

Earlier `cad_checks.json` tests checked printed parts and nominated component envelopes, without installed fasteners. Those results do not establish screw fit or assembly access.

## Method and limits

The audit models 2 mm diameter, 6 mm long shafts; hypothetical 4.6 mm diameter × 2 mm heads; hexagonal nuts with 4.156922 mm across flats × 1.6 mm thickness; and straight 3 mm diameter × 12 mm driver access. These head, nut and driver dimensions are **trial gauges, not measurements of purchased hardware**. A nut is checked at one hex orientation. Chamfers, nut bores, washers, thread strength, flexible cables, real motor internals and hand access are not established by this check. A separate full detailed Nano STEP hardware intersection attempt exceeded 180 seconds: those intersections remain **unverified**. The nominal board mounting pattern/stack and modeled camera PCB are covered by the audit, but this does not establish clearance from all Nano components.

Checks distinguish installed hardware interference from driver paths blocked by already installed parts. Some driver obstructions can be avoided by assembly order; that does not establish independent serviceability.

## Results by joint

| Joint | Screws | Result and required action |
|---|---:|---|
| Motors | 16 | Nominal shaft/head paths clear of printed parts. Four-millimeter pads give 2 mm arithmetic engagement. Actual motor safe depth, head fit and thread strength remain unverified. |
| Keyed arm roots | 8 | **Four inner screw tips intersect Nano-holder plastic**, approximately 0.608 mm³ per screw. Trial nuts also interfere with the holder. The 1.2 mm deep pockets do not fully recess the 1.6 mm trial nuts. At 180 mm, the four outer root driver paths also hit the ESC trays. Revise holder reliefs, nut seats and service clearance. |
| ESC trays to arms | 8 | Inner four driver paths intersect the center plate at all three wheelbases. Install-before-arm sequencing may permit assembly, but independent removal is not established. Square nut cavities have no verified retention. |
| Nano PCB to holder | 4 | The nominal 1.6 mm PCB plus 2 mm boss cap leaves 2.4 mm of a 6 mm screw for nut/extension. Nuts must be fitted and held before the holder goes onto the center plate; its circular cavities do not prevent rotation. Detailed STEP contacts and hardware material require review. |
| Nano holder to center | 4 | Circular underside recesses do not prevent nut rotation. All four trial hex nuts intersect the battery supports, approximately 0.163 mm³ each. Final nut dimensions, retention and conductive-hardware keepout are unresolved. |
| Battery cradle to center | 4 | **All four trial screw heads intersect the Nano holder**, approximately 25.429 mm³ each. Assembly order cannot remove an installed-head collision. Provide proper head clearance. The 1.7 mm pilots are not verified threads or insert seats. |
| Camera PCB to frame | 4 | Nominal frame/PCB hole paths are clear of the modeled printed parts. PCB thickness, spacers, head/component fit and actual nut retention remain unverified. |
| Camera pivots | 2 | Trial shafts, heads and nuts intersect the modeled ears/supports/frame. Bearing-to-nut distance is 4.4 mm; adding a 1.6 mm trial nut consumes all 6 mm, leaving no tip allowance. Revise the ears, hole relief, hardware seating and thickness stack while preserving the M2×6 baseline. |
| Camera fixed base | 2 | Trial heads and straight driver paths intersect the camera uprights. Add seating/tool relief or relocate the joint. Circular nut recesses also need a retention solution. |
| GPS support | 2 | Driver paths from below intersect the installed power tray. Fit GPS before that tray or revise service access. Three-millimeter nominal screw penetration into pilots does not establish reliable threads. |
| IMU support | 2 | Nominal shaft/head/driver gauges clear of modeled printed parts. The pilot/thread or insert interface remains unverified. |
| Power support | 2 | Nominal shaft/head/driver gauges clear of modeled printed parts. The pilot/thread or insert interface remains unverified. |
| Landing skids | 4 | Nominal shaft/head/driver gauges clear of modeled printed parts. The pilot/thread or insert interface remains unverified. |
| **Total** | **62** | **No group is physically verified with actual hardware.** |

## The joint in the screenshot

Nano-board and inner arm screw axes are about 1.891 mm apart in plan. **Their finite 6 mm shafts do not intersect each other**, because their installed axial ranges are at different heights. The real defect is the inner arm screw entering the holder and the competing nut/access space. The outside-arm reliefs alone do not resolve it.

Next revision should resolve the definite screw-tip interference first, then head and nut seating, assembly order and independent tool access. Retest every joint with the selected hardware dimensions, then print a coupon and representative joint before the complete frame. The camera frame and base have now been revised and their prototype meshes regenerated. Other frame fastening defects remain unresolved.
