"""Native camera reference from Waveshare's shared DWG plus labeled depth estimates.

Run via FreeCAD MCP with `assembly_doc` supplied. This is not manufacturer 3D CAD.
"""
from pathlib import Path
import FreeCAD as App, FreeCADGui as Gui, Part, Import
import json

ROOT=Path('/home/kyo/ws/orion')
ASSET=ROOT/'references'/'camera_g_reconstructed'
ASSET.mkdir(exist_ok=True)
ROWS=[
 ('pcb_width',25,'Specified','DWG outer rectangle'),
 ('pcb_height',24,'Specified','DWG outer rectangle'),
 ('mount_hole_diameter',2.2,'Specified','DWG four mounting circles'),
 ('lens_mount_hole_diameter',1.8,'Specified','DWG two internal mounting circles'),
 ('optical_u',12.5,'Derived','DWG circle center relative to board origin'),
 ('optical_v',15.65,'Specified','DWG optical center to lower board edge'),
 ('sensor_footprint',8.5,'Specified','Shared DWG central square; not full Type G barrel outline'),
 ('pcb_thickness',1.6,'Proposed','No side view in DWG; measure purchased PCB'),
 ('sensor_height',2,'Proposed','No height in DWG'),
 ('barrel_diameter',18,'Proposed','Retained ORION fisheye envelope; not the DWG 18 mm hole spacing'),
 ('lens_depth',14,'Proposed','Retained ORION lens depth from front PCB surface'),
 ('connector_width',20.5,'Proposed','Photo-based packaging estimate; measure connector'),
 ('connector_height',3,'Proposed','Photo-based packaging estimate'),
 ('connector_depth',2.5,'Proposed','Rear connector depth estimate'),
 ('latch_depth',1,'Proposed','Rear latch depth estimate'),
]

def build(d,parent=None):
    root=d.addObject('App::Part','CameraGReconstruction')
    root.Label='Waveshare Type G · DWG reconstruction / provisional depths'
    if parent:parent.addObject(root)
    for prop,value in [('Source','Waveshare RPi_Camera_E_F_G_H_Mechanical.dwg'),
                       ('ReferenceStatus','NON-PRINTABLE reconstruction; full Type G lens and depths unmeasured')]:
        root.addProperty('App::PropertyString',prop,'Provenance');setattr(root,prop,value)
    sheet=d.addObject('Spreadsheet::Sheet','CameraGParameters');root.addObject(sheet)
    for col,text in [('A','Parameter'),('B','Value'),('C','Status'),('D','Source / limitation')]:sheet.set(col+'1',text)
    for i,(alias,value,status,source) in enumerate(ROWS,2):
        sheet.set('A'+str(i),alias);sheet.set('B'+str(i),str(value)+' mm');sheet.setAlias('B'+str(i),alias)
        sheet.set('C'+str(i),status);sheet.set('D'+str(i),source)
    sheet.ViewObject.Visibility=False
    finals=[]
    def primitive(kind,name,values,base,color,status='Proposed'):
        o=d.addObject(kind,name);root.addObject(o)
        for k,v in values.items():
            if isinstance(v,str):o.setExpression(k,v)
            else:setattr(o,k,v)
        o.Placement.Base=App.Vector(*base)
        o.addProperty('App::PropertyString','DimensionStatus','Provenance');o.DimensionStatus=status
        o.ViewObject.ShapeColor=color;o.ViewObject.LineColor=(.12,.12,.12)
        return o
    black=(.08,.085,.09);metal=(.66,.65,.6)
    board=primitive('Part::Box','CameraGBoardBlank',{'Length':'CameraGParameters.pcb_width','Width':'CameraGParameters.pcb_height','Height':'CameraGParameters.pcb_thickness'},(0,0,0),black,'Plan specified; thickness proposed')
    holes=[]
    points=[(2,8.5,1.1),(23,8.5,1.1),(2,22,1.1),(23,22,1.1),(3.5,15.65,.9),(21.5,15.65,.9)]
    for i,(u,v,r) in enumerate(points):
        o=primitive('Part::Cylinder','CameraGHole'+str(i),{'Radius':r,'Height':'CameraGParameters.pcb_thickness + 2 mm'},(u,v,-1),metal,'Specified DWG circle');holes.append(o)
    tool=d.addObject('Part::MultiFuse','CameraGHoleTools');root.addObject(tool);tool.Shapes=holes
    pcb=d.addObject('Part::Cut','CameraGPCB');root.addObject(pcb);pcb.Base=board;pcb.Tool=tool;pcb.Refine=True
    pcb.ViewObject.ShapeColor=black;finals.append(pcb)
    block=primitive('Part::Box','CameraGSensorHousing',{'Length':'CameraGParameters.sensor_footprint','Width':'CameraGParameters.sensor_footprint','Height':'CameraGParameters.sensor_height'},(8.25,11.4,1.6),black,'DWG square footprint; height proposed')
    block.setExpression('Placement.Base.z','CameraGParameters.pcb_thickness');finals.append(block)
    cone=primitive('Part::Cone','CameraGLensShoulder',{'Radius1':'CameraGParameters.barrel_diameter / 2 - 2 mm','Radius2':'CameraGParameters.barrel_diameter / 2','Height':2.5},(12.5,15.65,3.6),black)
    cone.setExpression('Placement.Base.z','CameraGParameters.pcb_thickness + CameraGParameters.sensor_height');finals.append(cone)
    barrel=primitive('Part::Cylinder','CameraGFisheyeBarrel',{'Radius':'CameraGParameters.barrel_diameter / 2','Height':'CameraGParameters.lens_depth - CameraGParameters.sensor_height - 3.3 mm'},(12.5,15.65,6.1),black)
    barrel.setExpression('Placement.Base.z','CameraGParameters.pcb_thickness + CameraGParameters.sensor_height + 2.5 mm');finals.append(barrel)
    ring=primitive('Part::Cylinder','CameraGFocusRingBlank',{'Radius':'CameraGParameters.barrel_diameter / 2','Height':.8},(12.5,15.65,14.8),black)
    ring.setExpression('Placement.Base.z','CameraGParameters.pcb_thickness + CameraGParameters.lens_depth - 0.8 mm')
    opening=primitive('Part::Cylinder','CameraGFocusOpening',{'Radius':'CameraGParameters.barrel_diameter / 2 - 1.5 mm','Height':2},(12.5,15.65,14.4),black)
    opening.setExpression('Placement.Base.z','CameraGParameters.pcb_thickness + CameraGParameters.lens_depth - 1.2 mm')
    rim=d.addObject('Part::Cut','CameraGFocusRim');root.addObject(rim);rim.Base=ring;rim.Tool=opening;rim.Refine=True;rim.ViewObject.ShapeColor=black;finals.append(rim)
    glass=primitive('Part::Cylinder','CameraGOpticalFace',{'Radius':'CameraGParameters.barrel_diameter / 2 - 1.7 mm','Height':.2},(12.5,15.65,15.2),(.08,.15,.21))
    glass.setExpression('Placement.Base.z','CameraGParameters.pcb_thickness + CameraGParameters.lens_depth - 0.4 mm');finals.append(glass)
    connector=primitive('Part::Box','CameraGRearFFC',{'Length':'CameraGParameters.connector_width','Width':'CameraGParameters.connector_height','Height':'CameraGParameters.connector_depth'},(2.25,.5,-2.5),(.8,.79,.69))
    connector.setExpression('Placement.Base.x','(CameraGParameters.pcb_width - CameraGParameters.connector_width) / 2')
    connector.setExpression('Placement.Base.z','0 mm - CameraGParameters.connector_depth');finals.append(connector)
    latch=primitive('Part::Box','CameraGFFCLatch',{'Length':'CameraGParameters.connector_width - 2 mm','Width':1,'Height':'CameraGParameters.latch_depth'},(3.25,.5,-3.5),(.2,.2,.2))
    latch.setExpression('Placement.Base.x','(CameraGParameters.pcb_width - CameraGParameters.connector_width) / 2 + 1 mm')
    latch.setExpression('Placement.Base.z','0 mm - CameraGParameters.connector_depth - CameraGParameters.latch_depth');finals.append(latch)
    d.recompute()
    for o in root.Group:
        if hasattr(o,'ViewObject'):o.ViewObject.Visibility=o in finals
    root.ViewObject.Visibility=True
    for o in finals:
        if not o.Shape.isValid() or len(o.Shape.Solids)!=1:raise RuntimeError('Invalid camera reference '+o.Name)
    return root,finals

