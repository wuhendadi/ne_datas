#-*-coding:utf-8-*-
#Date:  2017��2��28��
#Auth:  zhaojunwang272

import os
import logging.config
import yaml

LOGPATH = ("d:/var/log" if os.path.exists("d:/var/log") else '/var/log') + '/pprc'
if not os.path.exists(LOGPATH): os.makedirs(LOGPATH)
file = os.path.join(os.path.dirname(__file__), 'default_log.yaml')
logging.config.dictConfig(yaml.load(open(file, 'r')))

logger = logging.getLogger("spyne.protocol.xml")
task_logger = logging.getLogger("apscheduler")