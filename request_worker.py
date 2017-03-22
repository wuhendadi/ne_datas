#-*-coding:utf-8-*-
#Date:  2017年3月2日
#Auth:  zhaojunwang272

#import json
import time
import requests
from settings import api_host, api_key, api_port
from datas import db_base
from log import logger
from celery import Celery
from settings import redis_host, redis_port

celery = Celery('tasks', broker='redis://%s:%s/0'%(redis_host, redis_port)) 


def get_device_by_api(api_name, params={}):
    s = requests.Session()
    url = 'http://%s:%s/api/json/device/%s?apiKey=%s'%(api_host, api_port, api_name, api_key)
    for k in params:
        url += '&%s=%s'%(k,params[k])
    ret = s.get(url)
    return ret.json()


def sync_device_list():
    #===========================================================================
    # ca_list = get_device_by_api("getCategoryList")
    # if ca_list:
    #     for _key in ca_list.keys():
    #===========================================================================
    start_time = time.time()
    for _key in ['Switch', 'Router']:
        tmp_dict = {}
        ret = get_device_by_api("listDevices", {"category":_key})
        if ret and isinstance(ret, list):
            for _one in ret:
                tmp_dict['zj_%s'%_one['ipaddress']] = _one['displayName']
        
        db_base.session_insert('nms_info_list', tmp_dict)
        
    logger.info('Sync_device_list Complete! Cast %sS'%(time.time() - start_time))

@celery.task
def run():
    
    try:
        sync_device_list()
    except Exception,e:
        logger.error(e)
        return False
    
    return True
    
#===============================================================================
# if __name__ == "__main__":
#     run()
#===============================================================================
    
    