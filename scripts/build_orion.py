"""Build the SPEC 0.3 editable fit-prototype in the live FreeCAD GUI.
Run through the FreeCAD MCP execute_code tool after importing/condensing STEP.
All manufactured shapes use native sketch/pad or expression-driven Part CSG.
"""
from pathlib import Path
import math, re, csv, json
import FreeCAD as App
import FreeCADGui as Gui
import Part, Sketcher

ROOT = Path('/home/kyo/ws/orion')
doc = App.getDocument('ORION_Frame')
if doc is None:
    doc = App.newDocument('ORION_Frame')
if doc.getObject('CenterBase'):
    raise RuntimeError('Model already exists; use its parameter sheet instead of rebuilding over it.')
if doc.getObject('Parameters'):
    doc.removeObject('Parameters')
sheet = doc.addObject('Spreadsheet::Sheet', 'Parameters')
for col, title in [('A','Parameter / stable alias'),('B','Value'),('C','Status'),('D','Source / interpretation')]:
    sheet.set(col+'1',title)
sheet.setColumnWidth('A',290); sheet.setColumnWidth('B',120)
sheet.setColumnWidth('C',110); sheet.setColumnWidth('D',520)
sheet.setStyle('A1:D1','bold','add'); sheet.setBackground('A1:D1',(0.12,0.22,0.27)); sheet.setForeground('A1:D1',(1,1,1))
rows = []; aliases = {}; row = 2

def parameter(alias,value,status,note):
    global row
    if alias in aliases:
        return
    for col, text in [('A',alias),('B',value),('C',status),('D',note)]:
        sheet.set(col+str(row), '=0 mm - ' + str(text)[1:] if col=='B' and re.match(r'^-\d',str(text)) else str(text))
    sheet.setAlias('B'+str(row),alias)
    aliases[alias] = row
    rows.append({'alias':alias,'value':str(value),'units':'mm' if '_mm' in alias else ('deg' if '_deg' in alias else ''),'status':status,'source_date':'2026-10-10','source':note,'uncertainty':'Fit verification pending' if status!='TBD' else 'Unresolved'})
    if status=='TBD': sheet.setBackground('B'+str(row),(1.0,0.81,0.63))
    row += 1

text = (ROOT/'SPEC.md').read_text()
for match in re.finditer(r'^\| `([^`]+)` \| ([^|]+) \| ([^|]+) \|',text,re.M):
    alias,value,note = match.groups()
    value=value.strip().replace('°',' deg')
    status=next((s for s in ['Specified','Derived','Baseline','Proposed','TBD'] if s.lower() in note.lower()),'Specified')
    if value=='TBD': status='TBD'
    parameter(alias,value,status,'SPEC 0.3 §4.1: '+note.strip())
# Actual interface aliases remain TBD; layout surrogates have distinct names.
for alias in ['prop_plane_z_mm','prop_sweep_thickness_mm','motor_safe_engagement_min_mm','motor_safe_engagement_max_mm','motor_underside_protrusion_mm','camera_lens_depth_mm','camera_pcb_thickness_mm','camera_cable_bend_radius_mm','imu_populated_height_mm','wifi_antenna_hardware_verified','fastener_head_diameter_mm','fastener_head_height_mm','nut_across_flats_mm','regulator_length_mm','regulator_width_mm','regulator_height_mm','pdb_length_mm','pdb_width_mm','pdb_height_mm','battery_connector_travel_mm']:
    parameter(alias,'TBD','TBD','Actual purchased hardware / physical fit measurement required')
