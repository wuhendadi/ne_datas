# -*-coding:utf-8-*-
# auth: ZJW
# Date: 2017-02-08

#default
webhost    = '127.0.0.1'
webport    = 8000
sys_name   = u'设备网管系统'
user_label = 'operator'
version    = '0.0.1'
xml_path   = './xmls'
xlsx_path  = u'./xlsxs/链路数据.xlsx'

device_category = ['Switch', 'Router']

#redis
redis_host = '127.0.0.1'
redis_port = 6379


#url
api_host   = '60.190.251.203'
api_port   = '12390'
api_key    = '5a1f39b05a4f2708b048b3852f12f7ca'

alarm_host = '60.190.251.203'
alarm_port = '12390'
alarm_key  = '5a1f39b05a4f2708b048b3852f12f7ca'

#ftp
ftp_user   = 'ftp'
ftp_pwd    = 'zjdl'
ftp_host   = '192.168.2.111'
ftp_port   = 21
ftp_path   = 'home'


#snmp
snmp_group = 'public'


#server
server_url = 'http://127.0.0.1:8000/?wsdl'


#oids
oid_list = {
            "Cisco Catalyst 4500":{"configoids":{"runtime":".1.3.6.1.2.1.1.3", "soft_version":"1.3.6.1.2.1.47.1.1.1.1.10.1"},
                                   "frame":{'frameid':'.1.3.6.1.2.1.1.3',"framename":".1.3.6.1.2.1.1.3"},
                                   "slot":{'soltid':'.1.3.6.1.2.1.1.3',"soltname":".1.3.6.1.2.1.1.3"},
                                   "card":{'cardid':'.1.3.6.1.2.1.1.3',"cardname":".1.3.6.1.2.1.1.3"},
                                   "interface":{'interfaceid':'.1.3.6.1.2.1.1.3',"interfacename":".1.3.6.1.2.1.1.3"},              
                                   },
            "dell":{}
            }

