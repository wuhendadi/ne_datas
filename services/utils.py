#-*-coding:utf-8-*-
#Date:  2017年3月2日
#Auth:  zhaojunwang272


from spyne import ComplexModel, Unicode, Array, XmlAttribute, Mandatory

Neobjlist = Mandatory(Array(Mandatory(Unicode, min_occurs=0, nillable=True), type_name='neobjlist', member_name='emssn', min_occurs=0, nillable=True), min_occurs=0, nillable=True)
Cardobjlist = Mandatory(Array(Mandatory(Unicode, min_occurs=0, nillable=True), type_name='cardobjlist', member_name='emssn', min_occurs=0, nillable=True), min_occurs=0, nillable=True)


class Flow(ComplexModel):
    
    __type_name__ = 'flow'
    _type_info = [
           ('period', XmlAttribute(Unicode)),
           ('p_flow', Unicode),
           ('p_inflow', Unicode),
           ('p_outflow', Unicode),
           ('starttime', Unicode),
           ('endtime', Unicode),
           ('srcip', Unicode),
           ('srcport', Unicode),
           ('destip', Unicode),
           ('destport', Unicode),
           ('protocal ', Unicode),
           ('packagesize', Unicode),
           ('packagecount', Unicode),
           ('passport', Unicode),
           ]
    
class Cardperf(ComplexModel):
    
    __type_name__  = 'cardperf'
    _type_info = [
            ('cardid', Unicode),
            ('occ_cpu', Unicode),
            ('occ_memory', Unicode),
            ('gathertime', Unicode),
            ]
    
    
class Linkperf(ComplexModel):
    
    __type_name__  = 'linkperf'
    _type_info = [
            ('linkid', Unicode),
            ('linkstatus', Unicode),
            ('speed', Unicode),
            ('occ_rate', Unicode),
            ('occ_lostpackages', Unicode),
            ('occ_errpackages', Unicode),
            ('shake', Unicode),
            ('gathertime', Unicode),
            ]


class Portperf(ComplexModel):
    
    __type_name__ = 'portperf'
    _type_info = [
            ('belongcard', Unicode),
            ('belongne', Unicode),
            ('portid', Unicode),
            ('managerstatus', Unicode),
            ('usestatus', Unicode),
            ('errorpackages', Unicode),
            ('inerrorpackages', Unicode),
            ('outerrorpackages', Unicode),
            ('lostpackages', Unicode),
            ('inlostpackages', Unicode),
            ('outlostpackages', Unicode),
            ('packages', Unicode),
            ('inpackages', Unicode),
            ('outpackages', Unicode),
            ('speed', Unicode),
            ('in_speed', Unicode),
            ('out_speed', Unicode),
            ('occ_rate', Unicode),
            ('flow', Array(Flow)),
            ('gathertime', Unicode) 
            ]
                                                                                                                                                                                                                                                                                                                                       
class Neperf(ComplexModel):
    
    __type_name__  = 'neperf'
    _type_info = [
            ('neid', Unicode),
            ('equipid', Unicode),
            ('cpu', Unicode),
            ('avgcpu', Unicode),
            ('memory', Unicode),
            ('runstatus', Unicode),
            ('runnormaltime', Unicode),
            ('gathertime', Unicode)
            ]


class Alarm(ComplexModel):
    
    __type_name__  = 'alarm'
    _type_info = [
            ('alarmobject', Unicode),
            ('objclass', Unicode),
            ('alarmtype', Unicode),
            ('alarmdesc', Unicode),
            ('alarmtext', Unicode),
            ('alarmlevel', Unicode),
            ('nestarttime', Unicode),
            ('neendtime', Unicode),
            ('netstarttime', Unicode),
            ('netendtime', Unicode),
            ]


class Vlan(ComplexModel):
    
    __type_name__  = 'vlan'
    _type_info = [
            ('vlanid', Unicode),
            ('vlan_name', Unicode),
            ('portid', Unicode),
            ]


class Vpn(ComplexModel):
    
    __type_name__  = 'vpn'
    _type_info = [
            ('belongport', XmlAttribute(Unicode)),
            ('belongne', XmlAttribute(Unicode)),
            ('vrfid', Unicode),
            ('vrf_name', Unicode),
            ('rd', Unicode),
            ('rt_imp', Unicode),
            ('rt_exp', Unicode),
            ]


class Configfile(ComplexModel):
    
    __type_name__  = 'configfile'
    _type_info = [
            ('equipid', Unicode),
            ('startup', Unicode),
            ('running', Unicode),
            ('gathertime', Unicode),
            ]


