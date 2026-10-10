"""Independent nominal top ESC retention check. Caller supplies doc."""
from pathlib import Path
import FreeCAD as App
import Part, json
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'scripts/audit_screws.py'
exec(compile(p.read_text().split("report={'status':")[0],str(p),'exec'))
sheet=doc.Parameters
wc=sheet.getCellFromAlias('wheelbase_mm');original=sheet.getContents(wc)
poses=[]
printed=['CenterBaseSolid','P4HolderSolid','BatteryCradleSolid','GPSMountSolid','IMUMountSolid','CameraFrameSolid','CameraBaseSolid']+[o.Name for o in doc.Objects if o.TypeId=='App::Link']
# The detailed Nano bound is a conservative check here; every proposed ESC clears it.
reference=['NanoAssemblyBounds','WiFiAntennaKeepout','BatteryEnvelope','GPSEnvelope','IMUEnvelope','CameraGPCB','CameraGSensorHousing','CameraGFisheyeBarrel','CameraGRearFFC','CameraGFFCLatch']+['ExpandedPropSweep'+str(i) for i in range(4)]
try:
 for wb in [180,190,200]:
  sheet.set(wc,str(wb)+' mm');doc.recompute()
  errors=[o.Name for o in doc.Objects if 'Error' in o.State or 'Invalid' in o.State]
  obstacles={n:world(doc.getObject(n)) for n in printed+reference if doc.getObject(n)}
  hits=[];distances=[]
  escs={f'ESCEnvelope{i}':world(doc.getObject(f'ESCEnvelope{i}')) for i in range(4)}
  for n,s in escs.items():
   for m,t in obstacles.items():
    v=overlap(s,t)
    if v>1e-4:hits.append({'esc':n,'other':m,'volume_mm3':round(v,6)})
   distances.append({'esc':n,'prop_keepout_distance_mm':round(min(s.distToShape(obstacles[f'ExpandedPropSweep{i}'])[0] for i in range(4)),3),'antenna_keepout_distance_mm':round(s.distToShape(obstacles['WiFiAntennaKeepout'])[0],3)})
  for i in range(4):
   for j in range(i+1,4):
    if overlap(escs[f'ESCEnvelope{i}'],escs[f'ESCEnvelope{j}'])>1e-4:hits.append({'esc_pair':[i,j]})
  center=obstacles['CenterBaseSolid'];centerhits=[]
  for n in printed[1:]:
   v=overlap(center,obstacles[n])
   if v>1e-4:centerhits.append({'part':n,'volume_mm3':round(v,6)})
  valid=all(obstacles[n].isValid() and len(obstacles[n].Solids)==1 for n in ['CenterBaseSolid','Arm_FL','Arm_RL','Arm_RR','Arm_FR'])
  poses.append({'wheelbase_mm':wb,'errors':errors,'valid_print_solids':valid,'esc_intersections':hits,'center_intersections':centerhits,'clearance':distances})
  print(wb,'ESC hits',hits,'center hits',centerhits,flush=True)
finally:
 sheet.set(wc,original);doc.recompute()
passed=all(not p['errors'] and p['valid_print_solids'] and not p['esc_intersections'] and not p['center_intersections'] for p in poses)
result={'status':'PASS nominal top ESC layout' if passed else 'FAIL','poses':poses,'limits':'25 x 20 x 7 mm supplied ESC envelopes; 0.5 mm proposed insulating pad; lead exits, ties, solder, heat-shrink, installed blade flex, real antenna behavior and strength unverified. The negative-Y pair has limited clearance at 180 mm. Existing other fastener defects remain.'}
(ROOT/'top_esc_checks.json').write_text(json.dumps(result,indent=2)+'\n')
assert passed,'See top_esc_checks.json'
