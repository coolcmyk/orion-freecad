# ORION mass estimate — 2026-10-11

Default 190 mm wheelbase; arm-top ESCs, motors raised 5 mm, shared GPS/IMU tower and compact battery cradle. CAD estimate, not a scale measurement.

| Printed group | Quantity | Solid PLA (g) |
|---|---:|---:|
| ArmSolid | 4 | 25.2 |
| CenterBaseSolid | 1 | 17.9 |
| P4HolderSolid | 1 | 3.4 |
| BatteryCradleSolid | 1 | 7.6 |
| GPSMountSolid | 1 | 3.5 |
| CameraFrameSolid | 1 | 1.3 |
| CameraBaseSolid | 1 | 0.9 |
| LandingSkidRevised | 2 | 3.7 |

Printable CAD volume: **51.11 cm³**. Solid PLA: **63.4 g**; solid PETG: **64.9 g**. Count four arms and two skids; exclude electronics/envelopes, coupon, supports, brim and unused legacy parts.

Density assumptions: PLA 1.24 g/cm³ ([Prusament datasheet](https://prusament.com/wp-content/uploads/2022/10/PLA_Prusament_TDS_2021_10_EN.pdf)), PETG 1.27 g/cm³ ([Prusament datasheet](https://prusament.com/wp-content/uploads/2022/10/PETG_Prusament_TDS_2021_10_EN.pdf)). Exact filament and extrusion differ. Infill percentage cannot simply multiply this total because shells and top/bottom layers remain. Use slicer extrusion mass for the selected orientations/profile.

| Assembled contribution | Mass (g) | Basis |
|---|---:|---|
| Printed parts, solid PLA | 63.4 | CAD volume × density |
| Battery | 26.1 | Specified |
| Four motors | 19.2 | 4 × 4.8 specified |
| Four ESCs | 36.0 | 4 × 9 specified |
| Four props | 3.2 | 4 × 0.8 specified |
| GPS | 2.4 | Nominal candidate specification |
| Nano | 20–35 | Unverified allowance |
| Camera | 8–15 | Unverified allowance |
| IMU, regulator, additional harness, insulation, ties/straps and fasteners | 15–30 | Unverified allowance; avoid double-counting supplied motor/ESC/battery wires |

Solid-PLA assembled subtotal including specified components and GPS: **150.3 g**. Add **43–80 g** of unweighed allowances: **193–230 g** assembled (approximately **210 g** for planning). Solid PETG adds about **1.5 g**.

Printed PLA reduction from the original 58.115 cm³ tray/power layout is about **8.7 g**. Motor raising added material, so savings are smaller than the superseded side-ESC layout. Removal of geometric power placeholders does not remove actual regulator/harness mass. Final print settings and measured Nano/camera/hardware mass can move the estimate outside this allowance range.
