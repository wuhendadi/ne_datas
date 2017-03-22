#-*-coding:utf-8-*-
# auth: ZJW
# Date: 2016-03-01


import redis
import datetime
from settings import redis_host, redis_port

R_Session = redis.StrictRedis(connection_pool=redis.ConnectionPool(host=redis_host,port=redis_port,db=0))


def session_insert(key, attrs):
    for (k,v) in attrs.items():
        R_Session.hset(key, k, v)
    R_Session.hset(key, 'updatetime', datetime.datetime.now())
        
def session_insert_single(key, k, v):
    R_Session.hset(key, k, v)
    
def session_select(key):
    return R_Session.keys(key)

def session_select_all(key):
    items = []
    if isinstance(key, list):
        for _key in key:
            items += R_Session.keys(_key)
    else:
        items = R_Session.keys(key)
    if not isinstance(items, list): items = [items]
    return [R_Session.hgetall(_key) for _key in items]

def session_get(key):
    return R_Session.hgetall(key)

    
if __name__ == '__main__':
    print session_select_all("*:port:*:port")
    