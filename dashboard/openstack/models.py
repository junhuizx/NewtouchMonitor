from django.db import models

class OpenStackAgent(models.Model):
    name = models.CharField(max_length=128)
    hostname = models.GenericIPAddressField()
    port = models.IntegerField(default=10888)
    create_time = models.DateTimeField(editable=False, auto_now_add=True)
    update_time = models.DateTimeField(editable=False,auto_now=True)

    def __unicode__(self):
        return self.name

