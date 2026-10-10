"""Export provisional meshes and view evidence from the native live model."""
from pathlib import Path
import FreeCAD as App, FreeCADGui as Gui
import MeshPart, json, csv, math
ROOT=Path('/home/kyo/ws/orion'); doc=App.getDocument('ORION_Frame')
export_dir=ROOT/'export'/'prototypes'; export_dir.mkdir(parents=True,exist_ok=True)
source_map=[
('ORION_arm','ArmSolid',4),('ORION_center_base','CenterBaseSolid',1),
('ORION_p4_holder','P4HolderSolid',1),('ORION_esc_holder','ESCHolderSolid',4),
('ORION_battery_mount','BatteryCradleSolid',1),('ORION_gps_mount','GPSMountSolid',1),
('ORION_imu_mount','IMUMountSolid',1),('ORION_power_mount','PowerMountSolid',1),
('ORION_camera_mount','CameraFrameSolid',1),('ORION_camera_base_mount','CameraBaseSolid',1),
('ORION_landing_skid','LandingSkidRevised',2),('ORION_tolerance_coupon','CouponSolid',1)]
manifest={'status':'FIT PROTOTYPES ONLY · relevant measurements unresolved','freecad_version':'.'.join(App.Version()[:3]),'linear_deflection_mm':0.1,'angular_deflection_rad':0.25,'print_orientation':'TBD; export translated to nonnegative local bounds','parts':[]}
for stem,name,quantity in source_map:
    obj=doc.getObject(name); shape=obj.Shape.copy()
    if shape.isNull() or not shape.isValid() or len(shape.Solids)!=1:
        raise RuntimeError('Invalid source '+name)
    bb=shape.BoundBox
    offset=App.Vector(-bb.XMin,-bb.YMin,-bb.ZMin)
    shape.translate(offset)
    mesh=MeshPart.meshFromShape(Shape=shape,LinearDeflection=0.1,AngularDeflection=0.25,Relative=False)
    if not mesh.isSolid(): raise RuntimeError('Mesh is not closed: '+name)
    target=export_dir/(stem+'.stl'); mesh.write(str(target))
    bounds=shape.BoundBox
    manifest['parts'].append({'file':str(target.relative_to(ROOT)),'source_object':name,'print_quantity':quantity,'valid_single_cad_solid':True,'closed_mesh':True,'facets':mesh.CountFacets,'cad_volume_mm3':round(shape.Volume,4),'bounds_mm':[round(bounds.XLength,3),round(bounds.YLength,3),round(bounds.ZLength,3)],'translation_mm':[offset.x,offset.y,offset.z]})
(export_dir/'manifest.json').write_text(json.dumps(manifest,indent=2))

# Measurement records preserve supplied values, proposed CAD revisions and TBDs.
for values in [('battery_mass_g','26.1 g','Specified','SPEC §2.2; pack excludes straps and free connector support'),('esc_mass_g','9 g','Specified','SPEC §2.2; each supplied ESC'),('prop_mass_g','0.8 g','Specified','SPEC §2.2; each prop'),('motor_mass_g','4.8 g','Specified','S3 manufacturer motor including wires'),('gps_mass_g','2.4 g','Specified','S5 nominal candidate GPS mass'),('printed_frame_mass_g','TBD','TBD','Actual scale measurement required'),('nano_mass_g','TBD','TBD','Actual populated board mass required'),('assembled_cg_x_mm','TBD','TBD','Measured balance required'),('assembled_cg_y_mm','TBD','TBD','Measured balance required')]:
    parameter(*values)
for record in rows:
    if record['alias'].endswith('_g'): record['units']='g'
