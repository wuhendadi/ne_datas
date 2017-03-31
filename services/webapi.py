#-*-coding:utf-8-*-
#Date:  2017年3月2日
#Auth:  zhaojunwang272

#import time
import thread
#from lxml import etree
#from spyne.util.xml import get_object_as_xml
from spyne import rpc, ServiceBase
from services.utils import ResultModel, Sys, Ne, Neobjlist, Cardobjlist, Port, Ip, Neperf, Alarm, Link, Portperf, Flow
from spyne import Integer, Unicode, Array
from settings import sys_name, user_label, version
from datas import db_base
from tools.utilfunc import _get_value, _make_ret_array
from tasks.snmp_worker import do_snmp_work
from tasks.ftp_worker import ftp_up_xml


class DeviceService(ServiceBase):
    
    
    #############################TEST SERVER API##############################################
    @rpc(_returns=ResultModel)
    def activeGetSysVender(self):

        return ResultModel(resultsign=1)
    
    @rpc(Sys, _returns=ResultModel)
    def passiveSetSysTms(self, sys):
        print sys
        return ResultModel(resultsign=1)  
    ##########################################################################################
    
    @rpc(_returns=ResultModel)
    def activeGetSysTms(self):

        return ResultModel(resultsign=1)
    
    @rpc(_returns=ResultModel)
    def passiveSetSysVender(self):
        
        items = db_base.session_get("nms_info_list")
        tmp_list = [Ne(neid=k, nename=v) for (k,v) in items.items()]
        sys_obj = Sys(name=sys_name, userlabel=user_label, version=version, nes=tmp_list)
        
        return ResultModel(resultsign=1, sys=sys_obj)       
    
    
    @rpc(_returns=ResultModel)
    def activeGetNeTms(self):
        
        return ResultModel(resultsign=1)
    
    
    @rpc(Neobjlist, _returns=ResultModel)
    def passiveSetNeVendor(self, Neobjlist):
        
        if not Neobjlist:
            ne_items = db_base.session_select_all('ne:zj_*:ne')
        else:
            ne_items = [db_base.session_get('ne:%s:ne'%_ne) for _ne in Neobjlist]
                
        tmp_list = _make_ret_array(ne_items, Ne)
    
        #=======================================================================
        # for _ne in ne_items:
        #     tmp_ne = Ne(neid         = _get_value(_ne, 'neid'),
        #                 nename       = _get_value(_ne, 'nename'),
        #                 userlabel    = _get_value(_ne, 'userlabel'),
        #                 runtime      = _get_value(_ne, 'runtime'),
        #                 manager_ip   = _get_value(_ne, 'manager_ip'),
        #                 vendor       = _get_value(_ne, 'vendor'),
        #                 soft_version = _get_value(_ne, 'soft_version', None),
        #                 nemodel      = _get_value(_ne, 'nemodel'),
        #                 netype       = _get_value(_ne, 'netype'),
        #                 memory_size  = _get_value(_ne, 'memory_size'),
        #                 flash_size   = _get_value(_ne, 'flash_size'),
        #                 cpu_size     = _get_value(_ne, 'cpu_size'))
        #=======================================================================
            
        return ResultModel(resultsign=1, nes=tmp_list)
    
    
    @rpc(_returns=ResultModel)
    def activeGetNeFrameTms(self):

        return ResultModel(resultsign=1)
    
    
    @rpc(_returns=ResultModel)
    def passiveSetNeFrameVendor(self):
        return
    
    @rpc(_returns=ResultModel)
    def activeGetNeSlotTms(self):

        return ResultModel(resultsign=1)
    
    
    @rpc(_returns=ResultModel)
    def passiveSetNeSlotVendor(self):
        return
    
    
    @rpc(_returns=ResultModel)
    def activeGetNeCardTms(self):

        return ResultModel(resultsign=1)
    
    
    @rpc(_returns=ResultModel)
    def passiveSetNeCardVendor(self):
        return
    
    
    @rpc(_returns=ResultModel)
    def activeGetNePortTms(self):

        return ResultModel(resultsign=1)
    
    
    @rpc(Cardobjlist, _returns=ResultModel)
    def passiveSetNePortVender(self, cardobjlist):
        tmp_list, items = [], []
        for _card in cardobjlist:                 
            keys = db_base.session_select(_card + ':port:*')
            items += [db_base.session_get(k) for k in keys]
         
        if not items: items = db_base.session_select('*:port:*:port')
        
        for item in items:
            new_port = Port(belongcard    = _get_value(item, 'belongcard'), 
                            belongslot    = _get_value(item, 'belongslot'), 
                            belongframe   = _get_value(item, 'belongframe'), 
                            belongne      = _get_value(item, 'belongne'), 
                            portid        = _get_value(item, 'portid'),
                            name          = _get_value(item, 'name'),
                            sn            = _get_value(item, 'sn'),
                            rate          = _get_value(item, 'rate'),
                            mac_address   = _get_value(item, 'mac_address'),
                            managerstatus = _get_value(item, 'managerstatus'),
                            usestatus     = _get_value(item, 'usestatus'),
                            port_type     = _get_value(item, 'port_type'),
                            belongvrf     = _get_value(item, 'belongvrf'),
                            islogicport   = _get_value(item, 'islogicport'),
                            accesstype    = _get_value(item, 'accesstype'),
                            workmode      = _get_value(item, 'workmode'),
                            ips           = (Ip(ipid='null',ipvalue='null',masks='null')))
            
            tmp_list.append(new_port)
        
        return ResultModel(resultsign=1, ports=tmp_list)
    
    
    @rpc(_returns=ResultModel)
    def activeGetNePortRelationTms(self):

        return ResultModel(resultsign=1)
    
    @rpc(_returns=ResultModel)
    def passiveSetNePortRelationVendor(self):
        return
    
    
    @rpc(_returns=ResultModel)
    def activeGetLinkTms(self):

        return ResultModel(resultsign=1)
    
    
    @rpc(_returns=ResultModel)
    def passiveSetLinkVender(self):
        tmp_list = []
        for item in db_base.session_select_all("link:*:link"):
            new_link = Link(linkid     = _get_value(item, 'linkid'), 
                            linkname   = _get_value(item, 'linkname'), 
                            userlabel  = _get_value(item, 'userlabel'), 
                            linkstatus = _get_value(item, 'linkstatus'), 
                            aport      = _get_value(item, 'aport'),
                            zport      = _get_value(item, 'zport'),
                            rate       = _get_value(item, 'rate'),
                            linktype   = _get_value(item, 'linktype'))
            
            tmp_list.append(new_link)
        
        return ResultModel(resultsign=1, links=tmp_list)
    
    
    @rpc(_returns=ResultModel)
    def activeGetConfigFileTms(self):

        return ResultModel(resultsign=1)
    
    
    @rpc(_returns=ResultModel)
    def passiveSetConfigFileVendor(self):
        return
    
    
    @rpc(_returns=ResultModel)
    def activeGetVpnTms(self):

        return ResultModel(resultsign=1)
    
    
    @rpc(_returns=ResultModel)
    def passiveSetVpnVendor(self):
        return
    
    
    @rpc(_returns=ResultModel)
    def activeGetVlanTms(self):

        return ResultModel(resultsign=1)
    
    
    @rpc(_returns=ResultModel)
    def passiveSetVlanVendor(self):
        return
    

