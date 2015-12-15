# -*- coding: utf-8 -*-
import json, pprint
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.forms.utils import ErrorList

from django.views.generic import ListView, DetailView, FormView, View, TemplateView
import requests
from api.openstack_api import OpenStackAgentClient
from models import OpenStackAgent
from forms import OpenStackAgentAddForm, OpenStackAgentEditForm
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

class OpenStackHypervisor(object):
    def __init__(self, hypervisor):
        self.network_status = None
        self.status = hypervisor['status']
        self.hypervisor_hostname = hypervisor['hypervisor_hostname']
        self.hypervisor_type = hypervisor['hypervisor_type']
        self.host_ip = hypervisor['host_ip']
        self.network_status = hypervisor['network_status']
        self.vcpus = hypervisor['vcpus']
        self.vcpus_used = hypervisor['vcpus_used']
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
        return self.hypervisor_hostname


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
        return super(OpenStackAgentAddView, self).post(request, *args, **kwargs)


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
        return super(OpenStackAgentEditView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        agent = OpenStackAgent.objects.get(pk=kwargs.get('pk'))
        self.initial = {
            'id': kwargs.get('pk'),
            'name': agent.name,
            'hostname': agent.hostname,
            'port': agent.port,
            'guest_agent_base_url': agent.guest_agent_base_url
        }

        return super(OpenStackAgentEditView, self).get(request, *args, **kwargs)

class OpenStackHypervisorsView(ListView):
    template_name = 'openstack/openstack_hypervisors.html'
    queryset = []

    def get_context_data(self, **kwargs):
        context = super(OpenStackHypervisorsView, self).get_context_data(**kwargs)
        hypervisors_tmp = []
        context['openstacks'] = OpenStackAgent.objects.all()
        context['tag'] = self.request.GET.get('tag')
        if context['tag']:
            context['tag'] = int(context['tag'])
            openstack = OpenStackAgent.objects.get(id=context['tag'])
        else:
            openstack = OpenStackAgent.objects.get(id=1)

        context['hypervisors'] = []
        client = OpenStackAgentClient(openstack.hostname, openstack.port)
        hypervisors = client.hypervisor_list()
        hypervisors_hostname = hypervisors.keys()

        for hypervisor in hypervisors_hostname:
            hypervisors_tmp.append(OpenStackHypervisor(hypervisors[hypervisor]))

        context['hypervisors'] = hypervisors_tmp

        return context

class OpenStackInstancesView(ListView):
    template_name = 'openstack/openstack_instances_status.html'
    queryset = []

    def get_context_data(self, **kwargs):
        context = super(OpenStackInstancesView, self).get_context_data(**kwargs)
        context['openstacks'] = OpenStackAgent.objects.all()
        context['tag'] = self.request.GET.get('tag')
        if context['tag']:
            context['tag'] = int(context['tag'])
            openstack = OpenStackAgent.objects.get(id = context['tag'])
        else:
            openstack = OpenStackAgent.objects.get(id = 1)

        client = OpenStackAgentClient(openstack.hostname, openstack.port)
        instances = client.instances_status_list()['object']

        context['instances_status'] = []
        for instance in instances:
            context['instances_status'].append(HostNetInfo(instance))

        return context

class OpenStackNovaServicesView(ListView):
    template_name = 'openstack/openstack_nova_services.html'
    queryset = []

    def get_context_data(self, **kwargs):
        context = super(OpenStackNovaServicesView, self).get_context_data(**kwargs)
        context['openstacks'] = OpenStackAgent.objects.all()
        context['tag'] = self.request.GET.get('tag')
        if context['tag']:
            context['tag'] = int(context['tag'])
            openstack = OpenStackAgent.objects.get(id=context['tag'])
        else:
            openstack = OpenStackAgent.objects.get(id=1)

        client = OpenStackAgentClient(openstack.hostname, openstack.port)
        services = client.nova_service_list()
        services_host = services.keys()

        context['nova_services'] = []
        for service in services_host:
            context['nova_services'].append(OpenStackNovaService(services[service]))

        return context