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
from api.socketPOperation import SocketOpt


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

        collertors = list(set([hypervisor.collector for hypervisor in context['hypervisors']]))
        data = []
        for collertor in collertors:
            hostnames = [ hypervisor.hostname for hypervisor in collertor.collector_hypervisors.all()]
            hostnames = list(set(hostnames))
            socket = SocketOpt()
            data.extend(socket.getMonitorData(hostnames,collertor.hostname, collertor.port))

        hosts = [HostInfo(info_dict) for info_dict in data]

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

# class HypervisorDeleteView(generic.DeleteView):
#     success_url =  reverse_lazy('newtouch:hypervisors:hypervisors_manager')
#     model = Hypervisors

class CollectorView(generic.ListView):
    model = Collector
    template_name = 'hypervisors/collertor.html'
    context_object_name = 'collertors'

    def get_context_data(self, **kwargs):
        context = super(CollectorView, self).get_context_data(**kwargs)
        status = []
        for collector in context['collertors']:
            one_status = True
            # stauts = test_collertor(collector.hostname, collector.port)
            status.append(one_status)

        context['collertors'] = zip(context['collertors'], status)
        return  context


class CollectorDetailView(generic.DetailView):
    model = Collector
    template_name = 'hypervisors/collertor.html'
    context_object_name = 'collertor'

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

# class CollertorDeteleView(generic.DeleteView):
#     pass