import json,pprint

from django.views.generic import ListView, DetailView
from api.openstack_api import OpenStackAgentClient
from models import OpenStackAgent

class OpenStackServer(object):
    def __init__(self, server):
        self.uuid = server['uuid']
        self.name = server['name']

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
        context['servers'] = []

        hypervisor_hostname = self.kwargs['hypervisor_hostname']
        agent = OpenStackAgent.objects.get(pk = self.kwargs['pk'])
        client = OpenStackAgentClient(agent.hostname, agent.port)
        servers = client.hypervisor_server_list(hypervisor_hostname)['servers']
        for server in servers:
            context['servers'].append(OpenStackServer(server))

        return context
