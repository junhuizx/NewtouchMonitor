import json
from socket import socket, AF_INET, SOCK_STREAM

from django.views import generic

from models import *
from api.hostInfo import HostInfo


# Agent Information
AGENT_IP = 'localhost'
AGENT_PORT = 80
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
            tcpCliSocket.send('get')
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

class ManagerHypervisorsAddView(generic.FormView):
    pass