with (ROOT/'measurements.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)

checks=doc.Checks
check_rows=[
('FreeCAD','1.1.3','Local instance through MCP'),
('190 mm motor-axis error','0 mm','Exact true-X formulas; see cad_checks.json'),
('180 / 190 / 200 recompute','PASS','Native single-solid sources; no broken dependencies'),
('Printed-part collisions','PASS','All three evaluated wheelbases'),
('Specified/proposed envelopes','PASS','Current nominated component boxes; actual solder/headers TBD'),
('Nano STEP vs printed parts','See cad_checks.json','Detailed manufacturer reference check'),
('Nominal prop sweep','PASS','10 mm center / 4 mm sweep are unmeasured layout surrogates'),
('Final prop sweep','UNRESOLVED','Measured height, sweep, flex and safe motor insertion depth required'),
('Wi-Fi CAD anchor','Derived','15 mm inflated actual STEP antenna copper bounds'),
('Wi-Fi added components','PASS','Current nominated boxes'),
('Wi-Fi conductive hardware','UNRESOLVED','Some candidate fastener locations lie in keepout'),
('Physical fits / mass / CG','TBD','No hardware or print measurements were performed'),
('Prototype meshes','12 closed meshes','Each maps to a native editable source; references excluded'),
('M2×6 candidate BOM','62 / +50 to purchase','Provisional plan; 12 M2×4 remain spares')]
for r,(a,b,c) in enumerate(check_rows,6):
    checks.set('A'+str(r),a); checks.set('B'+str(r),b); checks.set('C'+str(r),c)

# View changes are restored after the evidence set is captured.
shots=ROOT/'screenshots'; shots.mkdir(exist_ok=True)
original_visibility={o.Name:o.ViewObject.Visibility for o in doc.Objects if hasattr(o,'ViewObject')}
view=Gui.activeDocument().activeView()
def capture(name,orientation):
    getattr(view,orientation)(); view.fitAll(); Gui.updateGui()
    view.saveImage(str(shots/(name+'.png')),1600,1200,'White')
Gui.Selection.clearSelection()
for name,orientation in [('isometric','viewAxonometric'),('top','viewTop'),('bottom','viewBottom'),('side','viewFront')]: capture(name,orientation)
# Expose underside retention and electronics for inspection.
for o in prop_disks: o.ViewObject.Visibility=False
capture('underside_holders','viewBottom')
# Service reservations and actual antenna keepout.
for name in ['NanoFrontService','NanoRearService','NanoSDService','BatteryConnectorService','WiFiAntennaKeepout']:
    doc.getObject(name).ViewObject.Visibility=True
capture('port_access','viewAxonometric')
for name in ['NanoFrontService','NanoRearService','NanoSDService','BatteryConnectorService','WiFiAntennaKeepout']:
    doc.getObject(name).ViewObject.Visibility=False
for i in range(4): doc.getObject('ExpandedPropSweep'+str(i)).ViewObject.Visibility=True
capture('clearance_top','viewTop'); capture('clearance_side','viewFront')
for i in range(4): doc.getObject('ExpandedPropSweep'+str(i)).ViewObject.Visibility=False
# Exploded printed-parts-only illustration. Restore placements even on failure.
assembly_names=['CenterBaseSolid','P4HolderSolid','BatteryCradleSolid','GPSMountSolid','IMUMountSolid','PowerMountSolid','CameraFrameSolid','CameraBaseSolid']+[o.Name for o in doc.Objects if o.TypeId=='App::Link']
placements={}
try:
    for o in doc.Objects:
        if hasattr(o,'ViewObject') and o.Name in original_visibility: o.ViewObject.Visibility=False
    for name in assembly_names:
        o=doc.getObject(name); o.ViewObject.Visibility=True
        if name.startswith('Arm_') or name.startswith('ESCTray_'):
            placements[name]=o.LinkPlacement
            p=o.LinkPlacement
            direction=p.Rotation.multVec(App.Vector(1,0,0))
            p.Base=direction*22+App.Vector(0,0,-12 if name.startswith('ESC') else 0); o.LinkPlacement=p
        elif name.startswith('LandingSkid'):
            placements[name]=o.LinkPlacement; p=o.LinkPlacement; p.Base.z-=25; o.LinkPlacement=p
        elif name in ['P4HolderSolid','BatteryCradleSolid','GPSMountSolid','IMUMountSolid','PowerMountSolid']:
            placements[name]=o.Placement; p=o.Placement
            p.Base.z+=35 if name in ['P4HolderSolid','GPSMountSolid'] else -25; o.Placement=p
        elif name in ['CameraFrameSolid','CameraBaseSolid']:
            placements[name]=o.Placement; p=o.Placement; p.Base.x+=30; o.Placement=p
    doc.recompute(); capture('exploded_printed_parts','viewAxonometric')
finally:
    for name,p in placements.items():
        o=doc.getObject(name)
        if o.TypeId=='App::Link': o.LinkPlacement=p
        else: o.Placement=p
    for name,state in original_visibility.items():
        o=doc.getObject(name)
        if o is not None: o.ViewObject.Visibility=state
    doc.recompute()
    view.viewAxonometric(); view.fitAll(); doc.save()
print('Exported',len(manifest['parts']),'closed prototype meshes and screenshots; saved',doc.FileName)
