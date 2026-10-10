"""Revise the native camera mount in an open ORION document via FreeCAD MCP.

Caller supplies doc. Hardware dimensions are fit-prototype gauges, not measurements.
"""
import FreeCAD as App
import Part

def obtain(kind,name,group):
    o=doc.getObject(name)
    if o is None:
        o=doc.addObject(kind,name);group.addObject(o)
    o.ViewObject.Visibility=False
    return o

def box(name,group,size,base):
    o=obtain('Part::Box',name,group)
    o.Length,o.Width,o.Height=size
    o.Placement=App.Placement(App.Vector(*base),App.Rotation())
    return o

doc.openTransaction('Camera forward-lean pose and accessible M2x6 joints')
try:
    sheet=doc.Parameters
    sheet.set(sheet.getCellFromAlias('camera_tilt_deg'),'=0 deg - 15 deg')
    sheet.set(sheet.getCellFromAlias('camera_pivot_z_mm'),'=20 mm')
    moving=doc.CameraFrameSource
    fixed=doc.CameraFixedSource
    additions=[]; tools=[]
    for i,sign in enumerate([-1,1]):
        suffix='' if i==0 else '001'
        boss=doc.getObject('CameraPivotBoss'+suffix)
        boss.Height=1.5;boss.Placement.Base=App.Vector(0,-18 if sign<0 else 16.5,0)
        additions.append(box('CameraNutBridge'+str(i),moving,(8,4,8),(-4,-18 if sign<0 else 14,-4)))
        pocket=obtain('Part::Prism','CameraPivotNutPocket'+str(i),moving)
        pocket.Polygon=6;pocket.Circumradius=2.55;pocket.Height=2.5
        pocket.Placement=App.Placement(App.Vector(0,sign*16.5,0),App.Rotation(App.Vector(0,0,1),App.Vector(0,-sign,0)))
        tools.append(pocket)
        # Open the pocket from above so the nut can be dropped in before the PCB.
        tools.append(box('CameraPivotNutEntry'+str(i),moving,(5.1,2.5,12),(-2.55,-16.5 if sign<0 else 14,0)))
        hole=doc.getObject('CameraPivotHole'+suffix)
        hole.Height=44;hole.Placement.Base=App.Vector(0,-22,0)
        ear=doc.getObject('CameraFixedEar'+suffix)
        ear.Height=1.8;ear.Placement.Base.y=-20 if sign<0 else 18.2
        ear.setExpression('Placement.Base.x','Parameters.camera_pivot_x_mm')
        ear.setExpression('Placement.Base.z','Parameters.camera_pivot_z_mm')
        upright=doc.getObject('CameraUpright'+suffix)
        upright.Width=1.8;upright.Placement.Base.y=-20 if sign<0 else 18.2
        upright.Placement.Base.x=39
        upright.setExpression('Height','Parameters.camera_pivot_z_mm')
        bar=doc.getObject('CameraCrossbar'+suffix)
        bar.Width=1.8;bar.Placement.Base.y=-20 if sign<0 else 18.2
        bar.Placement.Base.x=39;bar.Length=5
        bar.setExpression('Placement.Base.z','Parameters.camera_pivot_z_mm - 4 mm')
        pivot=doc.getObject('CameraFixedPivot'+suffix)
        pivot.Height=9;pivot.Placement.Base.y=-23 if sign<0 else 14
        pivot.setExpression('Placement.Base.x','Parameters.camera_pivot_x_mm')
        pivot.setExpression('Placement.Base.z','Parameters.camera_pivot_z_mm')
        foot=doc.getObject('CameraFoot'+suffix)
        foot.Length=13.5;foot.Placement.Base.x=29.5
        for prefix in ['CameraBaseBolt','CameraCenterBolt','CameraCenterNutSeat']:
            doc.getObject(prefix+suffix).Placement.Base.x=35
    union=doc.CameraFrameUnion
    union.Shapes=list(dict.fromkeys(list(union.Shapes)+additions))
    cuttools=doc.CameraFrameSolid.Tool
    cuttools.Shapes=list(dict.fromkeys(list(cuttools.Shapes)+tools))
    for name in ['CameraFrameSolid','CameraBaseSolid']:
        o=doc.getObject(name)
        for prop in ['SupportedTiltMin','SupportedTiltMax']:
            if prop not in o.PropertiesList:o.addProperty('App::PropertyAngle',prop,'Camera fit prototype')
        o.SupportedTiltMin=-20;o.SupportedTiltMax=30
        o.ReleaseStatus='FIT PROTOTYPE: revised camera joints; actual hardware and strength unverified'
    doc.CameraTiltAssembly.Label='CAMERA · forward lean / -20 to +30 deg nominal adjustment'
    doc.recompute()
    for name in ['CameraFrameSolid','CameraBaseSolid','CenterBaseSolid']:
        s=doc.getObject(name).Shape
        if s.isNull() or not s.isValid() or len(s.Solids)!=1:
            raise RuntimeError('Invalid revised solid: '+name)
    doc.commitTransaction()
except Exception:
    doc.abortTransaction()
    raise
print('Camera revised: -15 deg default, pivot Z=20 mm, 3.5 mm pivot grip, top-entry nut pockets, base screws X=35 mm with uprights at X=39 mm.')