extra = [
('motor_radius_mm','=wheelbase_mm / 2','Derived','True-X center-to-motor distance'),
('motor_coordinate_mm','=wheelbase_mm / (2 * sqrt(2))','Derived','True-X coordinate magnitude'),
('m2_clearance_mm','2.4 mm','Proposed','Printed hole coupon candidate; not thread diameter'),
('motor_pad_diameter_mm','20 mm','Proposed','14.8 mm motor plus structural rim'),
('motor_mount_plate_mm','4 mm','Proposed','M2×6 nominal engagement 2 mm; safe limit TBD'),
('motor_washer_mm','0 mm','Proposed','No washer in illustrative prototype; actual stack TBD'),
('arm_root_radius_mm','34 mm','Proposed','Keyed root seating center along local arm axis'),
('arm_root_width_mm','18 mm','Proposed','Widened circular root'),
('arm_key_length_mm','14 mm','Proposed','Root anti-rotation tongue'),
('arm_key_width_mm','8 mm','Proposed','Root anti-rotation tongue'),
('arm_key_height_mm','1.5 mm','Proposed','Tongue rises into underside center pocket'),
('arm_key_fit_mm','0.2 mm','Proposed','Per-side tongue-to-seat clearance'),
('esc_radius_mm','=motor_radius_mm - 33 mm','Derived','ESC position follows arm span'),
('esc_mount_spacing_mm','33 mm','Proposed','Two holder attachment tabs outside ESC envelope'),
('esc_tray_z_mm','-17 mm','Proposed','ESCs below arms to avoid blade sweep'),
('layout_prop_plane_z_mm','10 mm','Proposed','Unmeasured nominal sweep plane; final clearance is unresolved'),
('layout_prop_sweep_mm','4 mm','Proposed','Unmeasured blade sweep thickness; separate from specified hub thickness'),
('p4_pcb_underside_z_mm','8 mm','Proposed','Stand-offs clear underside STEP components'),
('p4_pcb_top_z_mm','=p4_pcb_underside_z_mm + p4_pcb_thickness_mm','Derived','PCB datum for imported STEP'),
('p4_rotation_deg','0 deg','Proposed','STEP orientation; actual board/cable orientation must be verified'),
('battery_cradle_z_mm','-32 mm','Proposed','Tray bottom; battery underside -30 mm'),
('battery_offset_x_mm','0 mm','Proposed','Adjustment range ±5 mm; validate connectors throughout range'),
('layout_strap_width_mm','6 mm','Proposed','Slot prototype only; actual strap_width_mm remains TBD'),
('layout_strap_thickness_mm','1 mm','Proposed','Slot prototype only; actual strap_thickness_mm remains TBD'),
('camera_pivot_x_mm','43 mm','Proposed','Front optical-axis pivot X'),
('camera_pivot_z_mm','16 mm','Proposed','Front optical-axis pivot Z'),
('camera_tilt_deg','15 deg','Proposed','Upward optical angle relative to +X; validate fisheye image'),
('layout_camera_pcb_mm','1.6 mm','Proposed','Unmeasured board thickness surrogate'),
('layout_camera_lens_depth_mm','14 mm','Proposed','Unmeasured Type G lens depth surrogate'),
('layout_camera_lens_diameter_mm','18 mm','Proposed','Unmeasured fisheye lens diameter surrogate'),
('layout_imu_height_mm','5 mm','Proposed','Unmeasured populated/header height surrogate'),
('gps_center_x_mm','-39 mm','Proposed','Raised rearward sky-facing tray'),
('gps_tray_z_mm','26 mm','Proposed','Tray bottom above Nano reference'),
('landing_bottom_z_mm','-38 mm','Proposed','Nominal underside packaging protection'),
('layout_wire_diameter_mm','2.5 mm','Proposed','Finite wire envelope; actual insulated wires TBD'),
('layout_power_length_mm','12 mm','Proposed','Candidate power package only; actual regulator/PDB TBD'),
('layout_power_width_mm','16 mm','Proposed','Candidate power package only; actual regulator/PDB TBD'),
('layout_power_height_mm','5 mm','Proposed','Candidate power package only; actual regulator/PDB TBD'),
]
for values in extra: parameter(*values)
sheet.set('B'+str(aliases['center_width_mm']),'70 mm')
sheet.set('D'+str(aliases['center_width_mm']),'Proposed layout revision: widened from 55 to 70 mm to keep outer arm-joint holes inside the plate')
doc.recompute()

def val(ex):
    if isinstance(ex,(int,float)): return float(ex)
    def replace(m):
        q=getattr(sheet,m.group(1)); return str(q.Value if hasattr(q,'Value') else q)
    raw=re.sub(r'Parameters\.([a-zA-Z0-9_]+)',replace,ex)
    raw=raw.replace(' mm','').replace(' deg','')
    return float(eval(raw,{'__builtins__':{},'sqrt':math.sqrt,'sin':math.sin,'cos':math.cos}))

def setv(obj,prop,value):
    if isinstance(value,str): obj.setExpression(prop,value)
    else: setattr(obj,prop,value)

def group(name,label=None,kind='App::DocumentObjectGroup'):
    g=doc.addObject(kind,name); g.Label=label or name; return g

reference=group('ReferenceGeometry','01 · axes / layout references')
envelopes=group('ComponentEnvelopes','02 · component references · NON-PRINTABLE')
keepouts=group('Keepouts','03 · clearance / service zones · NON-PRINTABLE')
center=group('CenterBase','04 · center plate · editable source')
arm=group('MasterArm','05 · master arm · editable source')
arms=group('ArmInstances','06 · four linked arms')
p4=group('P4Holder','07 · removable Nano holder')
esc=group('MasterESCHolder','08 · common ventilated ESC holder')
escs=group('ESCHolderInstances','09 · four linked ESC holders')
battery=group('BatteryCradle','10 · battery cradle / two strap paths')
sensors=group('SensorMounts','11 · camera / GPS / IMU / power holder')
cables=group('CableRoutes','12 · finite cable envelopes / strain relief')
landing=group('LandingGear','13 · removable landing skids')
checks=doc.addObject('Spreadsheet::Sheet','Checks'); checks.Label='14 · checks / limitations'
printables=[]; visible=[]

COL_FRAME=(0.16,0.23,0.28); COL_HOLDER=(0.12,0.63,0.64); COL_SENSOR=(0.94,0.53,0.21)
def box(g,name,l,w,h,x=0,y=0,z=0):
    o=doc.addObject('Part::Box',name); g.addObject(o)
    for k,v in [('Length',l),('Width',w),('Height',h)]: setv(o,k,v)
    for k,v in [('x',x),('y',y),('z',z)]:
        if isinstance(v,str): o.setExpression('Placement.Base.'+k,v)
    # Placement Base is a value type; assign numeric coordinates as one placement.
    o.Placement.Base=App.Vector(val(x),val(y),val(z))
    o.ViewObject.Visibility=False
    return o

def cyl(g,name,r,h,x=0,y=0,z=0,axis='Z'):
    o=doc.addObject('Part::Cylinder',name); g.addObject(o)
    setv(o,'Radius',r); setv(o,'Height',h)
    rot=App.Rotation() if axis=='Z' else App.Rotation(App.Vector(0,1,0),90) if axis=='X' else App.Rotation(App.Vector(1,0,0),-90)
    o.Placement=App.Placement(App.Vector(val(x),val(y),val(z)),rot)
    for k,v in [('x',x),('y',y),('z',z)]:
        if isinstance(v,str): o.setExpression('Placement.Base.'+k,v)
    o.ViewObject.Visibility=False
    return o

def fuse(g,name,objects):
    if len(objects)==1: return objects[0]
    o=doc.addObject('Part::MultiFuse',name); g.addObject(o); o.Shapes=objects; o.Refine=True
    for src in objects: src.ViewObject.Visibility=False
    return o

