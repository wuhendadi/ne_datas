#-*-coding:utf-8-*-
#Date:  2017年3月7日
#Auth:  zhaojunwang272


from datas import db_base
from zeep import Client
from services.utils import ResultModel, Neperf, Portperf, Linkperf, Cardperf, Flow
from tasks.ftp_worker import ftp_up_xml
from settings import server_url, sys_name, user_label, version

SERVER_UTILS = "services.utils"

def _get_ret_obj(t_client, items, target_obj, target_obj_array):
    factory = t_client.type_factory(SERVER_UTILS)
    tmp_list = factory.target_obj_array([factory.target_obj(**one) for one in items])
    return tmp_list

def _send_request(active_func, passive_func, items):
    
    t_client = Client(server_url)
    t_client.service.active_func()
    array_obj = _get_ret_obj(t_client, items)
    return t_client.service.passive_func(array_obj)
    

def update_sys_vender(items=None):
    t_client = Client(server_url)
    if not items: items = db_base.session_get("nms_info_list")
    t_client.service.activeGetSysVender()
    factory = t_client.type_factory(SERVER_UTILS)
    tmp_list = factory.neArray([factory.ne(neid=k, nename=v) for (k,v) in items.items()])
    sys_obj = factory.sys(name=sys_name, userlabel=user_label, version=version, nes=tmp_list)
    respose = t_client.service.passiveSetSysTms(sys_obj)
    return respose

def update_ne_vender(items=None):
    t_client = Client(server_url)
    t_client.service.activeSetNeVendor()
    factory = t_client.type_factory(SERVER_UTILS)
    tmp_list = factory.neArray([factory.ne(**one) for one in items])
    respose = t_client.service.passiveSetNeTms(tmp_list)
    return respose

def update_frame_vender(items=None):
    t_client = Client(server_url)
    t_client.service.activeSetNeFrameVendor()
    factory = t_client.type_factory(SERVER_UTILS)
    tmp_list = factory.frameArray([factory.frame(**one) for one in items])
    respose = t_client.service.passiveSetNeFrameTms(tmp_list)
    return respose

def update_slots_vender(items=None):
    t_client = Client(server_url)
    t_client.service.activeSetNeSlotVendor()
    factory = t_client.type_factory(SERVER_UTILS)
    tmp_list = factory.slotArray([factory.solt(**one) for one in items])
    respose = t_client.service.passiveSetNeSlotTms(tmp_list)
    return respose

def update_card_vender(items=None):
    t_client = Client(server_url)
    t_client.service.activeSetNeCardVendor()
    factory = t_client.type_factory(SERVER_UTILS)
    tmp_list = factory.cardArray([factory.card(**one) for one in items])
    respose = t_client.service.passiveSetNeCardTms(tmp_list)
    return respose

def update_port_vender(items=None):
    t_client = Client(server_url)
    t_client.service.activeSetNePortVendor()
    factory = t_client.type_factory(SERVER_UTILS)
    tmp_list = factory.portArray([factory.port(**one) for one in items])
    respose = t_client.service.passiveSetNePortTms(tmp_list)
    return respose

def update_port_relation_vendor(items=None):
    t_client = Client(server_url)
    t_client.service.activeSetNePortRelationVendor()
    factory = t_client.type_factory(SERVER_UTILS)
    tmp_list = factory.portrelationArray([factory.portrelation(**one) for one in items])
    sys_obj = factory.sys(name=sys_name, userlabel=user_label, version=version, nes=tmp_list)
    respose = t_client.service.passiveSetNePortRelationTms(sys_obj)
    return respose

def update_link_vendor(items=None):
    t_client = Client(server_url)
    t_client.service.activeSetLinkVendor()
    factory = t_client.type_factory(SERVER_UTILS)
    tmp_list = factory.linkArray([factory.link(**one) for one in items])
    sys_obj = factory.sys(name=sys_name, userlabel=user_label, version=version, nes=tmp_list)
    respose = t_client.service.passiveSetLinkTms(sys_obj)
    return respose

def update_config_file_vendor(items=None):
    t_client = Client(server_url)
    t_client.service.activeSetConfigFileVendor()
    factory = t_client.type_factory(SERVER_UTILS)
    tmp_list = factory.configfileArray([factory.configfile(**one) for one in items])
    respose = t_client.service.passiveSetConfigFileTms(tmp_list)
    return respose

def update_vpn_vendor(items=None):
    t_client = Client(server_url)
    t_client.service.activeSetVpnVendor()
    factory = t_client.type_factory(SERVER_UTILS)
    tmp_list = factory.vpnArray([factory.vpn(**one) for one in items])
    respose = t_client.service.passiveSetVpnTms(tmp_list)
    return respose

def update_vlan_vendor(items=None):
    t_client = Client(server_url)
    t_client.service.activeSetVlanVendor()
    factory = t_client.type_factory(SERVER_UTILS)
    tmp_list = factory.vlanArray([factory.vlan(**one) for one in items])
    respose = t_client.service.passiveSetVlanTms(tmp_list)
    return respose

def update_alarm_vendor(items=None):
    t_client = Client(server_url)
    t_client.service.activeSetAlarmVendor()
    factory = t_client.type_factory(SERVER_UTILS)
    tmp_list = factory.alarmArray([factory.alarm(**one) for one in items])
    respose = t_client.service.passiveSetAlarmTms(tmp_list)
    return respose

def update_ne_perf_vendor(items=None):
    t_client = Client(server_url)
    t_client.service.activeSetNePerfVendor()
    tmp_list = [Neperf(**one) for one in items]
    ftp_up_xml(ResultModel(neperfs=tmp_list), ResultModel, "activeSetNePerfVendor")
    

def update_port_perf_vendor(items=None):
    t_client = Client(server_url)
    t_client.service.activeSetPortPerfVendor()
    tmp_list = [Portperf(**one) for one in items]
    ftp_up_xml(ResultModel(portperfs=tmp_list), ResultModel, "activeSetPortPerfVendor")

def update_link_perf_vendor(items=None):
    t_client = Client(server_url)
    t_client.service.activeSetLinkPerfVendor()
    tmp_list = [Linkperf(**one) for one in items]
    ftp_up_xml(ResultModel(linkperfs=tmp_list), ResultModel, "activeSetLinkPerfVendor")
    
def update_card_perf_vendor(items=None):
    t_client = Client(server_url)
    t_client.service.activeSetCardPerfVendor()
    tmp_list = [Cardperf(**one) for one in items]
    ftp_up_xml(ResultModel(cardperfs=tmp_list), ResultModel, "activeSetCardPerfVendor")

def update_flow_vendor(items=None):
    t_client = Client(server_url)
    t_client.service.activeSetFlowVendor()
    tmp_list = [Flow(**one) for one in items]
    ftp_up_xml(ResultModel(flows=tmp_list), ResultModel, "activeSetFlowVendor")

def compare_list(key, base_list, callbackfunc):
    new_list = db_base.session_select_all(key)
    if not isinstance(base_list, list):
        base_list = [base_list]
    if base_list != new_list:
        callbackfunc(new_list)
    
    
if __name__ == '__main__':
    update_sys_vender()
    
    