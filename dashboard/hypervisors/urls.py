from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'^overview/$', IndexView.as_view() ,name='hypervisors_overview'),

    url(r'^monitor/$', MonitorView.as_view() ,name='hypervisors_monitor'),
    url(r'^monitor/(?P<pk>\d+)/$', MonitorDetailView.as_view() ,name='hypervisor_detail'),

    url(r'^manager/$', ManagerView.as_view() ,name='hypervisors_manager'),
    url(r'^manager/add/$', HypervisorAddView.as_view() ,name='hypervisors_manager_add'),
    url(r'^manager/(?P<pk>\d+)/edit/$', HypervisorEditView.as_view() ,name='hypervisors_manager_edit'),
    url(r'^manager/(?P<pk>\d+)/delete/$', IndexView.as_view() ,name='hypervisors_manager_delete'),

    url(r'^collector/$', CollectorView.as_view() ,name='hypervisors_collector'),

    url(r'^rules/$', IndexView.as_view() ,name='hypervisors_rules'),
]