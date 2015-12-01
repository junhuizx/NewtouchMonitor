from django.db import models

class SyslogServerMysql(models.Model):
    name = models.CharField(max_length=128)
    mysql_hostname = models.GenericIPAddressField()
    mysql_db_name = models.CharField(max_length=128)
    mysql_db_username = models.CharField(max_length=128)
    mysql_db_password = models.CharField(max_length=128)
    syslog_tag = models.CharField(max_length=128)
    create_time = models.DateTimeField(editable=False, auto_now_add=True)
    update_time = models.DateTimeField(editable=False,auto_now=True)

    def __unicode__(self):
        return self.name
