#-*-coding:utf-8-*-
#Date:  2017年3月2日
#Auth:  zhaojunwang272

#import json
import time
import requests
from settings import api_host, api_key, api_port, device_category, alarm_host, alarm_key, alarm_port
from datas import db_base
from log import task_logger as logger
#from celery import Celery
#from settings import redis_host, redis_port
from tools.utilfunc import _get_value
from tasks.snmp_worker import do_snmp_work
from services.send_request import compare_list, update_sys_vender

#celery = Celery('tasks', broker='redis://%s:%s/0'%(redis_host, redis_port))

def get_device_by_api(api_name, api_func='device', params={}):
    s = requests.Session()
    url = 'http://%s:%s/api/json/%s/%s?apiKey=%s'%(api_host, api_port, api_func, api_name, api_key)
    for k in params:
        url += '&%s=%s'%(k,params[k])
    ret = s.get(url)
    return ret.json()

def get_device_by_alarm_api(api_name, api_func='device', params={}):
    s = requests.Session()
    url = 'http://%s:%s/api/json/%s/%s?apiKey=%s'%(alarm_host, alarm_port, api_func, api_name, alarm_key)
    for k in params:
        url += '&%s=%s'%(k,params[k])
    ret = s.get(url)
    return ret.json()


def sync_device_list():
    start_time = time.time()
    try:
        base_nms_list = db_base.session_get("nms_info_list")
        for _key in device_category:
            logger.info('category: %s'%_key)
            ret = get_device_by_api("listDevices", "device", {"category":_key})
            if ret and isinstance(ret, list):
                for _one in ret:
                    tmp_ip = _one['ipaddress']
                    db_base.session_insert_single('nms_info_list', 'zj_%s'%tmp_ip, _one['displayName'])
                    tmp_ne_dict = {"neid"        :"zj_%s"%tmp_ip,
                                   "nename"      : _get_value(_one, "deviceName"),
                                   "userlabel"   : _get_value(_one, "deviceName"),
                                   "runtime"     : _get_value(_one, "runtime"),
                                   "manager_ip"  : _get_value(_one, "ipaddress"),
                                   "vendor"      : _get_value(_one, "vendorName"),
                                   #"soft_version": _get_value(_one, "soft_version", None) or do_snmp_work(['1.3.6.1.2.1.47.1.1.1.1.10.1'], tmp_ip),
                                   "soft_version": _get_value(_one, "soft_version"),
                                   "nemodel"     : _get_value(_one, "type"),
                                   "netype"      : _get_value(_one, "category"),
                                   "memory_size" : _get_value(_one, "memory_size"),
                                   "flash_size"  : _get_value(_one, "flash_size"),
                                   "cpu_size"    : _get_value(_one, "cpu_size"),
                                   }    
                    
                    db_base.session_insert('ne:%s:ne'%tmp_ne_dict['neid'], tmp_ne_dict)
                    #TODO: frame
                    #TODO: slot
                    #TODO: ems
                    ports = get_device_by_api("getInterfaces", "device", {"name":_one["ipaddress"]})
                    if not isinstance(ports, list): 
                        logger.error('Sync_device_port Error! Reason[%s]'%ports)
                        continue
                    for _port in ports:
                        key = 'ne:%s:fm:%s:st:%s:ems:%s:port:%s:port'%('zj_%s'%tmp_ip, tmp_ip, tmp_ip, _port['ifIndex'], _port['ifIndex'])
                        tmp_port_dict = {"belongcard"   : ":".join(key.split(":")[:8]),
                                         "belongslot"   : ":".join(key.split(":")[:6]),
                                         "belongframe"  : ":".join(key.split(":")[:4]),
                                         "belongne"     : ":".join(key.split(":")[:2]),
                                         "portid"       : _get_value(_port, "ifIndex"),
                                         "name"         : _get_value(_port, "displayName"),
                                         "sn"           : _get_value(_port, "ifIndex"),
                                         "rate"         : _get_value(_port, "outSpeed"),
                                         "managerstatus": _get_value(_port, "ifAdminStatus"),
                                         "usestatus"    : _get_value(_port, "ifOperStatus"),
                                         "belongvrf"    : _get_value(_port, "belongvrf"),
                                         "ips"          : _get_value(_port, "ips", []),
                                        }  
                        db_base.session_insert(key, tmp_port_dict)
            else:
                logger.error(ret)
        
        compare_list('nms_info_list', base_nms_list, update_sys_vender)
               
    except Exception, e:
        logger.error('Sync_device_list Failed! Reason[%s]'%e)
            
    logger.info('Sync_device_list Complete! Cast %sS'%(time.time() - start_time))
    
    