def cut(g,name,base,tools):
    tool=fuse(g,name+'Tools',tools)
    o=doc.addObject('Part::Cut',name); g.addObject(o); o.Base=base; o.Tool=tool; o.Refine=True
    base.ViewObject.Visibility=False; tool.ViewObject.Visibility=False
    return o

def finish(o,label,color,quantity=1):
    o.Label=label
    o.addProperty('App::PropertyString','ReleaseStatus','ORION'); o.ReleaseStatus='FIT PROTOTYPE · relevant measured interfaces unresolved'
    o.addProperty('App::PropertyInteger','PrintQuantity','ORION'); o.PrintQuantity=quantity
    o.addProperty('App::PropertyString','Specification','ORION'); o.Specification='SPEC.md revision 0.3'
    o.ViewObject.ShapeColor=color; o.ViewObject.LineColor=(0.07,0.1,0.13)
    o.ViewObject.DisplayMode='Flat Lines'; o.ViewObject.Visibility=True
    printables.append(o); visible.append(o); return o

def rectangle_pad(g,name,x,y,l,w,z,height):
    body=doc.addObject('PartDesign::Body',name+'Body'); g.addObject(body)
    sk=doc.addObject('Sketcher::SketchObject',name+'Sketch'); body.addObject(sk)
    a,b,c,d=val(x),val(y),val(l),val(w)
    pts=[(a,b),(a+c,b),(a+c,b+d),(a,b+d)]
    for i in range(4):
        u,v=pts[i],pts[(i+1)%4]
        sk.addGeometry(Part.LineSegment(App.Vector(u[0],u[1],0),App.Vector(v[0],v[1],0)),False)
    for i in range(4): sk.addConstraint(Sketcher.Constraint('Coincident',i,2,(i+1)%4,1))
    for i in [0,2]: sk.addConstraint(Sketcher.Constraint('Horizontal',i))
    for i in [1,3]: sk.addConstraint(Sketcher.Constraint('Vertical',i))
    for constraint,ex in [(Sketcher.Constraint('DistanceX',0,1,a),x),(Sketcher.Constraint('DistanceY',0,1,b),y),(Sketcher.Constraint('Distance',0,c),l),(Sketcher.Constraint('Distance',1,d),w)]:
        n=sk.addConstraint(constraint)
        if isinstance(ex,str): sk.setExpression('Constraints['+str(n)+']',ex)
    sk.Placement.Base=App.Vector(0,0,val(z))
    if isinstance(z,str): sk.setExpression('Placement.Base.z',z)
    pad=body.newObject('PartDesign::Pad',name+'Pad'); pad.Profile=sk; setv(pad,'Length',height)
    sk.ViewObject.Visibility=False; body.ViewObject.Visibility=False
    return body,sk

# Primary center plate and arm beam: fully constrained, sheet-driven sketches.
plate,center_sketch=rectangle_pad(center,'CenterPlate','-Parameters.center_length_mm / 2','-Parameters.center_width_mm / 2','Parameters.center_length_mm','Parameters.center_width_mm','-Parameters.center_plate_thickness_mm','Parameters.center_plate_thickness_mm')
beam,arm_sketch=rectangle_pad(arm,'ArmBeam',34,'-Parameters.arm_width_mm / 2','Parameters.motor_radius_mm - 34 mm','Parameters.arm_width_mm','-Parameters.center_plate_thickness_mm - Parameters.arm_thickness_mm','Parameters.arm_thickness_mm')
root=cyl(arm,'ArmRootRound','Parameters.arm_root_width_mm / 2','Parameters.arm_thickness_mm','Parameters.arm_root_radius_mm',0,'-Parameters.center_plate_thickness_mm - Parameters.arm_thickness_mm')
pad=cyl(arm,'MotorPad','Parameters.motor_pad_diameter_mm / 2','Parameters.motor_mount_plate_mm','Parameters.motor_radius_mm',0,'-Parameters.center_plate_thickness_mm - Parameters.motor_mount_plate_mm')
key=box(arm,'ArmKey','Parameters.arm_key_length_mm','Parameters.arm_key_width_mm','Parameters.arm_key_height_mm','Parameters.arm_root_radius_mm - Parameters.arm_key_length_mm / 2','-Parameters.arm_key_width_mm / 2','-Parameters.center_plate_thickness_mm')
arm_base=fuse(arm,'ArmBlank',[beam,root,pad,key])
arm_cuts=[]
for j in range(4):
    angle=j*90
    cx=f'Parameters.motor_radius_mm + Parameters.motor_mount_bcd_mm / 2 * cos(Parameters.motor_mount_angle_deg + {angle} deg)'
    cy=f'Parameters.motor_mount_bcd_mm / 2 * sin(Parameters.motor_mount_angle_deg + {angle} deg)'
    # Use FreeCAD expressions with their unit-aware trig functions; initial coordinates separately below.
    o=cyl(arm,'MotorBolt'+str(j),'Parameters.m2_clearance_mm / 2',12,'Parameters.motor_radius_mm',0,-10)
    o.setExpression('Placement.Base.x',cx); o.setExpression('Placement.Base.y',cy); arm_cuts.append(o)
arm_cuts.append(cyl(arm,'MotorShaftAccess',1.5,12,'Parameters.motor_radius_mm',0,-10))
for j,r in enumerate([30,38]):
    arm_cuts.append(cyl(arm,'ArmJointHole'+str(j),'Parameters.m2_clearance_mm / 2',12,r,0,-10))
    arm_cuts.append(cyl(arm,'ArmJointHeadRecess'+str(j),2.3,2,r,0,-7))
