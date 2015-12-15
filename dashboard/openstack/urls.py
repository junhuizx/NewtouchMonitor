from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DeleteView, ListView

import views
# from views import OpenStackHypervisorsView, OpenStackHypervisorDetailView
from models import OpenStackAgent


urlpatterns = [
    url(r'^index/$', ListView.as_view(model=OpenStackAgent,template_name='openstack/index.html') ,name='openstack_index'),
    url(r'^add/$', views.OpenStackAgentAddView.as_view() ,name='openstack_agent_add'),
    # url(r'^(?P<pk>\d+)/$', views.OpenStackHypervisorsView.as_view() ,name='hypervisors'),
    url(r'^(?P<pk>\d+)/edit/$', views.OpenStackAgentEditView.as_view() ,name='openstack_agent_edit'),
    url(r'^(?P<pk>\d+)/delete/$',
        DeleteView.as_view(model=OpenStackAgent,
                           success_url=reverse_lazy('newtouch:openstack:openstack_index')) ,name='openstack_agent_delete'),

    url(r'^hypervisors/$', views.OpenStackHypervisorsView.as_view() ,name='hypervisors'),
    url(r'^hypervisors/(?P<hypervisor_hostname>\w+)/$', views.OpenStackHypervisorDetailView.as_view(), name='openstack_hypervisors_detail'),

    url(r'^net/(?P<pk>\d+)/$', views.OpenStackNetStatus.as_view() ,name='net'),

#     url(r'^(?P<pk>\d+)/uuid/$', views.InstanceUUID.as_view() ,name='instance_uuid'),
    url(r'^uuid/$', views.InstanceUUID.as_view() ,name='instance_uuid'),
    url(r'^detail/$', views.InstanceDetailView.as_view() ,name='instance_detail'),
    url(r'^data/$', views.ChartData.as_view() ,name='instance_data'),
]
