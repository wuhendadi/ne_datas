#-*-coding:utf-8-*-
# auth: ZJW
# Date: 2016-03-01

import requests

def _get_value(obj, key, default='null'):
    str_obj = obj.get(key, default)
    if isinstance(str_obj, str): return unicode(str_obj.decode().encode('utf-8'))
    return str_obj


def _get_request(api_host, api_port, api_func, api_name, api_key, params={}):
    s = requests.Session()
    url = 'http://%s:%s/api/json/%s/%s?apiKey=%s'%(api_host, api_port, api_func, api_name, api_key)
    for k in params:
        url += '&%s=%s'%(k,params[k])
    ret = s.get(url)
    return ret.json()
