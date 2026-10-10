"""Complete provisional attachment interfaces and save live FreeCAD artifacts."""
from pathlib import Path
import FreeCAD as App, FreeCADGui as Gui, Part
import csv, json, math
ROOT=Path('/home/kyo/ws/orion'); doc=App.getDocument('ORION_Frame')
# This follow-up uses the native source objects created by build_orion.py.

def replace_fuse_with_cut(name,g,tools):
    old=doc.getObject(name); sources=list(old.Shapes)
    label,color,qty=old.Label,old.ViewObject.ShapeColor,old.PrintQuantity
    uncut=fuse(g,name+'AttachmentBlank',sources)
    doc.removeObject(name)
    result=cut(g,name,uncut,tools)
    finish(result,label,color,qty)
    return result

center_add=[]
# GPS attaches independently from below; the proposed 3 mm pilot is not a verified insert interface.
gps_tools=[]
for sy in [-1,1]:
    gps_tools.append(cyl(gps,'GPSFastenerPilot',.85,4,-35.5,sy*6,0))
    center_add.append(cyl(center,'GPSBaseBolt','Parameters.m2_clearance_mm / 2',7,-35.5,sy*6,-4))
# Strap retention at module ends leaves the central 12×12 antenna sky zone open.
for sx in [-1,1]: gps_tools.append(box(gps,'GPSRetentionSlot',1,10,4,'Parameters.gps_center_x_mm'+f' + {sx*7.4} mm - 0.5 mm',-5,25))
gps_final=replace_fuse_with_cut('GPSMountSolid',gps,gps_tools)

imu_tools=[]
for sx in [-1,1]:
    imu_tools.append(cyl(imu,'IMUFastenerPilot',.85,4,sx*14,0,-7))
    center_add.append(cyl(center,'IMUBaseBolt','Parameters.m2_clearance_mm / 2',7,sx*14,0,-4))
for sy in [-1,1]: imu_tools.append(box(imu,'IMURetentionSlot',6,1.4,4,-3,sy*5.5-.7,-14))
imu_final=replace_fuse_with_cut('IMUMountSolid',imu,imu_tools)

# Move power mounting columns outside the nominated component envelope.
for sy,name in zip([-1,1],['PowerPost','PowerPost001']):
    o=doc.getObject(name); o.Length=4; o.Width=4
    o.Placement.Base=App.Vector(-23,sy*12-2,-13)
power_tools=[]
for sy in [-1,1]:
    power_tools.append(cyl(power,'PowerFastenerPilot',.85,4,-21,sy*12,-7))
    center_add.append(cyl(center,'PowerBaseBolt','Parameters.m2_clearance_mm / 2',7,-21,sy*12,-4))
    power_tools.append(box(power,'PowerRetentionSlot',6,1.4,4,-31,sy*5.5-.7,-14))
power_final=replace_fuse_with_cut('PowerMountSolid',power,power_tools)

# Skid screws remain accessible outside the Nano holder footprint.
landing_tools=[]
for sx in [-1,1]: landing_tools.append(cyl(ls,'LandingFastenerPilot',.85,4,sx*10,0,-7))
# Existing links are redirected to the revised native source.
old=doc.LandingSkidSolid; base=fuse(ls,'LandingSkidAttachmentBlank',list(old.Shapes))
landing_new=finish(cut(ls,'LandingSkidRevised',base,landing_tools),'LANDING SKID · detachable / below payload',COL_FRAME,2)
for sy,name in zip([-1,1],['LandingSkidN1','LandingSkid1']):
    link=doc.getObject(name); link.setLink(landing_new); link.LinkPlacement.Base=App.Vector(0,sy*30,0)
    for sx in [-1,1]: center_add.append(cyl(center,'LandingBaseBolt','Parameters.m2_clearance_mm / 2',7,sx*10,sy*30,-4))
# Keep old feature as the intermediate, hidden source rather than duplicate print geometry.
old.ViewObject.Visibility=False; landing_new.ViewObject.Visibility=False

# Camera base and pivot stack: two 1.8 mm outer ears plus the 2 mm moving ear.
for sy,name in zip([-1,1],['CameraFixedEar','CameraFixedEar001']):
    ear=doc.getObject(name); ear.Height=1.8; ear.Placement.Base.y=sy*18-.9
# Pivot cutting tools traverse the relocated ears.
for sy,name in zip([-1,1],['CameraFixedPivot','CameraFixedPivot001']):
    doc.getObject(name).Height=7; doc.getObject(name).Placement.Base.y=sy*18-3.5
cam_extra=[]
for sy in [-1,1]:
    cam_extra.append(cyl(fixed,'CameraBaseBolt','Parameters.m2_clearance_mm / 2',5,35,sy*19,-1))
    center_add.append(cyl(center,'CameraCenterBolt','Parameters.m2_clearance_mm / 2',7,35,sy*19,-4))
    center_add.append(cyl(center,'CameraCenterNutSeat',2.45,1.5,35,sy*19,-3))
doc.CameraBaseSolid.Tool.Shapes=list(doc.CameraBaseSolid.Tool.Shapes)+cam_extra

# A relief over each outside arm nut keeps arm-joint service independent of Nano retention.
p4_relief=[]
for theta in [45,135,225,315]:
    x,y=38*math.cos(math.radians(theta)),38*math.sin(math.radians(theta))
    p4_relief.append(cyl(p4,'P4ArmNutRelief',2.6,3,x,y,0))
doc.P4HolderSolid.Tool.Shapes=list(doc.P4HolderSolid.Tool.Shapes)+p4_relief
doc.CenterBaseSolid.Tool.Shapes=list(doc.CenterBaseSolid.Tool.Shapes)+center_add

doc.recompute()
master_names=['ArmSolid','CenterBaseSolid','P4HolderSolid','ESCHolderSolid','BatteryCradleSolid','GPSMountSolid','IMUMountSolid','PowerMountSolid','CameraFrameSolid','CameraBaseSolid','LandingSkidRevised','CouponSolid']
for name in master_names:
    o=doc.getObject(name)
    if o.Shape.isNull() or not o.Shape.isValid() or len(o.Shape.Solids)!=1:
        raise RuntimeError('Invalid printable source: '+name)
for name in ['ArmSolid','ESCHolderSolid','LandingSkidSolid','LandingSkidRevised','CouponSolid']:
    doc.getObject(name).ViewObject.Visibility=False
for groupname in ['MasterArm','MasterESCHolder','MasterLandingSkid']:
    for o in doc.getObject(groupname).Group: o.ViewObject.Visibility=False
for name in ['GPSMountSolid','IMUMountSolid','PowerMountSolid','CameraBaseSolid','P4HolderSolid']:
    doc.getObject(name).ViewObject.Visibility=True
Gui.Selection.clearSelection(); Gui.activeDocument().activeView().fitAll(); doc.recompute(); doc.save()
print('Final attachment interfaces recomputed; all 12 printable sources are valid single solids.')
