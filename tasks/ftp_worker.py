#-*-coding:utf-8-*-
#Date:  2017年3月3日
#Auth:  zhaojunwang272

import os
import time
from ftplib import FTP
from lxml import etree
from spyne.util.xml import get_object_as_xml
from log import task_logger as logger
from settings import ftp_host, ftp_port, ftp_path, ftp_user, ftp_pwd, xml_path

BUFFER_SIZE = 1024

def _init_ftp():
    ftp = FTP() 
    ftp.set_debuglevel(2)
    #打开调试级别2，显示详细信息;0为关闭调试信息 
    ftp.connect(ftp_host, ftp_port)
    ftp.login(ftp_user, ftp_pwd)
    return ftp
    
 
def ftp_up(filename, target_path=None): 
    ftp = _init_ftp() 
    if target_path: ftp.cwd(target_path)
    file_handler = open(filename,'rb')
    ftp.storbinary('STOR %s' % os.path.basename(filename), file_handler, BUFFER_SIZE)
    ftp.set_debuglevel(0) 
    file_handler.close() 
    ftp.quit() 
    logger.info("ftp up OK")
 
def ftp_down(filename, target_path=ftp_path): 
    ftp = _init_ftp()
    ftp.cwd(ftp_path) 
    file_handler = open(os.path.join(target_path, filename),'wb').write
    ftp.retrbinary('RETR %s' % os.path.basename(filename), file_handler, BUFFER_SIZE)
    ftp.set_debuglevel(0) 
    file_handler.close() 
    ftp.quit() 
    logger.info("ftp down OK") 
    

def ftp_up_xml(target_obj, target_model, filename):
    if not os.path.exists(xml_path): os.makedirs(xml_path)
    filename = os.path.join(xml_path, '%s_%s.xml'%(filename, time.time()))
    xml_str = etree.tostring(get_object_as_xml(target_obj, target_model), pretty_print=True)
    
    print xml_str
    
    with open(filename, 'wb') as infile: 
        infile.write(xml_str.replace("ns0:", ""))
        
    ftp_up(filename)

if __name__ == '__main__':
    ftp_up('c:/report.evt')
    
    

    
    
    