def sync_alarm_list():
    start_time = time.time()
    try:
        alarms = get_device_by_alarm_api("getAlarmList", "alarm")
        for _alarm in alarms.get("Alarm", {}).get("Details", []):
            alsrm_key = 'alarm:ne:%s:alarm:%s:ne'%('zj_%s'%_alarm["source"], _alarm["modTime"])
            tmp_alarm = {"neid"        : 'ne:%s:alarm:%s'%('zj_%s'%_alarm["source"], _alarm["source"]),
                         "alarmobject" : _get_value(_alarm, "source"),
                         "objclass"    : _get_value(_alarm, "category"),
                         "vlan_name"   : _get_value(_alarm, "severity"),
                         "alarmdesc"   : _get_value(_alarm, "message"),
                         "alarmtext"   : _get_value(_alarm, "message"),
                         "alarmlevel"  : _get_value(_alarm, "severity"),
                         "nestarttime" : _get_value(_alarm, "modTime"),
                         "neendtime"   : _get_value(_alarm, "neendtime"),
                         "netstarttime": _get_value(_alarm, "modTime"),
                         "netendtime"  : _get_value(_alarm, "netendtime"),
                        }
            db_base.session_insert(alsrm_key, tmp_alarm)
    except Exception, e:
        logger.exception('sync_alarm_list Failed! Reason[%s]'%e)
        
    logger.info('sync_alarm_list Complete! Cast %sS'%(time.time() - start_time))
    
def sync_perf_list():
    start_time = time.time()
    try:
        for _key in device_category:
            rets = get_device_by_api("listDevices", "device", {"category":_key})
            if not rets or not isinstance(rets, list): continue
            for _one_ne in rets:
                tmp_ne_ip = _one_ne['ipaddress']
                params = {"policyName"  :"SwitchCPUUtilization",
                          "graphName"   :"SwitchCPUUtilization",
                          "name"        :tmp_ne_ip,
                          "checkNumeric":"true (%s)"%tmp_ne_ip,
                          }
                tmp_ne_perf = get_device_by_api("getPerfomanceMonitorDetails",params=params)
                ne_key = "perf:ne:%s:ne"%('zj_'+tmp_ne_ip)
                tmp_curr_obj = tmp_ne_perf.get("statsList", None) or [{}]
                tmp_ne_perf_dict = {"equipid": ne_key,
                                    "cpu"    : _get_value(tmp_curr_obj[0], "lastPolledValue"),
                                    "avgcpu" : _get_value(tmp_curr_obj[0], "averageValue"),
                                    }
                
                params = {"policyName"  : "CiscoMemoryUtilization",
                          "graphName"   : "CiscoMemoryUtilization",
                          "name"        : tmp_ne_ip,
                          "checkNumeric": "true"}
                tmp_ne_perf = get_device_by_api("getPerfomanceMonitorDetails",params=params)
                tmp_curr_obj = tmp_ne_perf.get("statsList", None) or [{}]
                tmp_ne_perf_dict["memory"] = _get_value(tmp_curr_obj[0], "lastPolledValue")
                
                #tmp_ne_perf = get_device_by_api("getPingResponse",params={"deviceName":tmp_ne_ip})
                tmp_ne_perf_dict["runstatus"] = "null"
                tmp_ne_perf_dict["runnormaltime"] = "null"
                tmp_ne_perf_dict["gathertime"] = "null"
                
                db_base.session_insert(ne_key, tmp_ne_perf_dict)
                
    except Exception, e:
        logger.exception('sync_alarm_list Failed! Reason[%s]'%e)
            
    logger.info('sync_perf_list Complete! Cast %sS'%(time.time() - start_time))
       
#@celery.task
def run():
    try:
        sync_device_list()
    except Exception,e:
        logger.error(e)
        return False
    
    return True
    
if __name__ == "__main__":
    run()
    
    