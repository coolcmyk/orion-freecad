"""Move IMU beneath GPS on a shared native tower; compact the battery drop.
Caller supplies doc. All new packaging and vertical gaps are provisional.
"""
import FreeCAD as App
from pathlib import Path
ROOT=Path('/home/kyo/ws/orion')
def box(name,group,size,base):
 o=doc.addObject('Part::Box',name);group.addObject(o)
 for prop,v in zip(['Length','Width','Height'],size):
  if isinstance(v,str):o.setExpression(prop,v)
  else:setattr(o,prop,v)
 for axis,v in zip(['x','y','z'],base):
  if isinstance(v,str):o.setExpression('Placement.Base.'+axis,v)
  else:setattr(o.Placement.Base,axis,v)
 o.ViewObject.Visibility=False;return o

doc.saveCopy('/tmp/orion-before-sensor-battery.FCStd')
doc.openTransaction('Shared GPS IMU tower and compact battery cradle')
try:
 sheet=doc.Parameters
 for r,(alias,value,note) in enumerate([
  ('imu_tray_z_mm','8 mm','Proposed shelf bottom near ESP PCB level; integrated GPS tower'),
  ('imu_isolation_pad_mm','0.5 mm','Proposed insulating/isolation pad; verify actual board/header height'),
  ('sensor_post_y_mm','14 mm','Proposed wider GPS posts clear rotated IMU'),
 ],220):
  sheet.set('A'+str(r),alias);sheet.set('B'+str(r),value);sheet.setAlias('B'+str(r),alias);sheet.set('C'+str(r),'Proposed');sheet.set('D'+str(r),note)
 sheet.set(sheet.getCellFromAlias('battery_cradle_z_mm'),'=0 mm - 22 mm')
 imu_bolts=[o for o in doc.Objects if o.Name.startswith('IMUBaseBolt')]
 doc.CenterBaseSolidTools.Shapes=[o for o in doc.CenterBaseSolidTools.Shapes if o not in imu_bolts]
 for o in imu_bolts:doc.removeObject(o.Name)
 old=doc.IMUMount
 for o in list(old.Group):doc.removeObject(o.Name)
 doc.removeObject(old.Name)
 gps=doc.GPSMount;gps.Label='GPS + IMU · shared two-level tower'
 base=doc.GPSMountSolid.Base
 additions=[]
 for i,sy in enumerate([-1,1]):
  suffix='' if i==0 else '001'
  doc.getObject('GPSPost'+suffix).setExpression('Placement.Base.y',f'{sy} * Parameters.sensor_post_y_mm - 2 mm')
  doc.getObject('GPSBaseBolt'+suffix).setExpression('Placement.Base.y',f'{sy} * Parameters.sensor_post_y_mm')
  doc.getObject('GPSFastenerPilot'+suffix).setExpression('Placement.Base.y',f'{sy} * Parameters.sensor_post_y_mm')
  additions.append(box('GPSTopBridge'+str(i),gps,[4,9.85,2],[-37.5,-16 if sy<0 else 6.15,'Parameters.gps_tray_z_mm']))
 floor=box('IMUTowerShelf',gps,[18.3,26,2],['Parameters.gps_center_x_mm - 9.15 mm',-13,'Parameters.imu_tray_z_mm']);additions.append(floor)
 for i,sy in enumerate([-1,1]):
  additions.append(box('IMUTowerLip'+str(i),gps,[18.3,2,2],['Parameters.gps_center_x_mm - 9.15 mm',sy*11.75-1,'Parameters.imu_tray_z_mm + 2 mm']))
 base.Shapes=list(base.Shapes)+additions;base.Refine=True
 # Two strap slots in the integrated IMU shelf; no extra mounting screws.
 slots=[]
 for i,sx in enumerate([-1,1]):
  slots.append(box('IMUTowerStrapSlot'+str(i),gps,[1.5,12,4],[f'Parameters.gps_center_x_mm + {sx*7.8} mm - 0.75 mm',-6,'Parameters.imu_tray_z_mm - 1 mm']))
 doc.GPSMountSolid.Tool.Shapes=list(doc.GPSMountSolid.Tool.Shapes)+slots
 doc.GPSMountSolid.Refine=True;doc.GPSMountSolid.Label='GPS + IMU · integrated two-level support'
 o=doc.IMUEnvelope
 o.setExpression('Length','Parameters.imu_width_mm');o.setExpression('Width','Parameters.imu_length_mm')
 o.setExpression('Placement.Base.x','Parameters.gps_center_x_mm - Parameters.imu_width_mm / 2')
 o.setExpression('Placement.Base.y','-Parameters.imu_length_mm / 2')
 o.setExpression('Placement.Base.z','Parameters.imu_tray_z_mm + 2 mm + Parameters.imu_isolation_pad_mm')
 o.Label='GY-91 · under GPS / top-level / 90 degree board rotation'
 o.ViewObject.Visibility=True
 # Move both finite battery service reservations upward with the battery.
 for name,delta in [('BatteryConnectorService',1),('BatteryAdjustmentEnvelope',2)]:
  o=doc.getObject(name)
  if o:o.setExpression('Placement.Base.z',f'Parameters.battery_cradle_z_mm + {delta} mm')
 doc.recompute()
 errors=[o.Name for o in doc.Objects if 'Error' in o.State or 'Invalid' in o.State];assert not errors,errors
 for n in ['GPSMountSolid','BatteryCradleSolid','CenterBaseSolid']:
  s=doc.getObject(n).Shape;assert s.isValid() and len(s.Solids)==1,n
 doc.commitTransaction();doc.saveCopy('/tmp/orion-sensor-battery-candidate.FCStd')
 print('IMU moved below GPS, shared tower valid; battery floor raised 10 mm to -22 mm.')
except:
 doc.abortTransaction();raise
