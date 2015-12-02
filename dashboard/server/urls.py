from django.conf.urls import url
from django.views.generic import DeleteView
from views import *

urlpatterns = [
    url(r'^overview/$', IndexView.as_view() ,name='server_overview'),

    url(r'^monitor/$', MonitorView.as_view() ,name='server_monitor'),
    url(r'^monitor/(?P<pk>\d+)/$', MonitorDetailView.as_view() ,name='server_detail'),


    url(r'^manager/$', ManagerView.as_view() ,name='server_manager'),
    url(r'^manager/add/$', ServerAddView.as_view() ,name='server_manager_add'),
    url(r'^manager/(?P<pk>\d+)/edit/$', ServerEditView.as_view() ,name='server_manager_edit'),
    url(r'^manager/(?P<pk>\d+)/delete/$', ServerDeleteView.as_view(), name='server_manager_delete'),

    url(r'^collector/$', CollectorView.as_view() ,name='server_collector'),
    url(r'^collector/(?P<pk>\d+)/$', CollectorView.as_view() ,name='server_collector_detail'),
    url(r'^collector/add/$', CollertorAddView.as_view() ,name='server_collector_add'),
    url(r'^collector/(?P<pk>\d+)/edit/$', CollertorEditView.as_view() ,name='server_collector_edit'),
    url(r'^collector/(?P<pk>\d+)/delete/$',
        DeleteView.as_view(model=Collector,
                           success_url=reverse_lazy('newtouch:server:server_collector')),
        name='server_collector_delete'),

    url(r'^rules/$', IndexView.as_view() ,name='server_rules'),
]