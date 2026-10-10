"""Check camera motion and trial fasteners in a supplied independent FreeCAD doc."""
from pathlib import Path
import FreeCAD as App
import json

ROOT=Path(__file__).resolve().parents[1]
# Load helpers without running the full three-wheelbase audit.
audit=ROOT/'scripts'/'audit_screws.py'
exec(compile(audit.read_text().split("report={'status':")[0],str(audit),'exec'))
sheet=doc.Parameters
wbcell=sheet.getCellFromAlias('wheelbase_mm')
tiltcell=sheet.getCellFromAlias('camera_tilt_deg')
original=(sheet.getContents(wbcell),sheet.getContents(tiltcell))
camera=['CameraFrameSolid','CameraBaseSolid']
other=['CenterBaseSolid','P4HolderSolid','BatteryCradleSolid','GPSMountSolid','IMUMountSolid','PowerMountSolid']
other += [o.Name for o in doc.Objects if o.TypeId=='App::Link']
components=['BatteryEnvelope','GPSEnvelope','IMUEnvelope','PowerPackageProposed','CameraPCBReference','CameraLensProposed']
components += ['ESCEnvelope'+str(i) for i in range(4)]+['ExpandedPropSweep'+str(i) for i in range(4)]
if doc.getObject('CameraGReconstruction'):
    components += ['CameraGPCB','CameraGSensorHousing','CameraGLensShoulder','CameraGFisheyeBarrel',
                   'CameraGFocusRim','CameraGOpticalFace','CameraGRearFFC','CameraGFFCLatch']
results=[]
try:
    for wb in [180,190,200]:
        sheet.set(wbcell,str(wb)+' mm')
        for tilt in [-20,-15,0,15,30]:
            sheet.set(tiltcell,('=0 deg - '+str(-tilt)+' deg') if tilt<0 else str(tilt)+' deg')
            doc.recompute()
            errors=[o.Name for o in doc.Objects if 'Error' in o.State or 'Invalid' in o.State]
            shapes={n:world(doc.getObject(n)) for n in camera+other+components}
            hits=[]
            for n in camera:
                for m in camera+other+components:
                    if n==m or (n=='CameraBaseSolid' and m=='CameraFrameSolid'):continue
                    v=overlap(shapes[n],shapes[m])
                    if v>1e-4:hits.append({'camera':n,'other':m,'overlap_mm3':round(v,6)})
            gauges=audit_variant({'Camera pivot','Camera fixed base','Camera PCB to rotating frame'})
            gh=[{'id':j['id'],'hits':{k:h for k,h in j['gauge_collisions'].items() if h}}
                for j in gauges['joints'] if any(j['gauge_collisions'].values())]
            row={'wheelbase_mm':wb,'tilt_deg':tilt,'recompute_errors':errors,
                 'valid_single_camera_solids':all(shapes[n].isValid() and len(shapes[n].Solids)==1 for n in camera),
                 'camera_part_intersections':hits,'camera_fastener_gauge_hits':gh,
                 'camera_shaft_pair_hits':gauges['screw_shaft_pair_collisions']}
            results.append(row)
            print(wb,tilt,'part hits',len(hits),'fastener hits',len(gh),flush=True)
finally:
    sheet.set(wbcell,original[0]);sheet.set(tiltcell,original[1]);doc.recompute()
passed=all(not r['recompute_errors'] and r['valid_single_camera_solids'] and not r['camera_part_intersections']
           and not r['camera_fastener_gauge_hits'] and not r['camera_shaft_pair_hits'] for r in results)
report={'status':'PASS nominal camera CAD/gauges' if passed else 'FAIL',
        'default_tilt_deg':-15,'nominal_tilt_range_deg':[-20,30],
        'gauge_dimensions':GAUGE,'poses':results,
        'limits':'Sampled angles only; physical hardware, FFC bends, lens package, print strength, detailed Nano and real propeller clearance remain unverified. Other frame screw defects remain.'}
(ROOT/'camera_mount_checks.json').write_text(json.dumps(report,indent=2)+'\n')
if not passed:raise RuntimeError('Camera checks failed; see camera_mount_checks.json')
print(report['status'],flush=True)
