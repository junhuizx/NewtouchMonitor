from django.contrib import admin

from dashboard.server.models import *

admin.site.register(Server)
admin.site.register(IDC)
admin.site.register(ServerRules)
admin.site.register(Collector)

