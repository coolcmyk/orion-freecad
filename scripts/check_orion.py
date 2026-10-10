"""Verify live native geometry; report provisional CAD and unresolved fit checks."""
from pathlib import Path
import FreeCAD as App, FreeCADGui as Gui, Part
import json, math, itertools
ROOT=Path('/home/kyo/ws/orion')
doc=App.getDocument('ORION_Frame'); sheet=doc.Parameters
aliases={}
for r in range(2,300):
    alias=sheet.getContents('A'+str(r))
    if alias: aliases[alias]=r

def world(obj):
    shape=obj.Shape.copy()
    if hasattr(obj,'getGlobalPlacement'):
        shape.Placement=obj.getGlobalPlacement().multiply(obj.Placement.inverse()).multiply(shape.Placement)

    return shape

def intersection(a,b):
    if not a.BoundBox.intersect(b.BoundBox): return 0.0
    return a.common(b).Volume

master_names=['ArmSolid','CenterBaseSolid','P4HolderSolid','ESCHolderSolid','BatteryCradleSolid','GPSMountSolid','IMUMountSolid','PowerMountSolid','CameraFrameSolid','CameraBaseSolid','LandingSkidRevised','CouponSolid']
assembly_names=['CenterBaseSolid','P4HolderSolid','BatteryCradleSolid','GPSMountSolid','IMUMountSolid','PowerMountSolid','CameraFrameSolid','CameraBaseSolid']+[o.Name for o in doc.Objects if o.TypeId=='App::Link']
report={'freecad_version':'.'.join(App.Version()[:3]),'spec_revision':'0.3','release_status':'FIT PROTOTYPE / measured interfaces unresolved','shape_checks':[],'variants':[]}
for name in master_names:
    obj=doc.getObject(name); s=obj.Shape
    report['shape_checks'].append({'object':name,'valid':not s.isNull() and s.isValid(),'solids':len(s.Solids),'volume_mm3':round(s.Volume,3)})

for W in [180,190,200]:
    sheet.set('B'+str(aliases['wheelbase_mm']),f'{W} mm'); doc.recompute()
    errors=[{'object':o.Name,'status':o.getStatusString()} for o in doc.Objects if 'Invalid' in o.State or 'Error' in o.State]
    invalid=[name for name in master_names if doc.getObject(name).Shape.isNull() or not doc.getObject(name).Shape.isValid()]
    shapes={n:world(doc.getObject(n)) for n in assembly_names}
    props=[world(doc.getObject('ExpandedPropSweep'+str(i))) for i in range(4)]
    prop_hits=[]
    for name,s in shapes.items():
        for i,p in enumerate(props):
            volume=intersection(s,p)
            if volume>1e-5: prop_hits.append({'part':name,'prop':i,'overlap_mm3':round(volume,5)})
    mutual=[round(intersection(a,b),6) for a,b in itertools.combinations(props,2)]
    axes=[]
    for i,(sx,sy) in enumerate([(1,1),(-1,1),(-1,-1),(1,-1)]):
        pos=doc.getObject('MotorBody'+str(i)).Placement.Base
        expected=App.Vector(sx*W/(2*math.sqrt(2)),sy*W/(2*math.sqrt(2)),-3)
        axes.append({'motor':i,'x_mm':round(pos.x,6),'y_mm':round(pos.y,6),'position_error_mm':round((pos-expected).Length,9)})
    part_hits=[]
    for (na,a),(nb,b) in itertools.combinations(shapes.items(),2):
        volume=intersection(a,b)
        if volume>1e-4: part_hits.append({'a':na,'b':nb,'overlap_mm3':round(volume,5)})
    components=[]
    # CAD component envelopes are specified/proposed as recorded; the STEP is checked separately.
    envnames=['BatteryEnvelope','GPSEnvelope','IMUEnvelope','PowerPackageProposed']+['ESCEnvelope'+str(i) for i in range(4)]+['CameraPCBReference','CameraLensProposed']
    for en in envnames:
        envelope=world(doc.getObject(en))
        for pn,shape in shapes.items():
            volume=intersection(envelope,shape)
            if volume>1e-4: components.append({'component':en,'part':pn,'overlap_mm3':round(volume,5)})
    report['variants'].append({'wheelbase_mm':W,'recompute_errors':errors,'invalid_shapes':invalid,'axes':axes,'prop_mutual_overlap_mm3':mutual,'printed_part_prop_intersections':prop_hits,'printed_part_intersections':part_hits,'component_intersections':components,'nominal_prop_check':'PASS' if not prop_hits and not any(mutual) else 'FAIL','final_prop_clearance':'UNRESOLVED: prop_plane_z_mm and prop_sweep_thickness_mm are TBD'})
    print('Variant',W,'recompute errors',len(errors),'prop hits',len(prop_hits),'printed collisions',len(part_hits),'component collisions',len(components))
sheet.set('B'+str(aliases['wheelbase_mm']),'190 mm'); doc.recompute()
(ROOT/'cad_checks.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report['variants'][1],indent=2))
doc.save()
