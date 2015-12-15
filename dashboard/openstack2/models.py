from django.core.urlresolvers import reverse
from django.db import models

class OpenStackAgent(models.Model):
    name = models.CharField(max_length=128)
    hostname = models.GenericIPAddressField()
    port = models.IntegerField(default=10888)
    guest_agent_base_url = models.GenericIPAddressField(default='192.168.205.10')
    create_time = models.DateTimeField(editable=False, auto_now_add=True)
    update_time = models.DateTimeField(editable=False,auto_now=True)

    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
        }
        return reverse('newtouch:openstack:openstack_hypervisors', kwargs=kwargs)

    def __unicode__(self):
        return self.name

