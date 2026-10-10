"""Shared GPS/IMU tower and compact battery checks; caller supplies doc."""
import FreeCAD as App,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'scripts/audit_screws.py'
exec(compile(p.read_text().split("report={'status':")[0],str(p),'exec'))
printed=['CenterBaseSolid','P4HolderSolid','BatteryCradleSolid','GPSMountSolid','CameraFrameSolid','CameraBaseSolid']+[o.Name for o in doc.Objects if o.TypeId=='App::Link']
refs=['NanoAssemblyBounds','WiFiAntennaKeepout','IMUEnvelope','GPSEnvelope','BatteryEnvelope','CameraGPCB','CameraGFisheyeBarrel','CameraGRearFFC']+[f'ESCEnvelope{i}' for i in range(4)]+[f'ESCTieAllowance{i}' for i in range(4)]+[f'ExpandedPropSweep{i}' for i in range(4)]
wc=doc.Parameters.getCellFromAlias('wheelbase_mm');bc=doc.Parameters.getCellFromAlias('battery_offset_x_mm');original=[doc.Parameters.getContents(c) for c in [wc,bc]];rows=[]
try:
 for wb in [180,190,200]:
  doc.Parameters.set(wc,str(wb)+' mm')
  for shift in [-5,0,5]:
   doc.Parameters.set(bc,('=0 mm - 5 mm' if shift<0 else str(shift)+' mm'));doc.recompute()
   shapes={n:world(doc.getObject(n)) for n in printed+refs if doc.getObject(n)};hits=[];plastic_antenna=[]
   for n in ['GPSMountSolid','BatteryCradleSolid','IMUEnvelope','BatteryEnvelope']:
    for m,s in shapes.items():
     if n==m:continue
     # GPS feet are intended to touch center at Z0, battery supports touch Z-3.
     v=overlap(shapes[n],s)
     if v>1e-4:
      hit={'part':n,'other':m,'volume_mm3':round(v,6)}
      if n=='BatteryCradleSolid' and m=='WiFiAntennaKeepout':plastic_antenna.append(hit)
      else:hits.append(hit)
   errors=[o.Name for o in doc.Objects if 'Error' in o.State or 'Invalid' in o.State]
   valid=all(shapes[n].isValid() and len(shapes[n].Solids)==1 for n in ['GPSMountSolid','BatteryCradleSolid','CenterBaseSolid'])
   gap=shapes['CenterBaseSolid'].BoundBox.ZMin-shapes['BatteryEnvelope'].BoundBox.ZMax
   rows.append({'wheelbase_mm':wb,'battery_shift_mm':shift,'errors':errors,'valid_print_solids':valid,'hits':hits,'nominal_battery_top_gap_mm':round(gap,3),'existing_nonconductive_support_in_antenna_zone':plastic_antenna})
   print(wb,shift,'hits',hits,flush=True)
finally:
 for c,v in zip([wc,bc],original):doc.Parameters.set(c,v)
 doc.recompute()
passed=all(not r['errors'] and r['valid_print_solids'] and not r['hits'] for r in rows)
report={'status':'PASS nominal shared tower and compact battery' if passed else 'FAIL','poses':rows,'limits':'IMU populated height 5 mm and pad 0.5 mm are proposed. Header/cable/strap geometry, pilot retention, GPS/IMU performance and structural suitability need physical checks; Existing nonconductive battery support intrusion into the antenna zone is recorded separately; RF performance remains unverified. Other frame fastener defects remain.'}
(ROOT/'sensor_battery_checks.json').write_text(json.dumps(report,indent=2)+'\n')
assert passed,'See sensor_battery_checks.json'
