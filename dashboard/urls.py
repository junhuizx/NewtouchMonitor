from django.conf.urls import include, url
from dashboard.hypervisors import urls as hypervisors_urls
from dashboard.instances import urls as instances_urls
from dashboard.network import urls as network_urls
from dashboard.rules import urls as rules_urls
from dashboard.services import urls as services_urls
from dashboard.overview import urls as overview_urls

urlpatterns = [
    url(r'', include(overview_urls, namespace='overview')),
    url(r'^hypervisors/', include(hypervisors_urls, namespace='hypervisors')),
    url(r'^instances/', include(instances_urls, namespace='instances')),
    url(r'^network/', include(network_urls, namespace='network')),
    url(r'^rules/', include(rules_urls, namespace='rules')),
    url(r'^services/', include(services_urls, namespace='services')),
]