#-*-coding:utf-8-*-
# auth: ZJW
# Date: 2016-03-01

import requests

def _get_value(obj, key, default='null'):
    str_obj = obj.get(key, default)
    try:
        if isinstance(str_obj, str): return unicode(str_obj.decode().encode('utf-8'))
    except:
        pass
    return str_obj

def _make_ret_array(items, target_obj):
    tmp_list = []
    for _one in items:
        new_ne = {k:_get_value(_one, k) for k in _one.keys() if k != 'updatetime'}
        tmp_ne = target_obj(**new_ne)
        tmp_list.append(tmp_ne)
        
    return tmp_list


def _get_request(api_host, api_port, api_func, api_name, api_key, params={}):
    s = requests.Session()
    url = 'http://%s:%s/api/json/%s/%s?apiKey=%s'%(api_host, api_port, api_func, api_name, api_key)
    for k in params:
        url += '&%s=%s'%(k,params[k])
    ret = s.get(url)
    return ret.json()