for j,sgn in enumerate([-1,1]):
    cx=f'Parameters.esc_radius_mm + {sgn} * Parameters.esc_mount_spacing_mm / 2'
    arm_cuts.append(cyl(arm,'ESCArmHole'+str(j),'Parameters.m2_clearance_mm / 2',10,cx,0,-10))
    arm_cuts.append(cyl(arm,'ESCArmHeadRecess'+str(j),2.3,2,cx,0,-5))
# Small tie slots near motor pad, away from the widened root and screw pattern.
for sgn in [-1,1]:
    arm_cuts.append(box(arm,'MotorWireTie'+str(sgn).replace('-','N'),3,1.5,10,'Parameters.motor_radius_mm - 14 mm',sgn*2.5,-10))
master_arm=finish(cut(arm,'ArmSolid',arm_base,arm_cuts),'ARM · keyed root / 4× M2 motor pattern',COL_FRAME,4)
master_arm.ViewObject.Visibility=False

center_cuts=[]
for i,theta in enumerate([45,135,225,315]):
    seat=box(center,'KeySeat'+str(i),'Parameters.arm_key_length_mm + 2 * Parameters.arm_key_fit_mm','Parameters.arm_key_width_mm + 2 * Parameters.arm_key_fit_mm','Parameters.arm_key_height_mm + Parameters.arm_key_fit_mm','Parameters.arm_root_radius_mm - Parameters.arm_key_length_mm / 2 - Parameters.arm_key_fit_mm','-Parameters.arm_key_width_mm / 2 - Parameters.arm_key_fit_mm','-Parameters.center_plate_thickness_mm')
    seat.Placement.Rotation=App.Rotation(App.Vector(0,0,1),theta)
    # Rotating an object's own placement does not rotate its translation; rotate the seat base too.
    a=math.radians(theta); radial='Parameters.arm_root_radius_mm - Parameters.arm_key_length_mm / 2 - Parameters.arm_key_fit_mm'; tangential='-Parameters.arm_key_width_mm / 2 - Parameters.arm_key_fit_mm'
    seat.setExpression('Placement.Base.x',f'({radial}) * {math.cos(a)} - ({tangential}) * {math.sin(a)}')
    seat.setExpression('Placement.Base.y',f'({radial}) * {math.sin(a)} + ({tangential}) * {math.cos(a)}')
    center_cuts.append(seat)
    for j,r in enumerate([30,38]):
        x,y=r*math.cos(a),r*math.sin(a)
        center_cuts.append(cyl(center,f'CenterJointHole{i}_{j}','Parameters.m2_clearance_mm / 2',8,x,y,-5))
        # Recessed nut seat; under-head M2×6 passes 2 mm effective arm + 3 mm plate.
        n=doc.addObject('Part::Prism',f'ArmNutSeat{i}_{j}'); center.addObject(n)
        n.Polygon=6; n.Circumradius=2.4; n.Height=1.2; n.Placement.Base=App.Vector(x,y,-1.2); center_cuts.append(n)
    link=doc.addObject('App::Link','Arm_'+['FL','RL','RR','FR'][i]); arms.addObject(link); link.setLink(master_arm)
    link.LinkPlacement=App.Placement(App.Vector(),App.Rotation(App.Vector(0,0,1),theta)); link.ViewObject.Visibility=True; visible.append(link)

# Nano holder: open low ring and four point supports around manufacturer board holes.
p4_blank=box(p4,'P4RingBlank',55,55,2,-27.5,-27.5,0)
p4_ring=cut(p4,'P4OpenRing',p4_blank,[box(p4,'P4Window',47,47,4,-23.5,-23.5,-1)])
p4_add=[p4_ring]; p4_cuts=[]
for i,sx in enumerate([-1,1]):
    for j,sy in enumerate([-1,1]):
        x=f'{sx} * Parameters.p4_hole_spacing_u_mm / 2'; y=f'{sy} * Parameters.p4_hole_spacing_v_mm / 2'
        # Bosses have bottom nut access and leave lower component space open.
        p4_add.append(cyl(p4,f'P4Boss{i}{j}',4,'Parameters.p4_pcb_underside_z_mm',x,y,0))
        p4_cuts.append(cyl(p4,f'P4BoardBolt{i}{j}','Parameters.m2_clearance_mm / 2',12,x,y,-1))
        p4_cuts.append(cyl(p4,f'P4NutAccess{i}{j}',2.45,'Parameters.p4_pcb_underside_z_mm - 2 mm',x,y,0))
for sx in [-1,1]:
    for sy in [-1,1]:
        x,y=sx*30,sy*10
        p4_add.append(box(p4,f'P4MountTab{sx}_{sy}'.replace('-','N'),7,7,2,x-3.5,y-3.5,0))
        p4_cuts.append(cyl(p4,'P4TabHole','Parameters.m2_clearance_mm / 2',6,x,y,-1))
        center_cuts.append(cyl(center,'CenterP4Hole','Parameters.m2_clearance_mm / 2',8,x,y,-5))
        center_cuts.append(cyl(center,'CenterP4NutSeat',2.45,1.5,x,y,-3))
p4_solid=finish(cut(p4,'P4HolderSolid',fuse(p4,'P4HolderBlank',p4_add),p4_cuts),'NANO HOLDER · open support / removable',COL_HOLDER)

# ESC tray in local radial coordinates. End columns reach the arm underside.
ex='Parameters.esc_radius_mm'; ez='Parameters.esc_tray_z_mm'
esc_add=[box(esc,'ESCTrayFloor',37,25,2,ex+' - 18.5 mm',-12.5,ez)]
for sy in [-1,1]:
    esc_add.append(box(esc,'ESCEdgeRail',27,2,5,ex+' - 13.5 mm',sy*11.5-1,ez+' + 2 mm'))
