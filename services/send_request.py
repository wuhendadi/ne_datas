#-*-coding:utf-8-*-
#Date:  2017年3月7日
#Auth:  zhaojunwang272


from datas import db_base
from zeep import Client
from settings import server_url, sys_name, user_label, version


def update_sys_vender(items=None):
    t_client = Client(server_url)
    if not items: items = db_base.session_get("nms_info_list")
    t_client.service.activeGetSysVender()
    factory = t_client.type_factory("services.utils")
    tmp_list = factory.neArray([factory.ne(neid=k, nename=v) for (k,v) in items.items()])
    sys_obj = factory.sys(name=sys_name, userlabel=user_label, version=version, nes=tmp_list)
    respose = t_client.service.passiveSetSysTms(sys_obj)
    print respose
    return respose

def compare_list(key, base_list, callbackfunc):
    new_list = db_base.session_select_all(key)
    if not isinstance(base_list, list):
        base_list = [base_list]
    if base_list != new_list:
        callbackfunc(new_list)
    
    
if __name__ == '__main__':
    update_sys_vender()
    
    