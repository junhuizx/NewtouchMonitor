# -*- coding: utf-8 -*-

import json
from socket import socket, AF_INET, SOCK_STREAM
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.utils.encoding import force_text

from django.views import generic
from django.core.urlresolvers import reverse_lazy, reverse

from models import *
from forms import HypervisorsAddForm, HypervisorsEditForm, CollertorAddForm
from api.hostInfo import HostInfo


# Agent Information
AGENT_IP = '223.167.85.2'
AGENT_PORT = 30024
ADDR = (AGENT_IP, AGENT_PORT)
BUFSIZ = 1024*1024

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'hypervisors/index.html'

class MonitorView(generic.ListView):
    template_name = 'hypervisors/monitor.html'
    queryset = []

    def get_context_data(self, **kwargs):
        context = super(MonitorView, self).get_context_data(**kwargs)
        context['idcs'] = IDC.objects.all()
        context['tag'] = self.request.GET.get('tag')
        if context['tag']:
            idc = IDC.objects.get(name=context['tag'])
        else:
            idc = IDC.objects.get(name='ShangHai')
        context['hypervisors'] = Hypervisors.objects.filter(location_id = idc.id)

        tcpCliSocket = socket(AF_INET, SOCK_STREAM)
        try:
            tcpCliSocket.connect(ADDR)
            data = {'get':['172.16.17.110','172.16.17.120']}
            tcpCliSocket.send(json.dumps(data))
            web_data = tcpCliSocket.recv(BUFSIZ)
            data = json.loads(web_data)
            hosts = [HostInfo(info_dict) for info_dict in data]
            tcpCliSocket.send('release')
            tcpCliSocket.close()
        except:
            hosts = []
        context['hosts'] = hosts
        return context

class MonitorDetailView(generic.DetailView):
    template_name = 'hypervisors/monitor_detail.html'

class ManagerView(generic.ListView):
    template_name = 'hypervisors/manager.html'
    queryset = []

    def get_context_data(self, **kwargs):
        context = super(ManagerView,self).get_context_data(**kwargs)
        context['idcs'] = IDC.objects.all()
        context['tag'] = self.request.GET.get('tag')
        if context['tag']:
            idc = IDC.objects.get(name=context['tag'])
        else:
            idc = IDC.objects.get(name='ShangHai')
        context['hypervisors'] = Hypervisors.objects.filter(location_id = idc.id)

        return context

class HypervisorAddView(generic.FormView):
    form_class = HypervisorsAddForm
    success_url = reverse_lazy('newtouch:hypervisors:hypervisors_manager')
    template_name = 'hypervisors/manager_add.html'

    def post(self, request, *args, **kwargs):
        form = HypervisorsAddForm(request.POST)
        if form.is_valid():
            print form.cleaned_data
            try:
                form.save(form)
            except Exception,e:
                return self.form_invalid(form=form)
        else:
            return self.form_invalid(form=form)
        return super(HypervisorAddView,self).post(request, *args, **kwargs)


class HypervisorEditView(generic.FormView):
    form_class = HypervisorsEditForm
    required_css_class = 'required'
    success_url = reverse_lazy('newtouch:hypervisors:hypervisors_manager')
    template_name = 'hypervisors/manager_edit.html'

    def get(self, request, *args, **kwargs):
        hypervisor = Hypervisors.objects.get(pk=kwargs.get('pk'))
        self.initial = {
            'id': kwargs.get('pk'),
            'hostname' : hypervisor.hostname,
            'location': hypervisor.location,
            'collector': hypervisor.collector,
            'user': hypervisor.user,
            'rules': hypervisor.rules.all(),
            'snmp_version': hypervisor.snmp_version,
            'snmp_commit': hypervisor.snmp_commit,
            'ssh_username':hypervisor.ssh_username ,
            'ssh_password':hypervisor.ssh_password
        }

        return super(HypervisorEditView,self).get(request,*args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = HypervisorsEditForm(request.POST)
        if form.is_valid():
            data =  form.cleaned_data
            try:
                form.save(form)
            except Exception,e:
                print str(e)
                return self.form_invalid(form=form)
        else:
            return self.form_invalid(form=form)

        return super(HypervisorEditView,self).post(request, *args, **kwargs)


class CollectorView(generic.ListView):
    model = Collector
    template_name = 'hypervisors/collertor.html'
    context_object_name = 'collertors'

class CollectorDetailView(generic.DetailView):
    model = Collector
    template_name = 'hypervisors/collertor.html'
    context_object_name = 'collertors'

class CollertorAddView(generic.FormView):
    form_class = CollertorAddForm
    success_url = reverse_lazy('newtouch:hypervisors:hypervisors_collector')
    template_name = 'hypervisors/collertor_add.html'

    def get(self, request, *args, **kwargs):
        Collectors = Collector.objects.all().order_by('-id')
        if Collectors:
            id = Collectors[0].id + 1
        else:
            id = 1
        self.initial = {
            'id': id,
            'key' : uuid.uuid4()
        }

        return super(CollertorAddView,self).get(request,*args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = CollertorAddForm(request.POST)
        if form.is_valid():
            print form.cleaned_data
            try:
                form.save(form)
            except Exception,e:
                return self.form_invalid(form=form)
        else:
            return self.form_invalid(form=form)
        return super(CollertorAddView,self).post(request, *args, **kwargs)

class CollertorEditView(generic.FormView):
    pass

class CollertorDeteleView(generic.FormView):
    pass