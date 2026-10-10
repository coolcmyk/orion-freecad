"""Native top ESC retention revision. Caller supplies doc; independent checks precede final save."""
import FreeCAD as App
from pathlib import Path
ROOT=Path('/home/kyo/ws/orion')

def box(group,name,size,base):
    o=doc.addObject('Part::Box',name);group.addObject(o)
    for prop,value in zip(['Length','Width','Height'],size):
        if isinstance(value,str):o.setExpression(prop,value)
        else:setattr(o,prop,value)
    for axis,value in zip(['x','y','z'],base):
        if isinstance(value,str):o.setExpression('Placement.Base.'+axis,value)
        else:setattr(o.Placement.Base,axis,value)
    o.ViewObject.Visibility=False
    return o

def purge_group(name):
    g=doc.getObject(name)
    if not g:return
    members=[o.Name for o in g.Group]
    for n in reversed(members):
        if doc.getObject(n):doc.removeObject(n)
    doc.removeObject(name)

doc.saveCopy('/tmp/orion-before-top-esc.FCStd')
doc.openTransaction('Integrated top ESC tie supports; remove provisional power tray')
try:
    sheet=doc.Parameters
    start=200
    for r,(alias,value,note) in enumerate([
        ('esc_top_pair_x_mm','13 mm','Proposed pair offset along X'),
        ('esc_top_side_y_mm','42.5 mm','Proposed side station; check prop and antenna clearance'),
        ('esc_top_rear_y_mm','51 mm','Proposed negative-Y side station beyond Wi-Fi keepout'),
        ('esc_top_pad_mm','0.5 mm','Proposed insulating pad; must verify heat-shrink and actual leads'),
    ],start):
        sheet.set('A'+str(r),alias);sheet.set('B'+str(r),value);sheet.setAlias('B'+str(r),alias)
        sheet.set('C'+str(r),'Proposed');sheet.set('D'+str(r),note)
    powerbolts=[o for o in doc.Objects if o.Name.startswith('PowerBaseBolt')]
    doc.CenterBaseSolidTools.Shapes=[o for o in doc.CenterBaseSolidTools.Shapes if o not in powerbolts]
    purge_group('PowerMount')
    if doc.getObject('PowerPackageProposed'):doc.removeObject('PowerPackageProposed')
    for o in powerbolts:doc.removeObject(o.Name)
    purge_group('ESCHolderInstances');purge_group('MasterESCHolder')
    obsolete=[o for o in doc.Objects if o.Name.startswith(('ESCArmHole','ESCArmHeadRecess'))]
    doc.ArmSolidTools.Shapes=[o for o in doc.ArmSolidTools.Shapes if o not in obsolete]
    for o in obsolete:doc.removeObject(o.Name)
    for o in list(doc.Objects):
        if o.Name.startswith(('ESCPowerRoute','PhaseWireEnvelope')):doc.removeObject(o.Name)
    group=doc.addObject('App::DocumentObjectGroup','TopESCRetention')
    group.Label='ESC retention · integrated center-plate tie fingers'
    ribs=[];slots=[]
    for i,(sx,sy) in enumerate([(-1,1),(1,1),(-1,-1),(1,-1)]):
        cx=f'{sx} * Parameters.esc_top_pair_x_mm'
        cy='Parameters.esc_top_side_y_mm' if sy>0 else '-Parameters.esc_top_rear_y_mm'
        parent=doc.getObject('ESCReference'+str(i));parent.Placement=App.Placement()
        o=doc.getObject('ESCEnvelope'+str(i))
        for axis in ['x','y','z']:o.setExpression('Placement.Base.'+axis,None)
        o.Placement=App.Placement()
        o.setExpression('Placement.Base.x',cx+' - Parameters.esc_length_mm / 2')
        o.setExpression('Placement.Base.y',cy+' - Parameters.esc_width_mm / 2')
        o.setExpression('Placement.Base.z','Parameters.esc_top_pad_mm')
        o.Label='ESC '+str(i+1)+' · top / insulated / two cable ties'
        o.ViewObject.Visibility=True
        for j,dx in enumerate([-8,8]):
            x=cx+f' + {dx} mm'
            # 5 mm fingers overlap the plate by 3 mm; side stations have different reach.
            y=32 if sy>0 else -56
            ribs.append(box(group,f'ESCTieFinger{i}_{j}',[5,15 if sy>0 else 24,'Parameters.center_plate_thickness_mm'],[x+' - 2.5 mm',y,'-Parameters.center_plate_thickness_mm']))
            # 2 x 4 mm through-slot retains a nominal <=1.8 mm wide tie.
            slots.append(box(group,f'ESCTieSlot{i}_{j}',[2,4,8],[x+' - 1 mm',41.5 if sy>0 else -53,-5]))
    base=doc.addObject('Part::MultiFuse','CenterPlateWithESCRetention');doc.CenterBase.addObject(base)
    base.Shapes=[doc.CenterBaseSolid.Base]+ribs;base.Refine=True;base.ViewObject.Visibility=False
    doc.CenterBaseSolid.Base=base
    doc.CenterBaseSolidTools.Shapes=list(doc.CenterBaseSolidTools.Shapes)+slots
    doc.CenterBaseSolid.Refine=True
    doc.CenterBaseSolid.Label='CENTER · integrated top ESC tie fingers'
    doc.recompute()
    errors=[o.Name for o in doc.Objects if 'Error' in o.State or 'Invalid' in o.State]
    assert not errors,errors
    assert doc.CenterBaseSolid.Shape.isValid() and len(doc.CenterBaseSolid.Shape.Solids)==1
    doc.commitTransaction()
    doc.saveCopy('/tmp/orion-top-esc-candidate.FCStd')
    print('Created native top ESC retention; removed power placeholder, tray, mounting holes and ESC tray hardware.')
except:
    doc.abortTransaction();raise