####################################################################################################################
  
    @rpc(_returns=ResultModel)
    def activeGetAlarmTms(self):
         
        def _do_perf_alarm_ftp():
            tmp_list = []
            ne_alarms = db_base.session_select_all('perf:zj_*:alarm:*:ne')
            for _ne_alarm in ne_alarms:
                new_ne_alarm = Alarm(alarmobject  = _get_value(_ne_alarm, 'alarmobject'),
                                      objclass     = _get_value(_ne_alarm, 'objclass'),
                                      alarmtype    = _get_value(_ne_alarm, 'alarmtype'),
                                      alarmdesc    = _get_value(_ne_alarm, 'alarmdesc'),
                                      alarmtext    = _get_value(_ne_alarm, 'alarmtext'),
                                      alarmlevel   = _get_value(_ne_alarm, 'alarmlevel'),
                                      nestarttime  = _get_value(_ne_alarm, 'nestarttime'),
                                      neendtime    = _get_value(_ne_alarm, 'neendtime'),
                                      netstarttime = _get_value(_ne_alarm, 'netstarttime'),
                                      netendtime   = _get_value(_ne_alarm, 'netendtime'))
                
                tmp_list.append(new_ne_alarm)
            
            ftp_up_xml(ResultModel(alarms=tmp_list), ResultModel, "activeGetAlarmTms")
        
        thread.start_new_thread(_do_perf_alarm_ftp, ())
        return ResultModel(resultsign=1)
    
    @rpc(_returns=ResultModel)
    def activeGetAlarmByDeviceTms(self):

        return ResultModel(resultsign=1)
    
    
    @rpc(_returns=ResultModel)
    def passiveSetAlarmByDeviceVendor(self):
        return
    
