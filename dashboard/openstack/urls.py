from django.conf.urls import url
from django.views.generic import TemplateView, ListView

from views import OpenStackHypervisorsView, OpenStackHypervisorDetailView
from models import OpenStackAgent


urlpatterns = [
    url(r'^index/$', ListView.as_view(model=OpenStackAgent,template_name='openstack/index.html') ,name='openstack_index'),
    url(r'^hypervisors/(?P<pk>\d+)/$', OpenStackHypervisorsView.as_view(),name='openstack_hypervisors'),
    url(r'^hypervisors/(?P<pk>\d+)/(?P<hypervisor_hostname>\w+)/$', OpenStackHypervisorDetailView.as_view(), name='openstack_hypervisors_detail'),
]
