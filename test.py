#-*-coding:utf-8-*-
#Date:  2017年3月2日
#Auth:  zhaojunwang272

from lxml import etree
#from spyne.util.xml import get_object_as_xml
from suds.client import Client
from services.utils import Neobjlist, Cardobjlist
from spyne import Array, Unicode
#from services.utils import SysVenderResultModel


#===============================================================================
# client = Client(url, cache=None)
# client.service.passiveSetNePortVender(Cardobjlist(emssn = 'ne:zj_10.10.0.3:fm:10.10.0.3:st:10.10.0.3:ems:3'))
# req = str(client.last_sent())           # 保存请求报文，因为返回的是一个实例，所以要转换成str
# response = str(client.last_received())  # 保存返回报文，返回的也是一个实例
# print req       # 打印请求报文
# print response  # 打印返回报文
#===============================================================================
    
for i in xrange(10):
    for j in xrange(10):
        yield i+j
        