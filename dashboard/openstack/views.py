# -*- coding: utf-8 -*-

import json,pprint

from django.views.generic import ListView, DetailView
import requests
from api.openstack_api import OpenStackAgentClient
from models import OpenStackAgent
from django.conf import settings

class OpenStackServer(object):
    def __init__(self, server, project_id):
        self.uuid = server['uuid']
        self.name = server['name']
        self.project_id = project_id

    def fill_instance(self, token):
        url = settings.REDIS_BASE_URL + "/v2/%s/guest/%s" % (self.project_id, self.uuid)
        headers = {'X-Auth-Token': '%s' % (token)}
        re = requests.get(url, headers=headers, verify =False)

        return_data = json.loads(re.text)
        if return_data['return']:
            self.return_data = True
            data_dict =  eval(return_data['return'])
            self.memstat = data_dict['memstat']
            self.netstat = data_dict['netstat']
            self.diskstat = data_dict['diskstat']
            self.processstat = data_dict['processstat']
            self.login = data_dict['login']
        else:
            self.return_data = False

    def __unicode__(self):
        return  self.name

class OpenStackHypervisor(object):
    def __init__(self , hypervisor):
        self.status = hypervisor['status']
        self.hypervisor_hostname = hypervisor['hypervisor_hostname']
        self.hypervisor_type = hypervisor['hypervisor_type']
        self.host_ip = hypervisor['host_ip']
        self.vcpus = hypervisor['vcpus']
        self.vcpus_used =hypervisor['vcpus_used']
        self.memory_mb_used = int(hypervisor['memory_mb_used'])
        self.memory_used = self.memory_mb_used * 1024 * 1024
        self.memory_mb = int(hypervisor['memory_mb'])
        self.memory = self.memory_mb * 1024 * 1024
        self.local_gb_used = int(hypervisor['local_gb_used'])
        self.local_used = self.local_gb_used * 1024 * 1024 * 1024
        self.local_gb = int(hypervisor['local_gb'])
        self.local = self.local_gb * 1024 * 1024 * 1024
        self.current_workload = hypervisor['current_workload']
        self.state = hypervisor['state']
        self.running_vms = hypervisor['running_vms']
        self.free_disk_gb = hypervisor['free_disk_gb']
        self.hypervisor_version = hypervisor['hypervisor_version']
        self.disk_available_least = hypervisor['disk_available_least']
        self.free_ram_mb = hypervisor['free_ram_mb']
        self.id = hypervisor['id']

    def __unicode__(self):
        return  self.hypervisor_hostname


class OpenStackHypervisorsView(ListView):
    template_name = 'openstack/hypervisors.html'
    queryset = []

    def get_context_data(self, **kwargs):
        context = super(OpenStackHypervisorsView, self).get_context_data(**kwargs)
        context['hypervisors'] = []

        context['agent_pk'] = self.kwargs['pk']
        agent = OpenStackAgent.objects.get(pk = self.kwargs['pk'])
        client = OpenStackAgentClient(agent.hostname, agent.port)
        hypervisors = client.hypervisor_list()
        hypervisors_hostname = hypervisors.keys()
        for hypervisor in hypervisors_hostname:
            context['hypervisors'].append(OpenStackHypervisor( hypervisors[hypervisor] ))

        return context

class OpenStackHypervisorDetailView(ListView):
    template_name = 'openstack/instances.html'
    queryset = []

    def get_context_data(self, **kwargs):
        context = super(OpenStackHypervisorDetailView, self).get_context_data(**kwargs)
        context['instances'] = []

        hypervisor_hostname = self.kwargs['hypervisor_hostname']
        agent = OpenStackAgent.objects.get(pk = self.kwargs['pk'])
        client = OpenStackAgentClient(agent.hostname, agent.port)
        instances = client.hypervisor_server_list(hypervisor_hostname)['servers']

        token = client.get_token()['token']
        for instance in instances:
            project_id = client.get_project_id()['project_id']
            instance = OpenStackServer(instance, project_id)
            instance.fill_instance(token)
            context['instances'].append(instance)

        return context
