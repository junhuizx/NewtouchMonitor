# -*- coding:utf-8 -*-
import urllib2
import json
import logging
import ConfigParser

class ClientAPI(object):
    def __init__(self):
        super(ClientAPI, self).__init__()

    @staticmethod
    def getHyperInfo(agent_IP, port):
        req_url = 'http://' + str(agent_IP) + ':' + str(port) + '/instance/'
        print req_url
        headers = {'content-type': 'application/json', "Accept": "application/json"}
        req = urllib2.Request(url=req_url, headers=headers)
        try:
            response = urllib2.urlopen(req)
            hosts_info_list = json.loads(response.read())
        except:
            logging.warn('Fial to connect agent!')
            hosts_info_list = []
        return hosts_info_list

    @staticmethod
    def setHostIPToCfg(agent_IP, port, host_IP, add_to_config=True):
        req_url = 'http://' + str(agent_IP) + ':' + str(port) + '/config/add/' + str(host_IP) \
            if add_to_config else \
            'http://' + str(agent_IP) + ':' + str(port) + '/config/delete/' + str(host_IP)
        headers = {'content-type': 'application/json', 'Accept': 'application/json'}
        req = urllib2.Request(url=req_url, headers=headers)
        try:
            response = urllib2.urlopen(req)
            data = json.loads(response.read())
            result = True if data['flag'] == 'success' else False
        except:
            logging.warn('Fial to connect agent!')
            result = False
        return result


class ConfigOpt(object):
    def __init__(self):
        super(ConfigOpt, self).__init__()
        self.config = ConfigParser.RawConfigParser()

    def readCfg(self, cfg_name, section, option):
        self.config.read(cfg_name)
        return self.config.get(section, option)

    def setCfg(self, cfg_name, section, option, json_value):
        self.config.set(section, option, json_value)
        with open(cfg_name, 'wb') as config_file:
            self.config.write(config_file)