for sg in [-1,1]:
    cx=ex+f' + {sg} * Parameters.esc_mount_spacing_mm / 2'
    esc_add.append(box(esc,'ESCMountColumn',4,7,'-7 mm - Parameters.esc_tray_z_mm',cx+' - 2 mm',-3.5,ez))
    # Nut recesses below the upper mounting shoulder remain accessible from the end.
esc_cuts=[]
for sg in [-1,1]:
    cx=ex+f' + {sg} * Parameters.esc_mount_spacing_mm / 2'
    esc_cuts.append(cyl(esc,'ESCTabBolt','Parameters.m2_clearance_mm / 2',15,cx,0,ez))
    esc_cuts.append(box(esc,'ESCNutAccess',5,5,6,cx+' - 2.5 mm',-2.5,-15))
for sy in [-1,1]:
    esc_cuts.append(box(esc,'ESCStrapSlot',8,1.7,4,ex+' - 4 mm',sy*9.5-.85,ez+' - 1 mm'))
esc_solid=finish(cut(esc,'ESCHolderSolid',fuse(esc,'ESCTrayBlank',esc_add),esc_cuts),'ESC HOLDER · open tray / strap / end strain relief',COL_HOLDER,4)
esc_solid.ViewObject.Visibility=False
for i,theta in enumerate([45,135,225,315]):
    link=doc.addObject('App::Link','ESCTray_'+str(i)); escs.addObject(link); link.setLink(esc_solid); link.LinkPlacement=App.Placement(App.Vector(),App.Rotation(App.Vector(0,0,1),theta)); visible.append(link)
    # Reference ESC box follows the same radial station, below the propellers.
    pack=group('ESCReference'+str(i),'ESC '+str(i+1)+' · Specified envelope',kind='App::Part'); envelopes.addObject(pack)
    pack.Placement.Rotation=App.Rotation(App.Vector(0,0,1),theta)
    o=box(pack,'ESCEnvelope'+str(i),'Parameters.esc_length_mm','Parameters.esc_width_mm','Parameters.esc_height_mm',ex+' - Parameters.esc_length_mm / 2','-Parameters.esc_width_mm / 2',ez+' + 2 mm')
    o.ViewObject.ShapeColor=(0.2,0.23,0.29); o.ViewObject.Visibility=True; visible.append(o)

# Battery cradle provides length allowance for ±5 mm position and two strap slots.
bat_add=[box(battery,'BatteryFloor','Parameters.battery_length_mm + Parameters.battery_slide_travel_mm + 5 mm','Parameters.battery_width_mm + 7 mm',2,'-(Parameters.battery_length_mm + Parameters.battery_slide_travel_mm + 5 mm) / 2','-(Parameters.battery_width_mm + 7 mm) / 2','Parameters.battery_cradle_z_mm')]
for sy in [-1,1]:
    bat_add.append(box(battery,'BatterySideRail','Parameters.battery_length_mm + Parameters.battery_slide_travel_mm + 5 mm',2,5,'-(Parameters.battery_length_mm + Parameters.battery_slide_travel_mm + 5 mm) / 2',f'{sy} * (Parameters.battery_width_mm / 2 + 2.5 mm) - 1 mm','Parameters.battery_cradle_z_mm + 2 mm'))
for sx in [-1,1]:
    for sy in [-1,1]:
        x,y=sx*28,sy*13
        bat_add.append(box(battery,'BatterySupport',4,4,'-3 mm - Parameters.battery_cradle_z_mm',x-2,y-2,'Parameters.battery_cradle_z_mm'))
        bat_add.append(box(battery,'BatterySupportBridge',4,4,2,x-2,min(sy*13,sy*10),'Parameters.battery_cradle_z_mm'))
        center_cuts.append(cyl(center,'CenterBatteryBolt','Parameters.m2_clearance_mm / 2',7,x,y,-5))
bat_cuts=[]
for sx in [-1,1]:
    for sy in [-1,1]:
        bat_cuts.append(box(battery,'BatteryStrapSlot','Parameters.layout_strap_width_mm + Parameters.strap_slot_extra_mm',2,4,sx*20-3.5,sy*7.5-1,'Parameters.battery_cradle_z_mm - 1 mm'))
        bat_cuts.append(cyl(battery,'BatteryInsertPilot',.85,4,sx*28,sy*13,-7))
bat_solid=finish(cut(battery,'BatteryCradleSolid',fuse(battery,'BatteryCradleBlank',bat_add),bat_cuts),'BATTERY CRADLE · two straps / ±5 mm travel',COL_HOLDER)
bat_env=box(envelopes,'BatteryEnvelope','Parameters.battery_length_mm','Parameters.battery_width_mm','Parameters.battery_height_mm','Parameters.battery_offset_x_mm - Parameters.battery_length_mm / 2','-Parameters.battery_width_mm / 2','Parameters.battery_cradle_z_mm + 2 mm'); bat_env.ViewObject.ShapeColor=(0.32,0.4,0.64); bat_env.ViewObject.Visibility=True; visible.append(bat_env)

# Center base final: all attachment holes and keyed pockets are retained as editable cuts.
center_solid=finish(cut(center,'CenterBaseSolid',plate,center_cuts),'CENTER BASE · four keyed arm seats',COL_FRAME)

