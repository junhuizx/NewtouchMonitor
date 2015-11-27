import requests
import json
import pprint

class OpenStackAgentClient(object):
    def __init__(self, hostname, port):
        self.base_url = 'http://%s:%d' % (hostname, port)
        self.headers = {'Content-Type': 'application/json'}

    def hypervisor_list(self):
        url = self.base_url + '/hypervisor'
        re = requests.get(url, headers=self.headers)

        return json.loads(re.text)

    def hypervisor_server_list(self, hypervisor):
        url = self.base_url + '/hypervisor-servers/%s' %(hypervisor)
        re = requests.get(url, headers=self.headers)

        return json.loads(re.text)

