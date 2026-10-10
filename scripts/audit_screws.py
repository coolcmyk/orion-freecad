"""Geometric audit in FreeCAD Python. Caller supplies doc; never saves the CAD.

The head/nut dimensions below are explicit audit gauges, not measured hardware.
No printed pilot hole is treated as a verified thread or heat-set insert seat.
"""
from pathlib import Path
import FreeCAD as App
import Part
import json, math, itertools

ROOT = Path(__file__).resolve().parents[1]
GAUGE = {'shaft_diameter_mm': 2, 'under_head_length_mm': 6,
         'head_diameter_mm': 4.6, 'head_height_mm': 2,
         'nut_across_flats_mm': 4.156922, 'nut_height_mm': 1.6,
         'driver_diameter_mm': 3, 'driver_access_length_mm': 12}

def world(obj):
    s = obj.Shape.copy()
    if hasattr(obj, 'getGlobalPlacement'):
        s.Placement = obj.getGlobalPlacement().multiply(obj.Placement.inverse()).multiply(s.Placement)
    return s

def vec(v):
    return [round(x, 6) for x in (v.x, v.y, v.z)]

def overlap(a, b):
    return a.common(b).Volume if a.BoundBox.intersect(b.BoundBox) else 0.0

def primitive_points(prefix):
    return sorted([o for o in doc.Objects if o.Name.startswith(prefix)], key=lambda o:o.Name)

