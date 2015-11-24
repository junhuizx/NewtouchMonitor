from django.contrib import admin

from dashboard.hypervisors.models import *

admin.site.register(Hypervisors)
admin.site.register(IDC)
admin.site.register(HypervisorsRules)
admin.site.register(Collector)

