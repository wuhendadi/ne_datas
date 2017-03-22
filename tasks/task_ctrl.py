#-*-coding:utf-8-*-
# auth: ZJW
# Date: 2016-03-01

import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED
from log import logger
from tasks.request_worker import sync_device_list, sync_alarm_list, sync_perf_list

scheduler = BackgroundScheduler()
 
def err_listener(ev):
    if ev.exception:  
        logger.exception('%s error.', str(ev.job))  
    else:  
        logger.info('%s miss', str(ev.job))  
  
scheduler.add_listener(err_listener, EVENT_JOB_ERROR | EVENT_JOB_MISSED) 

def start_task(): 
    scheduler.add_job(sync_device_list, 'interval', next_run_time=datetime.datetime.now(), seconds=60)
    scheduler.add_job(sync_alarm_list, 'interval', next_run_time=datetime.datetime.now(), seconds=60)
    scheduler.add_job(sync_perf_list, 'interval', next_run_time=datetime.datetime.now(), seconds=60)
    scheduler.start()
    