# GPS: raised open cradle with rear supports and sky-view reference.
gps=group('GPSMount','GPS support · upward antenna'); sensors.addObject(gps)
gps_add=[box(gps,'GPSTray',20.2,16.3,2,'Parameters.gps_center_x_mm - 10.1 mm',-8.15,'Parameters.gps_tray_z_mm')]
for sy in [-1,1]:
    gps_add.append(box(gps,'GPSRail',20.2,2,3,'Parameters.gps_center_x_mm - 10.1 mm',sy*7.15-1,'Parameters.gps_tray_z_mm + 2 mm'))
    gps_add.append(box(gps,'GPSPost',4,4,'Parameters.gps_tray_z_mm',-37.5,sy*6-2,0))
gps_solid=finish(fuse(gps,'GPSMountSolid',gps_add),'GPS MOUNT · elevated rear open tray',COL_SENSOR)
gps_env=box(envelopes,'GPSEnvelope','Parameters.gps_length_mm','Parameters.gps_width_mm','Parameters.gps_height_mm','Parameters.gps_center_x_mm - Parameters.gps_length_mm / 2','-Parameters.gps_width_mm / 2','Parameters.gps_tray_z_mm + 2 mm'); gps_env.ViewObject.ShapeColor=(0.79,0.75,0.55); gps_env.ViewObject.Visibility=True; visible.append(gps_env)
gps_sky=box(keepouts,'GPSSkyView',12,12,15,'Parameters.gps_center_x_mm - 6 mm',-6,'Parameters.gps_tray_z_mm + 2 mm + Parameters.gps_height_mm')

# IMU: near-origin underside tray with a proposed soft-pad interface.
imu=group('IMUMount','GY-91 · near origin / axes TBD'); sensors.addObject(imu)
imu_add=[box(imu,'IMUFloor',24.5,18.3,2,-12.25,-9.15,-13)]
for sx in [-1,1]:
    imu_add.append(box(imu,'IMUSupport',3,6,10,sx*14-1.5,-3,-13))
    imu_add.append(box(imu,'IMUBridge',5,6,2,sx*12-2.5,-3,-13))
for sy in [-1,1]: imu_add.append(box(imu,'IMULip',24.5,2,2,-12.25,sy*8.15-1,-11))
imu_solid=finish(fuse(imu,'IMUMountSolid',imu_add),'IMU MOUNT · open clip / isolation pad allowance',COL_SENSOR)
imu_env=box(envelopes,'IMUEnvelope','Parameters.imu_length_mm','Parameters.imu_width_mm','Parameters.layout_imu_height_mm','-Parameters.imu_length_mm / 2','-Parameters.imu_width_mm / 2',-11); imu_env.ViewObject.ShapeColor=(0.17,0.43,0.57); imu_env.ViewObject.Visibility=True; visible.append(imu_env)

# Power tray: isolated candidate package; actual retained regulator/harness dimensions are TBD.
power=group('PowerMount','Power packaging · provisional dimensions'); sensors.addObject(power)
power_add=[box(power,'PowerTrayFloor',16,20,2,-36,-10,-13)]
for sy in [-1,1]: power_add.append(box(power,'PowerLip',16,2,2,-36,sy*9-1,-11))
for sy in [-1,1]: power_add.append(box(power,'PowerPost',3,3,10,-37,sy*7-1.5,-13))
power_solid=finish(fuse(power,'PowerMountSolid',power_add),'POWER TRAY · insulated regulator/harness candidate',COL_SENSOR)
power_env=box(envelopes,'PowerPackageProposed','Parameters.layout_power_length_mm','Parameters.layout_power_width_mm','Parameters.layout_power_height_mm',-34,-8,-11); power_env.ViewObject.ShapeColor=(0.44,0.28,0.49); power_env.ViewObject.Visibility=True; visible.append(power_env)

# Camera frame and reference are built in an optical-axis local coordinate system.
cam=group('CameraTiltAssembly','CAMERA · adjustable +X optical axis',kind='App::Part'); sensors.addObject(cam)
cam.Placement.Base=App.Vector(43,0,16); cam.Placement.Rotation=App.Rotation(App.Vector(0,1,0),-15)
cam.setExpression('Placement.Base.x','Parameters.camera_pivot_x_mm'); cam.setExpression('Placement.Base.z','Parameters.camera_pivot_z_mm'); cam.setExpression('Placement.Rotation.Angle','-Parameters.camera_tilt_deg')
cam_src=group('CameraFrameSource','Camera rotating frame source'); cam.addObject(cam_src)
cf=box(cam_src,'CameraFrameBlank',2,29,28,-2,-14.5,-17.65)
cf=cut(cam_src,'CameraFrameOpen',cf,[box(cam_src,'CameraFrameWindow',4,17,24,-3,-8.5,-15.65)])
cam_add=[cf]
for sy in [-1,1]: cam_add.append(cyl(cam_src,'CameraPivotBoss',4,2,0,sy*15.5-1,0,axis='Y'))
cam_holes=[]
for u in [2,23]:
    for v in [8.5,22]: cam_holes.append(cyl(cam_src,'CameraBoardBolt','Parameters.m2_clearance_mm / 2',4,-3,u-12.5,v-15.65,axis='X'))
for sy in [-1,1]: cam_holes.append(cyl(cam_src,'CameraPivotHole','Parameters.m2_clearance_mm / 2',5,0,sy*15.5-2.5,0,axis='Y'))
cam_frame=finish(cut(cam_src,'CameraFrameSolid',fuse(cam_src,'CameraFrameUnion',cam_add),cam_holes),'CAMERA FRAME · correct offset 21×13.5 pattern',COL_SENSOR)
cam_ref=group('CameraReference','OV5647 Type G · dimensions / lens TBD'); cam.addObject(cam_ref)
board=box(cam_ref,'CameraPCB','Parameters.layout_camera_pcb_mm','Parameters.camera_length_mm','Parameters.camera_width_mm',0,-12.5,-15.65)
camera_holes=[]
for u in [2,23]:
    for v in [8.5,22]: camera_holes.append(cyl(cam_ref,'CameraPCBHole','Parameters.camera_hole_diameter_mm / 2',4,-1,u-12.5,v-15.65,axis='X'))
