from django.core.urlresolvers import reverse
from django.db import models

class Rule(models.Model):
    name = models.CharField(max_length=128)
    type = models.GenericIPAddressField()
    port = models.IntegerField(default=10888)
    create_time = models.DateTimeField(editable=False, auto_now_add=True)
    update_time = models.DateTimeField(editable=False,auto_now=True)

    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
        }
        return reverse('newtouch:openstack:openstack_hypervisors', kwargs=kwargs)

    def __unicode__(self):
        return self.name

