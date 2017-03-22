#-*-coding:utf-8-*-
# auth: ZJW
# Date: 2016-03-01

import sys
import datetime, time
import thread
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED
from log import task_logger
from tasks.request_worker import sync_device_list, sync_alarm_list, sync_perf_list
from tasks.xlsx_parser import sync_xlsx_list
from tasks.snmp_worker import sync_snmp_info

scheduler = BackgroundScheduler()
 
def err_listener(ev):
    if ev.exception:  
        task_logger.error('%s error.', str(ev.job))  
    else:  
        task_logger.info('%s miss', str(ev.job))  
  
scheduler.add_listener(err_listener, EVENT_JOB_ERROR | EVENT_JOB_MISSED) 

def start_task(): 
    scheduler.add_job(sync_device_list, 'interval', next_run_time=datetime.datetime.now(), seconds=60)
    scheduler.add_job(sync_alarm_list, 'interval', next_run_time=datetime.datetime.now(), seconds=60)
    scheduler.add_job(sync_perf_list, 'interval', next_run_time=datetime.datetime.now(), seconds=60)
    scheduler.add_job(sync_snmp_info, 'interval', next_run_time=datetime.datetime.now(), seconds=300)
    scheduler.add_job(sync_xlsx_list, 'interval', next_run_time=datetime.datetime.now(), seconds=600)
    scheduler.start()
    
    
if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')
    thread.start_new_thread(start_task, ())
    while 1:
        cur_time = time.localtime()
        #TODO: do something everyday 00:00:00 clock
        offset = 24 * 3600 - cur_time.tm_hour * 3600 - cur_time.tm_min * 60 - cur_time.tm_sec
        time.sleep(offset)
        
    
        