board=cut(cam_ref,'CameraPCBReference',board,camera_holes); board.ViewObject.ShapeColor=(0.1,0.45,0.31); board.ViewObject.Visibility=True; visible.append(board)
lens=cyl(cam_ref,'CameraLensProposed','Parameters.layout_camera_lens_diameter_mm / 2','Parameters.layout_camera_lens_depth_mm','Parameters.layout_camera_pcb_mm',0,0,axis='X'); lens.ViewObject.ShapeColor=(0.16,0.16,0.17); lens.ViewObject.Visibility=True; visible.append(lens)
fixed=group('CameraFixedSource','Camera fixed base / pivot ears'); sensors.addObject(fixed)
fixed_add=[box(fixed,'CameraBaseCrossTie',2,40,2,34,-20,0)]; fixed_cuts=[]
for sy in [-1,1]:
    fixed_add.append(box(fixed,'CameraFoot',11,4,2,32,sy*19-2,0))
    fixed_add.append(box(fixed,'CameraUpright',4,2,16,35,sy*19-1,0))
    fixed_add.append(box(fixed,'CameraCrossbar',9,2,4,35,sy*19-1,12))
    fixed_add.append(cyl(fixed,'CameraFixedEar',4,2,43,sy*19-1,16,axis='Y'))
    fixed_cuts.append(cyl(fixed,'CameraFixedPivot','Parameters.m2_clearance_mm / 2',4,43,sy*19-2,16,axis='Y'))
cam_fixed=finish(cut(fixed,'CameraBaseSolid',fuse(fixed,'CameraFixedBlank',fixed_add),fixed_cuts),'CAMERA BASE · removable pivot support',COL_SENSOR)
# A centerline viewing guide is illustrative, not a 160° horizontal/vertical cone.
viewaxis=cyl(cam_ref,'OpticalAxisGuide',.35,35,14,0,0,axis='X'); viewaxis.ViewObject.Visibility=False

# Two detachable skids protect nominal underside packaging.
ls=group('MasterLandingSkid','Common landing skid source'); landing.addObject(ls)
landing_add=[box(ls,'SkidRail',58,4,2,-29,-2,'Parameters.landing_bottom_z_mm')]
for sx in [-1,1]:
    landing_add.append(box(ls,'SkidPost',4,4,'-3 mm - Parameters.landing_bottom_z_mm',sx*10-2,-2,'Parameters.landing_bottom_z_mm'))
landing_solid=finish(fuse(ls,'LandingSkidSolid',landing_add),'LANDING SKID · underside protection candidate',COL_FRAME,2); landing_solid.ViewObject.Visibility=False
for sy in [-1,1]:
    lk=doc.addObject('App::Link','LandingSkid'+str(sy).replace('-','N')); landing.addObject(lk); lk.setLink(landing_solid); lk.LinkPlacement=App.Placement(App.Vector(0,sy*24,0),App.Rotation()); visible.append(lk)

# Non-printable motor, shaft and both physical / inflated prop envelopes.
prop_keepouts=[]; prop_disks=[]
for i,(sx,sy) in enumerate([(1,1),(-1,1),(-1,-1),(1,-1)]):
    x=f'{sx} * Parameters.motor_coordinate_mm'; y=f'{sy} * Parameters.motor_coordinate_mm'
    m=cyl(envelopes,'MotorBody'+str(i),'Parameters.motor_body_diameter_mm / 2','Parameters.motor_body_height_mm',x,y,'-Parameters.center_plate_thickness_mm'); m.ViewObject.ShapeColor=(0.22,0.24,0.28); m.ViewObject.Visibility=True; visible.append(m)
    shaft=cyl(envelopes,'MotorShaft'+str(i),'Parameters.motor_shaft_diameter_mm / 2','Parameters.motor_shaft_projection_mm',x,y,'-Parameters.center_plate_thickness_mm + Parameters.motor_body_height_mm'); shaft.ViewObject.ShapeColor=(0.68,0.7,0.72); shaft.ViewObject.Visibility=True
    physical=cyl(keepouts,'PropDisk'+str(i),'Parameters.prop_diameter_mm / 2',.6,x,y,'Parameters.layout_prop_plane_z_mm - 0.3 mm'); physical.ViewObject.ShapeColor=(0.78,0.83,0.88); physical.ViewObject.Transparency=80; prop_disks.append(physical)
    ko=cyl(keepouts,'ExpandedPropSweep'+str(i),'Parameters.prop_diameter_mm / 2 + Parameters.prop_radial_clearance_mm','Parameters.layout_prop_sweep_mm + 2 * Parameters.prop_vertical_clearance_mm',x,y,'Parameters.layout_prop_plane_z_mm - Parameters.layout_prop_sweep_mm / 2 - Parameters.prop_vertical_clearance_mm'); ko.ViewObject.ShapeColor=(0.96,0.59,0.2); ko.ViewObject.Transparency=87; prop_keepouts.append(ko)
    axis=cyl(reference,'MotorAxis'+str(i),.25,30,x,y,-8); axis.ViewObject.Visibility=False
# Boundary references for variants are planar, non-printable.
for W in [180,190,200]:
    a=W/(2*math.sqrt(2))
    for sx,sy in [(1,1),(1,-1),(-1,1),(-1,-1)]:
        r=cyl(reference,'Wheelbase'+str(W),1.2,.2,sx*a,sy*a,0); r.Label=f'{W} mm variant motor-axis marker'; r.ViewObject.Visibility=False