class Link(ComplexModel):
    
    __type_name__  = 'link'
    _type_info = [
            ('linkid', Unicode),
            ('linkname', Unicode),
            ('userlabel', Unicode),
            ('linkstatus', Unicode),
            ('aport', Unicode),
            ('zport', Unicode),
            ('rate', Unicode),
            ('linktype', Unicode),
            ]
    

class Portrelation(ComplexModel):
    
    __type_name__  = 'portrelation'
    _type_info = [
            ('logicportid', Unicode),
            ('physicalid', Unicode),
            ]   


class Ip(ComplexModel):
    
    __type_name__  = 'ip'
    _type_info = [
            ('ipid', Unicode),
            ('ipvalue', Unicode),
            ('masks', Unicode),
            ]    
            

class Port(ComplexModel):
    
    __type_name__  = 'port'
    _type_info = [
            ('belongscard', XmlAttribute(Unicode)),
            ('belongslot', XmlAttribute(Unicode)),
            ('belongframe', XmlAttribute(Unicode)),
            ('belongne', XmlAttribute(Unicode)),
            ('portid', Unicode),
            ('name', Unicode),
            ('sn', Unicode),
            ('rate', Unicode),
            ('mac_address', Unicode),
            ('managerstatus', Unicode),
            ('usestatus', Unicode),
            ('port_type', Unicode),
            ('belongvrf', Unicode),
            ('islogicport', Unicode),
            ('accesstype', Unicode),
            ('workmode', Unicode),
            ('ips', Array(Ip)),
            ]


class Card(ComplexModel):
    
    __type_name__  = 'card'
    _type_info = [
            ('belongslot', XmlAttribute(Unicode)),
            ('belongframe', XmlAttribute(Unicode)),
            ('belongne', XmlAttribute(Unicode)),
            ('cardid', Unicode),
            ('cardname', Unicode),
            ('userlabel', Unicode),
            ('cardserial', Unicode),
            ('soft_version', Unicode),
            ('hard_version', Unicode),
            ('cpu_count', Unicode),
            ('memory_size', Unicode),
            ]
    
    
class Frame(ComplexModel):
    
    __type_name__  = 'frame'
    _type_info = [
            ('belongne', XmlAttribute(Unicode)),
            ('frameid', Unicode),
            ('framenename', Unicode),
            ('userlabel', Unicode),
            ('frameserial', Unicode),
            ('framemodel', Unicode),
            ('fatherframe', Unicode),
            ]


class Slot(ComplexModel):
    
    __type_name__  = 'slot'
    belongframe = XmlAttribute(Unicode)
    belongne = XmlAttribute(Unicode)
    _type_info = [
            ('belongframe', XmlAttribute(Unicode)),
            ('belongne', XmlAttribute(Unicode)),
            ('slotid', Unicode),
            ('slotname', Unicode),
            ('userlabel', Unicode),
            ('slotserial', Unicode),
            ('fatherslot', Unicode),
            ]


class Ne(ComplexModel):
    
    __type_name__  = 'ne'
    _type_info = [
            ('neid', Unicode),
            ('nename', Unicode),
            ('userlabel', Unicode),
            ('runtime', Unicode),
            ('manager_ip', Unicode),
            ('vendor', Unicode),
            ('soft_version', Unicode),
            ('nemodel', Unicode),
            ('netype', Unicode),
            ('memory_size', Unicode),
            ('flash_size', Unicode),
            ('cpu_size', Unicode),
            ]


class Sys(ComplexModel):
    
    __type_name__ = 'sys'
    _type_info = [
            ('name', Unicode),
            ('userlabel', Unicode),
            ('version', Unicode),
            ('nes', Array(Ne))
            ]
    
     
class ResultModel(ComplexModel):
    
    __type_name__ = 'resultmodel'
    _type_info = [
            ('resultsign', Unicode),
            ('sys', Sys),
            ('nes', Array(Ne)),
            ('frames', Array(Frame)),
            ('slots', Array(Slot)),
            ('cards', Array(Card)),
            ('ports', Array(Port)),
            ('portrelations', Array(Portrelation)),
            ('links', Array(Link)),
            ('configfiles', Array(Configfile)),
            ('vpns', Array(Vpn)),
            ('vlans', Array(Vlan)),
            ('alarms', Array(Alarm)),
            ('neperfs', Array(Neperf)),
            ('portperfs', Array(Portperf)),
            ('linkperfs', Array(Linkperf)),
            ('cardperfs', Array(Cardperf)),
            ('flows', Array(Flow))
            ]
    
    