########################################################################################################################    
    
    
    @rpc(Neobjlist, _returns=ResultModel)
    def activeGetNePerfTms(self, neobjlist):
         
        def _do_ftp():
            tmp_list = []
            ne_prefs = db_base.session_select('perf:ne:zj_*:ne')
            for _ne_perf_key in ne_prefs:
                _ne_perf = db_base.session_get(_ne_perf_key)
                new_ne_perf = Neperf(equipid       = _get_value(_ne_perf, 'equipid'),
                                     cpu           = _get_value(_ne_perf, 'cpu'),
                                     avgcpu        = _get_value(_ne_perf, 'avgcpu'),
                                     memory        = _get_value(_ne_perf, 'memory'),
                                     runstatus     = _get_value(_ne_perf, 'runstatus'),
                                     runnormaltime = _get_value(_ne_perf, 'runnormaltime'),
                                     gathertime    = _get_value(_ne_perf, 'gathertime'))
                tmp_list.append(new_ne_perf)
                 
            ftp_up_xml(ResultModel(neperfs=tmp_list), ResultModel, "activeSetNePerfVendor")
         
        thread.start_new_thread(_do_ftp, ())
         
        return ResultModel(resultsign=1)
    
    
    @rpc(Neobjlist, _returns=ResultModel)
    def activeGetPortPerfTms(self, neobjlist):
         
        def _do_perf_port_ftp():
            tmp_list = []
            for _port_perf in db_base.session_select_all('perf:ne:zj_*:card:*:port:*:port'):
                flows = [Flow(period=_one['period'], p_flow=_one['p_flow'], p_inflow=_one['p_inflow'], p_outflow=_one['p_outflow']) for _one in _get_value(_port_perf, "flow", [])]
                new_port_perf = Portperf(belongcard = _get_value(_port_perf, "belongcard"),
                                        belongne = _get_value(_port_perf, "belongne"),
                                        portid = _get_value(_port_perf, "portid"),
                                        managerstatus = _get_value(_port_perf, "managerstatus"),
                                        usestatus = _get_value(_port_perf, "usestatus"),
                                        errorpackages = _get_value(_port_perf, "errorpackages"),
                                        inerrorpackages = _get_value(_port_perf, "inerrorpackages"),
                                        outerrorpackages = _get_value(_port_perf, "outerrorpackages"),
                                        lostpackages = _get_value(_port_perf, "lostpackages"),
                                        inlostpackages = _get_value(_port_perf, "inlostpackages"),
                                        outlostpackages = _get_value(_port_perf, "outlostpackages"),
                                        packages = _get_value(_port_perf, "packages"),
                                        inpackages = _get_value(_port_perf, "inpackages"),
                                        outpackages = _get_value(_port_perf, "outpackages"),
                                        speed = _get_value(_port_perf, "speed"),
                                        in_speed = _get_value(_port_perf, "in_speed"),
                                        out_speed = _get_value(_port_perf, "out_speed"),
                                        occ_rate = _get_value(_port_perf, "occ_rate"),
                                        flow = flows,
                                        gathertime = _get_value(_port_perf, "gathertime")
                                        )
            
                
                tmp_list.append(new_port_perf)
        
            ftp_up_xml(ResultModel(neperfs=tmp_list), ResultModel, "activeGetPortPerfTms")
        
        thread.start_new_thread(_do_perf_port_ftp, ())
        return ResultModel(resultsign=1)
    
    
    @rpc(_returns=ResultModel)
    def activeGetLinkPerfTms(self):
        return
    
    
    @rpc(_returns=ResultModel)
    def activeGetCardPerfTms(self):
        return
    
######################################################################################################################

    @rpc(Neobjlist, _returns=ResultModel)
    def activeGetFlowTms(self, neobjlist):
        return
    
    
    
    
def on_method_return_string(ctx):
    ctx.out_string[0] = ctx.out_string[0].replace('tns0:', '').replace('s0:', '')

DeviceService.event_manager.add_listener('method_return_string', on_method_return_string)
    
