#-*-coding:utf-8-*-
# auth: ZJW
# Date: 2016-03-01

from celery import Celery
from settings import redis_host, redis_port
from log import logger
from tasks import request_worker

celery = Celery('tasks', broker='redis://%s:%s/0'%(redis_host, redis_port)) 

# bind 表示开启, max_retries 是重新尝试的次数,default_retry_delay 是默认的间隔时间，尝试的时间
@celery.task
def exec_request_task():
    try:
        logger.info('exec_request_task start!')
        success = request_worker.run()
        if success is False:
            logger.error('exec_request_task Failed')
            raise
        else:
            logger.info('exec_request_task Success')
            
    except Exception, e:
        logger.info('exec_task_order_overtime retry, Reason[%s]' % e)
        return
    
