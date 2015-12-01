from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DeleteView, ListView

from views import OpenStackHypervisorsView, OpenStackHypervisorDetailView, OpenStackAgentAddView,OpenStackAgentEditView
from models import OpenStackAgent


urlpatterns = [
    url(r'^index/$', ListView.as_view(model=OpenStackAgent,template_name='openstack/index.html') ,name='openstack_index'),
    url(r'^add/$', OpenStackAgentAddView.as_view() ,name='openstack_agent_add'),
    url(r'^(?P<pk>\d+)/edit/$', OpenStackAgentEditView.as_view() ,name='openstack_agent_edit'),
    url(r'^(?P<pk>\d+)/delete/$',
        DeleteView.as_view(model=OpenStackAgent,
                           success_url=reverse_lazy('newtouch:openstack:openstack_index')) ,name='openstack_agent_delete'),

    url(r'^hypervisors/(?P<pk>\d+)/$', OpenStackHypervisorsView.as_view(),name='openstack_hypervisors'),
    url(r'^hypervisors/(?P<pk>\d+)/(?P<hypervisor_hostname>\w+)/$', OpenStackHypervisorDetailView.as_view(), name='openstack_hypervisors_detail'),
]
