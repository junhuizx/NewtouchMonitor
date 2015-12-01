
# -*- coding:utf-8 -*-
import urllib2
import json
import logging
import ConfigParser


BUFSIZ = 1024*1024

class ClientAPI(object):
	def __init__(self):
		super(ClientAPI, self).__init__()
				
	@staticmethod
	def getHyperInfo(agent_IP, port):
		req_url = 'http://'+str(agent_IP)+':'+str(port)+'/instance/'
		print req_url
		headers = {'content-type': 'application/json',"Accept": "application/json"}
		req = urllib2.Request(url=req_url, headers=headers)
		try:
			response = urllib2.urlopen(req)
			hosts_info_list = json.loads(response.read())
		except:
			logging.warn('Fial to connect agent!')
			hosts_info_list = []
		return hosts_info_list


	@staticmethod
	def setHostIPToCfg(host_IP, add_to_config = True):
		cfg_name = 'config'
		section = 'HostIP'
		option = 'Hosts'
		
		if not isinstance(host_IP, str):
			host_IP = json.dumps(host_IP)
		cfg_obj = ConfigOpt()
		hosts = json.loads(cfg_obj.readCfg(cfg_name, section, option))
		if add_to_config:
			if host_IP in hosts:
				raise Exception, 'The host_IP is already existed!'
			else:
				hosts.append(host_IP)
		else:
			try:
				hosts.remove(host_IP)
			except Exception, error:
				raise error
		cfg_obj.setCfg(cfg_name, section, option, json.dumps(hosts))
		return True



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
