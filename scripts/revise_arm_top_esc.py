"""Replace side ESC fingers with arm-top ties and raised integral motor pads.
Caller supplies doc. Native geometry; dimensions are fit-prototype proposals.
"""
import FreeCAD as App
from pathlib import Path
ROOT=Path('/home/kyo/ws/orion')
doc.saveCopy('/tmp/orion-before-arm-top-esc.FCStd')
doc.openTransaction('Arm-top ESCs and raised integral motor pads')
try:
 sheet=doc.Parameters
 for r,(alias,value,note) in enumerate([
  ('esc_arm_radius_mm','67 mm','Proposed common ESC center from origin; clear Nano antenna'),
  ('motor_lift_mm','5 mm','Proposed raised integral pad; bottom screw wells preserve 4 mm grip'),
  ('esc_tie_allowance_mm','2 mm','Proposed clearance above ESC for ties/wires; actual leads TBD'),
 ],210):
  sheet.set('A'+str(r),alias);sheet.set('B'+str(r),value);sheet.setAlias('B'+str(r),alias)
  sheet.set('C'+str(r),'Proposed');sheet.set('D'+str(r),note)
 # Remove the earlier side fingers and restore the original center plate source.
 doc.CenterBaseSolid.Base=doc.CenterPlateBody
 doc.CenterBaseSolidTools.Shapes=[o for o in doc.CenterBaseSolidTools.Shapes if not o.Name.startswith('ESCTieSlot')]
 doc.removeObject('CenterPlateWithESCRetention')
 g=doc.TopESCRetention
 for o in list(g.Group):doc.removeObject(o.Name)
 doc.removeObject(g.Name)
 doc.CenterBaseSolid.Label='CENTER · no ESC side extensions / power tray'
 # Motors remain supported by the continuous original pad, increased upward.
 doc.MotorPad.setExpression('Height','Parameters.motor_mount_plate_mm + Parameters.motor_lift_mm')
 tools=[]
 for j in range(4):
  bolt=doc.getObject('MotorBolt'+str(j));bolt.Height=24
  c=doc.addObject('Part::Cylinder','MotorHeadWell'+str(j));doc.MasterArm.addObject(c)
  c.Radius=2.3;c.setExpression('Height','Parameters.motor_lift_mm + 1 mm')
  c.setExpression('Placement.Base.x',f'MotorBolt{j}.Placement.Base.x')
  c.setExpression('Placement.Base.y',f'MotorBolt{j}.Placement.Base.y')
  c.setExpression('Placement.Base.z','-Parameters.center_plate_thickness_mm - Parameters.motor_mount_plate_mm - 1 mm')
  c.ViewObject.Visibility=False;tools.append(c)
 doc.MotorShaftAccess.Height=24
 # Two ties per arm: opposing small through slots in the master arm beam.
 for i,dx in enumerate([-8,8]):
  for side in [-1,1]:
   c=doc.addObject('Part::Box',f'ArmESCTieSlot{i}_{"N" if side<0 else "P"}');doc.MasterArm.addObject(c)
   c.Length=2;c.Width=1.7;c.Height=12
   c.setExpression('Placement.Base.x',f'Parameters.esc_arm_radius_mm + {dx} mm - 1 mm')
   c.Placement.Base.y=side*2.5-.85;c.Placement.Base.z=-10
   c.ViewObject.Visibility=False;tools.append(c)
 doc.ArmSolidTools.Shapes=list(doc.ArmSolidTools.Shapes)+tools
 doc.ArmSolid.Refine=True;doc.ArmSolid.Label='ARM · top ESC ties / raised motor / recessed M2x6 seats'
 for i,angle in enumerate([45,135,225,315]):
  parent=doc.getObject('ESCReference'+str(i));parent.Placement=App.Placement(App.Vector(),App.Rotation(App.Vector(0,0,1),angle))
  o=doc.getObject('ESCEnvelope'+str(i))
  o.setExpression('Placement.Base.x','Parameters.esc_arm_radius_mm - Parameters.esc_length_mm / 2')
  o.setExpression('Placement.Base.y','-Parameters.esc_width_mm / 2')
  o.setExpression('Placement.Base.z','-Parameters.center_plate_thickness_mm + Parameters.esc_top_pad_mm')
  o.Label=f'ESC {i+1} · arm top / insulation / two ties'
  c=doc.addObject('Part::Box','ESCTieAllowance'+str(i));parent.addObject(c)
  c.setExpression('Length','Parameters.esc_length_mm');c.setExpression('Width','Parameters.esc_width_mm');c.setExpression('Height','Parameters.esc_tie_allowance_mm')
  c.setExpression('Placement.Base.x',f'ESCEnvelope{i}.Placement.Base.x');c.setExpression('Placement.Base.y',f'ESCEnvelope{i}.Placement.Base.y')
  c.setExpression('Placement.Base.z',f'ESCEnvelope{i}.Placement.Base.z + Parameters.esc_height_mm')
  c.ViewObject.ShapeColor=(0.9,0.7,0.25);c.ViewObject.Transparency=85;c.ViewObject.Visibility=False
  doc.getObject('MotorBody'+str(i)).setExpression('Placement.Base.z','-Parameters.center_plate_thickness_mm + Parameters.motor_lift_mm')
  doc.getObject('MotorShaft'+str(i)).setExpression('Placement.Base.z','-Parameters.center_plate_thickness_mm + Parameters.motor_lift_mm + Parameters.motor_body_height_mm')
  doc.getObject('PropDisk'+str(i)).setExpression('Placement.Base.z','Parameters.layout_prop_plane_z_mm + Parameters.motor_lift_mm - 0.3 mm')
  doc.getObject('ExpandedPropSweep'+str(i)).setExpression('Placement.Base.z','Parameters.layout_prop_plane_z_mm + Parameters.motor_lift_mm - Parameters.layout_prop_sweep_mm / 2 - Parameters.prop_vertical_clearance_mm')
 doc.recompute()
 errors=[o.Name for o in doc.Objects if 'Error' in o.State or 'Invalid' in o.State]
 assert not errors,errors
 for n in ['CenterBaseSolid','ArmSolid']:assert doc.getObject(n).Shape.isValid() and len(doc.getObject(n).Shape.Solids)==1,n
 doc.commitTransaction();doc.saveCopy('/tmp/orion-arm-top-esc-candidate.FCStd')
 print('Native arm-top ESC revision ready for independent checks.')
except:
 doc.abortTransaction();raise