def audit_variant(categories=None):
    parts = ['CenterBaseSolid', 'P4HolderSolid', 'BatteryCradleSolid', 'GPSMountSolid',
             'IMUMountSolid', 'PowerMountSolid', 'CameraFrameSolid', 'CameraBaseSolid']
    parts += [o.Name for o in doc.Objects if o.TypeId == 'App::Link']
    shapes = {n:world(doc.getObject(n)) for n in parts if doc.getObject(n)}
    components = {n:world(doc.getObject(n)) for n in
                  ['BatteryEnvelope','GPSEnvelope','IMUEnvelope','PowerPackageProposed',
                   'CameraPCBReference','CameraLensProposed'] + ['ESCEnvelope'+str(i) for i in range(4)] if doc.getObject(n)}
    if doc.getObject('CameraGReconstruction'):
        for name in ['CameraGPCB','CameraGSensorHousing','CameraGLensShoulder','CameraGFisheyeBarrel',
                     'CameraGFocusRim','CameraGOpticalFace','CameraGRearFFC','CameraGFFCLatch']:
            components[name]=world(doc.getObject(name))
    joints = []
    def add(name, category, p, axis, owners, nut=None, pilot=False, note='', nut_rotation=None):
        if categories is not None and category not in categories:
            return
        axis.normalize()
        end = p + axis * 6
        shaft = Part.makeCylinder(1, 6, p, axis)
        head = Part.makeCylinder(2.3, 2, p-axis*2, axis)
        driver = Part.makeCylinder(1.5, 12, p-axis*14, axis)
        gauges = {'shaft':shaft, 'head':head, 'driver':driver}
        if nut is not None:
            vertices=[App.Vector(2.4*math.cos(i*math.pi/3),2.4*math.sin(i*math.pi/3),0) for i in range(6)]
            hexnut=Part.Face(Part.makePolygon(vertices+[vertices[0]])).extrude(App.Vector(0,0,1.6))
            hexnut.Placement=App.Placement(nut,nut_rotation or App.Rotation(z,axis))
            gauges['nut_hex_gauge'] = hexnut
        hits = {}
        for label, gauge in gauges.items():
            hit = []
            for pn, shape in shapes.items():
                if label == 'shaft' and pilot and pn in owners and pn != 'CenterBaseSolid':
                    continue  # Intentional undersize pilot; no verified thread.
                vol = overlap(gauge, shape)
                if vol > 1e-4:
                    hit.append({'part':pn, 'overlap_mm3':round(vol,5)})
            for cn, shape in components.items():
                vol = overlap(gauge,shape)
                if vol > 1e-4:
                    hit.append({'component':cn,'overlap_mm3':round(vol,5)})
            hits[label] = hit
        joints.append({'id':name,'category':category,'head_bearing_point_mm':vec(p),
                       'axis':vec(axis),'tip_mm':vec(end),'owners':owners,
                       'pilot_thread_unverified':pilot,'gauge_collisions':hits,'note':note,
                       '_shaft':shaft,'_head':head,'_gauges':gauges})
    z = App.Vector(0,0,1)
    for ai,an in enumerate(['Arm_FL','Arm_RL','Arm_RR','Arm_FR']):
        placement=doc.getObject(an).LinkPlacement
        for j in range(4):
            p=doc.getObject('MotorBolt'+str(j)).Placement.Base
            add(f'motor_{ai}_{j}','Motor mounts',placement.multVec(App.Vector(p.x,p.y,-7)),z,[an],
                note='2 mm nominal motor engagement; real threads, head size and safe depth unknown')
        for j,r in enumerate([30,38]):
            p=placement.multVec(App.Vector(r,0,-5))
            add(f'arm_{ai}_{j}','Keyed arm joints',p,z,[an,'CenterBaseSolid'],
                nut=placement.multVec(App.Vector(r,0,-1.2)),
                note='Nut pocket 1.2 mm deep; gauge nut projects 0.4 mm above plate')
        for j,o in enumerate(primitive_points('ESCArmHole')):
            p=placement.multVec(App.Vector(o.Placement.Base.x,0,-5))
            add(f'esc_{ai}_{j}','ESC holder to arm',p,-z,[an,'ESCTray_'+str(ai)],
                nut=placement.multVec(App.Vector(o.Placement.Base.x,0,-9)),
                note='Square open nut cavity has no verified captive-nut retention')
    for i,o in enumerate(primitive_points('P4BoardBolt')):
        p=o.Placement.Base
        add(f'nano_board_{i}','Nano PCB to holder',App.Vector(p.x,p.y,9.6),-z,['P4HolderSolid'],
            nut=App.Vector(p.x,p.y,6),note='Preload nut from below before mounting holder; center blocks underside access')
    for i,o in enumerate(primitive_points('P4TabHole')):
        p=o.Placement.Base
        add(f'nano_holder_{i}','Nano holder to center',App.Vector(p.x,p.y,2),-z,['P4HolderSolid','CenterBaseSolid'],
            nut=App.Vector(p.x,p.y,-1.5),note='Circular recess cannot lock hex nut against rotation')
    for category,prefix,owner,seat,axis in [
        ('Battery cradle to center','CenterBatteryBolt','BatteryCradleSolid',0,-z),
        ('GPS support','GPSBaseBolt','GPSMountSolid',-3,z),
        ('IMU support','IMUBaseBolt','IMUMountSolid',0,-z),
        ('Power support','PowerBaseBolt','PowerMountSolid',0,-z),
        ('Landing skids','LandingBaseBolt',None,0,-z)]:
        for i,o in enumerate(primitive_points(prefix)):
            p=o.Placement.Base
            own=owner or ('LandingSkidN1' if p.y<0 else 'LandingSkid1')
            add(prefix+'_'+str(i),category,App.Vector(p.x,p.y,seat),axis,[own,'CenterBaseSolid'],pilot=True,
                note='3 mm nominal penetration into 1.7 mm pilot; thread/insert design unverified')
    cp=doc.CameraTiltAssembly.getGlobalPlacement()
    for i,o in enumerate(primitive_points('CameraBoardBolt')):
        p=o.Placement.Base
        add('camera_board_'+str(i),'Camera PCB to rotating frame',cp.multVec(App.Vector(1.6,p.y,p.z)),
            cp.Rotation.multVec(App.Vector(-1,0,0)),['CameraFrameSolid'],
            nut=cp.multVec(App.Vector(-2,p.y,p.z)),note='PCB thickness and spacer/head/component clearances unmeasured')
    for i,sign in enumerate([-1,1]):
        axis=App.Vector(0,-sign,0)
        suffix='' if i==0 else '001'
        ear=doc.getObject('CameraFixedEar'+suffix)
        boss=doc.getObject('CameraPivotBoss'+suffix)
        ey=ear.Placement.Base.y+(float(ear.Height) if sign>0 else 0)
        by=boss.Placement.Base.y+(float(boss.Height) if sign<0 else 0)
        head=App.Vector(cp.Base.x,ey,cp.Base.z)
        nut=App.Vector(cp.Base.x,by,cp.Base.z)
        grip=abs(ey-by)
        add('camera_pivot_'+str(i),'Camera pivot',head,axis,
            ['CameraFrameSolid','CameraBaseSolid'],nut=nut,
            nut_rotation=cp.Rotation.multiply(App.Rotation(z,axis)),
            note=f'{grip:.3f} mm bearing-to-nut distance; {6-grip-1.6:.3f} mm tip allowance with 1.6 mm gauge nut')
    for i,o in enumerate(primitive_points('CameraBaseBolt')):
        p=o.Placement.Base
        add('camera_base_'+str(i),'Camera fixed base',App.Vector(p.x,p.y,2),-z,
            ['CameraBaseSolid','CenterBaseSolid'],nut=App.Vector(p.x,p.y,-1.5),
            note='Circular nut recess needs physical retention verification; gauge collisions recorded separately')
    pairs=[]
    for a,b in itertools.combinations(joints,2):
        vol=overlap(a['_shaft'],b['_shaft'])
        if vol>1e-4:
            pairs.append({'a':a['id'],'b':b['id'],'shaft_overlap_mm3':round(vol,5)})
    for j in joints:
        del j['_shaft']; del j['_head']; del j['_gauges']
    return {'quantity':len(joints),'joints':joints,'screw_shaft_pair_collisions':pairs,
            'excluded_checks':['Real hardware dimensions and thread strength',
                'Detailed Nano STEP hardware boolean intersections: separate attempt exceeded 180 s; not established',
                'Actual motor thread geometry','Flexible cables and assembly hand/tool ergonomics',
                'Wi-Fi conductive hardware acceptance; existing keepout remains unresolved']}

report={'status':'FAIL: assembly defects found; not manufacturing ready',
        'gauge_dimensions':GAUGE,'gauge_warning':'Hypothetical hardware gauges; do not infer purchased hardware dimensions',
        'source_document':doc.FileName,'variants':[],
        'nut_gauge_note':'Solid hexagonal fit gauge at one orientation; actual nut bore, chamfers and tolerances excluded'}
cell=doc.Parameters.getCellFromAlias('wheelbase_mm')
original=doc.Parameters.getContents(cell)
try:
    for wb in [180,190,200]:
        doc.Parameters.set(cell,str(wb)+' mm'); doc.recompute()
        v=audit_variant(); v['wheelbase_mm']=wb
        report['variants'].append(v)
        print('wheelbase',wb,'joints',v['quantity'],'shaft pairs',v['screw_shaft_pair_collisions'],flush=True)
finally:
    doc.Parameters.set(cell,original); doc.recompute()
(ROOT/'screw_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print('Saved screw_audit.json',flush=True)
