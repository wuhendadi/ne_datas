#-*-coding:utf-8-*-
#Date:  2017年3月6日
#Auth:  zhaojunwang272

import os
import xlrd
import time
from log import task_logger as logger
from datas import db_base
from settings import xlsx_path
from tools.utilfunc import _get_value


def sync_xlsx_list(colnameindex=0):
    try:
        start_time = time.time()
        logger.info(u'parse xlsx......')
        if os.path.exists(xlsx_path):
            data = xlrd.open_workbook(xlsx_path)
            table_sheet = data.sheet_by_index(colnameindex)        
            for rownum in xrange(1, table_sheet.nrows): 
                row = table_sheet.row_values(rownum)
                if row and len(row) > 1:
                    key = 'link:%s:link'%row[0]
                    ne_ip, port_id = row[0].split("_")[0], row[0].split("_")[1]
                    tmp_dict = {"linkid":row[0], "linkname":row[1], "userlabel":row[2], "linkstatus":row[3], 
                                "aport":row[4], "zport":row[5], "rate":row[6], "linktype":row[7]}
                    
                    port_info = db_base.session_get("ne:zj_%s:fm:%s:st:%s:ems:%s:port:%s:port"%(ne_ip, ne_ip, ne_ip, port_id, port_id))
                    tmp_dict["rate"] = _get_value(port_info, "rate", "1G")
                    tmp_dict["linkstatus"] = _get_value(port_info, "usestatus", "up")
                    
                    db_base.session_insert(key, tmp_dict)
                     
    except Exception,e:
        logger.info('Import Excel[%s] Failed! Reason:[%s]'%(xlsx_path, e))
        
    logger.info("Sync_xlsx_list Complete! cast %ss"%(time.time() - start_time))
    
        
