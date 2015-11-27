
#-*-coding: utf-8-*-
from socket import socket, AF_INET, SOCK_STREAM
import json
import logging

BUFSIZ = 1024*1024

class SocketOpt(object):

    def __init__(self):
        super(SocketOpt, self).__init__()

    def getMonitorData(self, monitor_list, hostIP='', port=18888):
        if not isinstance(monitor_list, list) or not monitor_list:
            return json.dumps({})
		
        ADDR = (hostIP, port)
        tcpCliSocket = socket(AF_INET, SOCK_STREAM)
        jData = json.dumps({'get' : monitor_list})

        try:
            tcpCliSocket.connect(ADDR)
            tcpCliSocket.send(jData)
            jWebData = tcpCliSocket.recv(BUFSIZ)
            data = json.loads(jWebData)
        except Exception,e:
            print str(e)
            data = []
        finally:
            tcpCliSocket.close()
            return data