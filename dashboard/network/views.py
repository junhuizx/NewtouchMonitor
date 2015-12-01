# -*- coding: utf-8 -*-

import json,pprint

from django.views.generic import ListView, DetailView
import requests
from api.syslog_api import get_syslog_message
from models import SyslogServerMysql
from django.conf import settings

class SyslogListView(ListView):
    template_name = 'network/syslog.html'
    queryset = []

    def get_context_data(self, **kwargs):
        mysql = SyslogServerMysql.objects.get(pk = self.kwargs['pk'])
        context = super(SyslogListView, self).get_context_data(**kwargs)

        context['syslogs'] = get_syslog_message( mysql.mysql_hostname, mysql.mysql_db_name,
                                                mysql.mysql_db_username, mysql.mysql_db_password,
                                                mysql.syslog_tag )

        return context