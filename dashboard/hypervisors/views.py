from django.views import generic
from models import *

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'hypervisors/index.html'

class MonitorView(generic.ListView):
    template_name = 'hypervisors/monitor.html'
    queryset = []

class MonitorDetailView(generic.DetailView):
    template_name = 'hypervisors/monitor_detail.html'

