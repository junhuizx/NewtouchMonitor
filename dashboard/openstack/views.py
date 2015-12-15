# -*- coding: utf-8 -*-

import json,pprint
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.forms.utils import ErrorList

from django.views.generic import ListView, DetailView, FormView, View, TemplateView
import requests
from api.openstack_api import OpenStackAgentClient
from models import OpenStackAgent
from forms import OpenStackAgentAddForm,OpenStackAgentEditForm
from django.conf import settings
from django.http import HttpResponse
from api.redisPOperation import RedisHashOprt
from api.hostInfo import HostNetInfo



UUID = None
OPS_AGENT = None


class OpenStackNovaService(object):
    def __init__(self, service):
        self.host = service['host']
        self.service = service['binary']
        self.zone = service['zone']
        self.status = service['status']
        self.state = service['state']
        self.reason = service['disabled_reason']

    def __unicode__(self):
        return self.host

class OpenStackServer(object):
    def __init__(self, server, project_id):
        self.uuid = server['uuid']
        self.name = server['name']
        self.project_id = project_id

    def fill_instance(self, base_url, token):
        url = 'http://%s:8774' % (base_url) + "/v2/%s/guest/%s" % (self.project_id, self.uuid)
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
        self.network_status = None
        self.status = hypervisor['status']
        self.hypervisor_hostname = hypervisor['hypervisor_hostname']
        self.hypervisor_type = hypervisor['hypervisor_type']
        self.host_ip = hypervisor['host_ip']
	self.network_status = hypervisor['network_status']
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
        hypervisors_tmp = []
        context['services'] = []

        context['agent_pk'] = self.kwargs['pk']
        agent = OpenStackAgent.objects.get(pk = self.kwargs['pk'])
        client = OpenStackAgentClient(agent.hostname, agent.port)
        hypervisors = client.hypervisor_list()
        services = client.nova_service_list()
        hypervisors_hostname = hypervisors.keys()
        services_host = services.keys()
        for hypervisor in hypervisors_hostname:
            hypervisors_tmp.append(OpenStackHypervisor( hypervisors[hypervisor] ))

        context['hypervisors'] = hypervisors_tmp
        for service in services_host:
            context['services'].append(OpenStackNovaService(services[service]))

        return context

class OpenStackHypervisorDetailView(ListView):
    template_name = 'openstack/instances.html'
    queryset = []

    def get_context_data(self, **kwargs):
        context = super(OpenStackHypervisorDetailView, self).get_context_data(**kwargs)
        context['instances'] = []
        context['ops_agent'] = self.kwargs['pk']
        hypervisor_hostname = self.kwargs['hypervisor_hostname']
        agent = OpenStackAgent.objects.get(pk = self.kwargs['pk'])
        client = OpenStackAgentClient(agent.hostname, agent.port)
        instances = client.hypervisor_server_list(hypervisor_hostname)['servers']

        token = client.get_token()['token']
        for instance in instances:
            project_id = client.get_project_id()['project_id']

            instance = OpenStackServer(instance, project_id)
            instance.fill_instance(agent.guest_agent_base_url ,token)
            context['instances'].append(instance)

        return context

class OpenStackAgentAddView(FormView):
    form_class = OpenStackAgentAddForm
    success_url = reverse_lazy('newtouch:openstack:openstack_index')
    template_name = 'openstack/openstack_agent_add.html'

    def post(self, request, *args, **kwargs):
        form = OpenStackAgentAddForm(request.POST)
        if form.is_valid():
            try:
                OpenStackAgent.objects.get(name=form.cleaned_data['name'])
                errors = form._errors.setdefault("name", ErrorList())
                errors.append(u"OpenStack Agent name had already used!")
                return self.form_invalid(form=form)
            except ObjectDoesNotExist:
                form.save(form)
        else:
            return self.form_invalid(form=form)
        return super(OpenStackAgentAddView,self).post(request, *args, **kwargs)

class OpenStackAgentEditView(FormView):
    form_class = OpenStackAgentEditForm
    required_css_class = 'required'
    success_url = reverse_lazy('newtouch:openstack:openstack_index')
    template_name = 'openstack/openstack_agent_edit.html'

    def post(self, request, *args, **kwargs):
        form = OpenStackAgentEditForm(request.POST)
        if form.is_valid():
                form.save(form)
        else:
            return self.form_invalid(form=form)
        return super(OpenStackAgentEditView,self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        agent = OpenStackAgent.objects.get(pk=kwargs.get('pk'))
        self.initial = {
            'id': kwargs.get('pk'),
            'name' : agent.name,
            'hostname': agent.hostname,
            'port': agent.port,
            'guest_agent_base_url': agent.guest_agent_base_url
        }

        return super(OpenStackAgentEditView, self).get(request,*args, **kwargs)

class OpenStackNetStatus(ListView):
    template_name = 'openstack/net.html'
    queryset = []
    
    def get_context_data(self, **kwargs):
        context = super(OpenStackNetStatus, self).get_context_data(**kwargs)
        agent= OpenStackAgent.objects.get(id=self.kwargs['pk'])
        client = OpenStackAgentClient(agent.hostname, agent.port)        
        context['instances'] = []
        net_dics = client.net_list()['object']
        net_infos = [HostNetInfo(info_dic) for info_dic in net_dics]
        context['instances'].extend(net_infos)
        return context

    
class InstanceUUID(View):
    def get(self, request):
        global UUID
        global OPS_AGENT
        UUID = request.GET.get('uuid')
        OPS_AGENT = request.GET.get('ops_agent')

        return HttpResponse(json.dumps({}),
                            content_type='application/json')

class ChartData(View):
    def get(self, request):
        global UUID
        global OPS_AGENT
        agent = OpenStackAgent.objects.get(pk=int(OPS_AGENT))
        redis_ip = agent.guest_agent_base_url
        redis_port = 6379
        hash_name = 'hash_data'
        list_name = 'list:'+str(UUID)
        
        try:
            redis_obj = RedisHashOprt(redis_ip, redis_port)
            keys_list = redis_obj.getListValue(list_name)
            data = redis_obj.getInstanceData(hash_name, keys_list)
            return HttpResponse(json.dumps(data),
                            content_type='application/json')
        except:
            return HttpResponse(json.dumps({}),
                            content_type='application/json')


class InstanceDetailView(TemplateView):
    template_name = 'openstack/instance_detail.html'
    def get_context_data(self, **kwargs):
        context = super(InstanceDetailView, self).get_context_data(**kwargs)
        return context
