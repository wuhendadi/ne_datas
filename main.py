#-*-coding:utf-8-*-
# auth: ZJW
# Date: 2016-03-01

#import thread
import sys
from spyne import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from services.webapi import DeviceService
from wsgiref.simple_server import make_server
from log import logger
#from tasks import task_ctrl
from settings import webhost, webport


def main():
    
    logger.info('*********************WebService Run*******************')
    application = Application([DeviceService], 'spyne.device.soap',
                              in_protocol=Soap11(validator='lxml'),
                              out_protocol=Soap11())

    wsgi_application = WsgiApplication(application)
    logger.info("wsdl is at: http://%s:%s/?wsdl"%(webhost, webport))
    server = make_server(webhost, webport, wsgi_application)
    #thread.start_new_thread(task_ctrl.start_task, ())
    server.serve_forever()

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    main()
    
