from django.conf.urls import url

from views import IndexView,MonitorView,MonitorDetailView

urlpatterns = [
    url(r'^overview/$', IndexView.as_view() ,name='overview'),
    url(r'^monitor/$', MonitorView.as_view() ,name='monitor'),
    url(r'^monitor/<?P(pk)\d+>/$', MonitorDetailView.as_view() ,name='hypervisor_detail'),
]