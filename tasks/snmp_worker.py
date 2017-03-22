#-*-coding:utf-8-*-
#Date:  2017��3��2��
#Auth:  zhaojunwang272


import time

from pysnmp.hlapi import getCmd, SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity, nextCmd
from log import task_logger as logger
from datas import db_base
from settings import snmp_group, oid_list


def do_snmp_work(oids, target_ip='127.0.0.1', target_group=snmp_group):
    try:
        oid_str = ",".join(["ObjectType(ObjectIdentity('%s'))"%oid for oid in oids])
        cmd_obj = eval("getCmd(SnmpEngine(),CommunityData(target_group),UdpTransportTarget((target_ip,161)), ContextData(), %s)"%oid_str)
        
        errorIndication, errorStatus, errorindex, varBinds = next(cmd_obj)
        
        if errorIndication:
            logger.error(errorIndication)
            
        elif errorStatus:
            logger.error('%s at %s' % (errorStatus.prettyPrint(),errorindex and varBinds[int(errorindex)-1][0] or '?'))
            
        if len(oids) == 1:
            tmp_str = [varBind[1].prettyPrint() for varBind in varBinds][0]
            return tmp_str if tmp_str and not "such" in tmp_str.lower() else 'null'
        
        return [varBind[1].prettyPrint() for varBind in varBinds]
    except Exception, e:
        logger.error(e)
        return 'null'
  
        
def do_snmp_list(oid, target_ip='127.0.0.1', target_group=snmp_group):
    #tmp_dict = {}
    for (errorIndication,errorStatus,errorIndex,varBinds) in nextCmd(SnmpEngine(),
                                                                        CommunityData(target_group, mpModel=0),
                                                                        UdpTransportTarget((target_ip, 161)),
                                                                        ContextData(),
                                                                        ObjectType(ObjectIdentity(oid)),
                                                                        #取整个表名，或者指定表中某一个字段实例，均可，不过一次搞定一个表，不要跨表
                                                                        ignoreNonIncreasingOid=True,
                                                                        lexicographicMode=False,
                                                                        lookupValues=True,
                                                                        lookupMib=False):

        if errorIndication:
            logger.error(errorIndication)
            break
        elif errorStatus:
            logger.error('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
            break
        else:
            #return {varBind[0].prettyPrint(): varBind[1].prettyPrint() for varBind in varBinds}
            for varBind in varBinds:
                #print ' = '.join([x.prettyPrint() for x in varBind])
                #tmp_dict[varBind[0].prettyPrint()] = varBind[1].prettyPrint()
                yield {varBind[0].prettyPrint(): varBind[1].prettyPrint()}
                
    #return tmp_dict


def sync_snmp_info():
    start_time = time.time()
    for ne_item in db_base.session_select_all('ne:zj_*:ne'):
        ne_item_type, ne_item_ip = ne_item.get('nemodel', None), ne_item.get('manager_ip', None)
        if not ne_item_type or not ne_item_ip: continue
        oids = oid_list.get(ne_item_type, {})
        for _sub_key in oids.keys():
            key_obj = oids[_sub_key]
            if _sub_key == 'configoids':
                for _config_key in key_obj.keys():
                    for _val in do_snmp_list(key_obj[_config_key], '127.0.0.1'):
                        db_target_key = "ne:zj_%s:ne"%ne_item_ip
                        print _val
                        if _val.get(key_obj[_config_key], None):
                            db_base.session_insert(db_target_key, {_config_key: _val[key_obj[_config_key]]})
            elif _sub_key == 'frame':
                for _frame_key in key_obj.keys():
                    for _val in do_snmp_list(key_obj[_frame_key], '127.0.0.1'):
                        print _val
            elif _sub_key == 'slot':
                #TODO
                continue
            elif _sub_key == 'card':
                #TODO
                continue
            elif _sub_key == 'port':
                #TODO
                continue
                                                              
    logger.info('Sync_snmp_info Complete! Cast %sS'%(time.time() - start_time))
    
         
if __name__ == '__main__':
    #print do_snmp_list('1.3.6.1.2.1')
    #sync_snmp_info()
    print do_snmp_work(['.1.3.6.1.2.1'])