# Official STEP and exact antenna-zone anchor are injected from CAD extraction below.
nano=doc.getObject('OfficialNanoSTEP')
if nano is not None:
    envelopes.addObject(nano)
    nano.Placement.Base=App.Vector(-25,-25,val('Parameters.p4_pcb_top_z_mm'))
    nano.setExpression('Placement.Base.z','Parameters.p4_pcb_top_z_mm'); nano.ViewObject.Visibility=True; visible.append(nano)
    nano.ViewObject.ShapeColor=(0.25,0.52,0.35)
# Supplied assembly bounding box is an aid, not detailed component geometry.
nano_bbox=box(envelopes,'NanoAssemblyBounds','Parameters.p4_assembly_length_mm','Parameters.p4_assembly_width_mm','Parameters.p4_assembly_height_mm',-25.05,-26.45,'Parameters.p4_pcb_underside_z_mm - Parameters.p4_component_below_pcb_mm'); nano_bbox.ViewObject.Transparency=90

# Ports/SD and battery connector travel are explicit proposed service-space reservations.
for name,l,w,h,x,y,z in [('NanoFrontService',15,12,10,25,-6,9),('NanoRearService',15,10,10,-40,-5,9),('NanoSDService',16,15,7,-8,-40,9),('BatteryConnectorService',22,18,16,35,-9,-31),('BatteryAdjustmentEnvelope',73,16.5,14.5,-36.5,-8.25,-30)]:
    o=box(keepouts,name,l,w,h,x,y,z); o.ViewObject.ShapeColor=(0.28,0.54,0.96); o.ViewObject.Transparency=85

# Finite cable route guides below the frame, with independent visible endpoints.
for i,theta in enumerate([45,135,225,315]):
    route=group('PhaseRoute'+str(i),'Phase wires '+str(i+1)+' · routing proposal',kind='App::Part'); cables.addObject(route); route.Placement.Rotation=App.Rotation(App.Vector(0,0,1),theta)
    wire=cyl(route,'PhaseWireEnvelope'+str(i),'Parameters.layout_wire_diameter_mm / 2','Parameters.motor_radius_mm - Parameters.esc_radius_mm - Parameters.esc_length_mm / 2 - Parameters.holder_fit_clearance_mm',ex+' + Parameters.esc_length_mm / 2 + Parameters.holder_fit_clearance_mm',6,-8.5,axis='X'); wire.ViewObject.ShapeColor=(0.87,0.68,0.26); wire.ViewObject.Visibility=False
    feed=cyl(route,'ESCPowerRoute'+str(i),'Parameters.layout_wire_diameter_mm / 2','Parameters.esc_radius_mm - Parameters.esc_length_mm / 2 - Parameters.holder_fit_clearance_mm - 28 mm',28,-6,-11,axis='X'); feed.ViewObject.Visibility=False
# Tolerance coupon is a distinct native editable part, excluded from assembly views.
coupon=group('ToleranceCoupon','Fit coupon · printer calibration')
blank=box(coupon,'CouponBlank',38,22,3,0,0,0); holes=[]
for i,diam in enumerate([2.1,2.2,2.3,2.4,2.5,2.6,2.7]): holes.append(cyl(coupon,'CouponHole'+str(i),diam/2,5,4+5*i,6,-1))
for i,clear in enumerate([.25,.5,.75]): holes.append(box(coupon,'CouponSlot'+str(i),6+2*clear,1+2*clear,5,3+11*i,14,-1))
coupon_solid=finish(cut(coupon,'CouponSolid',blank,holes),'FIT COUPON · holes 2.1–2.7 / strap slot allowances',COL_HOLDER); coupon_solid.ViewObject.Visibility=False

doc.recompute()
for o in doc.Objects:
    if hasattr(o,'ViewObject') and o not in visible and o.TypeId.startswith(('Part::','PartDesign::','Sketcher::')):
        o.ViewObject.Visibility=False
for o in visible: o.ViewObject.Visibility=True
for o in [master_arm,esc_solid,landing_solid,coupon_solid]: o.ViewObject.Visibility=False
for o in prop_disks: o.ViewObject.Visibility=True
for o in prop_keepouts: o.ViewObject.Visibility=False
Gui.activeDocument().activeView().viewAxonometric(); Gui.activeDocument().activeView().fitAll()
checks.set('A1','Check'); checks.set('B1','Result'); checks.set('C1','Evidence / limits')
checks.setColumnWidth('A',240); checks.setColumnWidth('B',180); checks.setColumnWidth('C',620)
checks.setStyle('A1:C1','bold','add')
checks.set('A2','RELEASE STATUS'); checks.set('B2','FIT PROTOTYPE'); checks.set('C2','Relevant TBD inputs and physical fit acceptance remain unresolved')
checks.set('A3','Measured prop sweep'); checks.set('B3','TBD'); checks.set('C3','Model uses distinct layout surrogates; no final prop clearance claim')
checks.set('A4','IMU axes / power package'); checks.set('B4','TBD'); checks.set('C4','Proposed outlines and retention only; actual hardware required')
checks.set('A5','Sketches'); checks.set('B5',str([(s.Name,s.FullyConstrained) for s in [center_sketch,arm_sketch]])); checks.set('C5','Sheet-driven center and arm primary sketches')
with (ROOT/'measurements.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
doc.recompute()
doc.saveAs(str(ROOT/'ORION_frame.FCStd'))
print('Built',len(doc.Objects),'native objects;',len(printables),'master printable shapes')
print('Primary sketches fully constrained:',center_sketch.FullyConstrained,arm_sketch.FullyConstrained)
print('Saved',doc.FileName)