camera_doc=App.newDocument('Waveshare_Camera_G')
asset,parts=build(camera_doc)
camera_doc.recompute();camera_doc.saveAs(str(ASSET/'Waveshare_Camera_G.FCStd'))
Import.export(parts,str(ASSET/'Waveshare_Camera_G.step'))
Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll()
Gui.activeDocument().activeView().saveImage(str(ASSET/'camera_g.png'),1200,1000,'White')

assembly_doc.openTransaction('Replace camera surrogate with DWG reconstruction')
try:
    asset_in_frame,assembly_parts=build(assembly_doc,assembly_doc.CameraReference)
    asset_in_frame.Placement=App.Placement(App.Vector(0,-12.5,-15.65),App.Rotation(App.Vector(1,1,1),120))
    for n in ['CameraPCBReference','CameraLensProposed']:
        assembly_doc.getObject(n).ViewObject.Visibility=False
    # Existing lower frame rails need a rear FFC service opening for the candidate connector.
    g=assembly_doc.CameraFrameSource
    relief=assembly_doc.addObject('Part::Box','CameraGRearFFCRelief');g.addObject(relief)
    relief.Length=5;relief.Width=22;relief.Height=4
    relief.Placement.Base=App.Vector(-4,-11,-15.5)
    relief.ViewObject.Visibility=False
    tool=assembly_doc.CameraFrameSolid.Tool;tool.Shapes=list(tool.Shapes)+[relief]
    assembly_doc.recompute()
    if not assembly_doc.CameraFrameSolid.Shape.isValid() or len(assembly_doc.CameraFrameSolid.Shape.Solids)!=1:
        raise RuntimeError('Rear cable relief invalidated camera frame')
    assembly_doc.commitTransaction()
except Exception:
    assembly_doc.abortTransaction();raise
report={'source':'RPi_Camera_E_F_G_H_Mechanical.dwg','asset':'Waveshare_Camera_G.FCStd',
        'classification':'Reconstructed reference, not official 3D CAD or a print part',
        'parameters':[dict(alias=a,value_mm=v,status=s,source=n) for a,v,s,n in ROWS],
        'holes':[
            dict(u_mm=u,v_mm=v,diameter_mm=diameter) for u,v,diameter in [(2,8.5,2.2),(23,8.5,2.2),(2,22,2.2),(23,22,2.2),(3.5,15.65,1.8),(21.5,15.65,1.8)]],
        'native_part_validity':{o.Name:o.Shape.isValid() for o in parts},
        'warning':'All depths, complete Type G barrel dimensions and connector packaging require actual measurement.'}
(ASSET/'provenance.json').write_text(json.dumps(report,indent=2)+'\n')
Gui.setActiveDocument(assembly_doc.Name)
assembly_doc.saveCopy('/tmp/orion-camera-g-reconstruction.FCStd')
print('Created standalone native FCStd and STEP; integrated non-printable camera reference and rear FFC relief into ORION.')
