from django.conf.urls import url
from django.views.generic import ListView

from views import SyslogListView
from models import SyslogServerMysql


urlpatterns = [
    url(r'^index/$', ListView.as_view(model=SyslogServerMysql,template_name='network/index.html') ,name='network_index'),
    url(r'^(?P<pk>\d+)/$', SyslogListView.as_view() ,name='network_syslog'),
]
