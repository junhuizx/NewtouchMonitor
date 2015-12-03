from django.views.generic import ListView
from dashboard.server.models import Server
from dashboard.openstack.models import OpenStackAgent
from dashboard.network.models import SyslogServerMysql

# Create your views here.
class IndexView(ListView):
    template_name = 'overview/index.html'
    queryset = []

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['server_num'] = len(Server.objects.all())
        context['openstack_num'] = len(OpenStackAgent.objects.all())
        context['network_num'] = len(SyslogServerMysql.objects.all())
        context['service_num'] = 0

        return context
