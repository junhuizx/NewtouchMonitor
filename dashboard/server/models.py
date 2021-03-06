# -*- coding: utf-8 -*-
import uuid

from django.db import models
from django.contrib.auth.models import User

class IDC(models.Model):
    name = models.CharField(max_length=128)
    create_time = models.DateTimeField(editable=False, auto_now_add=True)
    update_time = models.DateTimeField(editable=False,auto_now=True)

    def __unicode__(self):
        return self.name

class ServerRules(models.Model):
    SERVER_RULES_TYPE_CHOICES = (('CPU Usgae', 'CPU Usgae'),
                                 ('CPU Load','CPU Load'),
                                 ('Memory Usgae','Memory Usgae'),
                                 ('Disk Usgae','Disk Usgae'),
                                 ('Process Num','Process Num'))

    SERVER_RULES_THRESHOLD_USAGE_CHOICES = (('30', '30-50%'),
                                                 ('50', '50-80%'),
                                                 ('80', '80+%'))

    SERVER_RULES_THRESHOLD_LOAD_CHOICES = (('1.0', '1.0-1.5'),
                                                ('1.5', '1.5-2.0'),
                                                ('2.0', '2.0+'))

    HYPERVISORS_RULES_THRESHOLD_NUM_CHOICES = (('200', '200-250'),
                                               ('250', '250-300'),
                                               ('300', '300'))

    name = models.CharField(max_length=128)
    type = models.CharField(max_length=32, choices=SERVER_RULES_TYPE_CHOICES)
    threshold_usage = models.CharField(max_length=32, choices=SERVER_RULES_THRESHOLD_USAGE_CHOICES)
    threshold_load = models.CharField(max_length=32, choices=SERVER_RULES_THRESHOLD_LOAD_CHOICES)
    threshold_num = models.CharField(max_length=32, choices=HYPERVISORS_RULES_THRESHOLD_NUM_CHOICES)
    create_time = models.DateTimeField(editable=False, auto_now_add=True)
    update_time = models.DateTimeField(editable=False,auto_now=True)

    def __unicode__(self):
        return self.name

class Collector(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(User, related_name='user_collector')
    key = models.CharField(max_length=128, editable=False)
    hostname = models.GenericIPAddressField()
    port = models.IntegerField(default=18888)
    create_time = models.DateTimeField(editable=False, auto_now_add=True)
    update_time = models.DateTimeField(editable=False,auto_now=True)

    def save(self, *args, **kwargs):
        self.key = uuid.uuid4()
        super(Collector,self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Server(models.Model):
    hostname = models.GenericIPAddressField()
    collector = models.ForeignKey(Collector, related_name='collector_server')
    create_time = models.DateTimeField(editable=False, auto_now_add=True)
    update_time = models.DateTimeField(editable=False,auto_now=True)
    location = models.ForeignKey(IDC, related_name='idc_server')
    user = models.ForeignKey(User, related_name='user_server',blank=True)
    rules = models.ManyToManyField(ServerRules, related_name= 'rules_server',blank=True)
    snmp_version = models.CharField(max_length=4,
                                    choices=(('1', '1'),('2', '2c'),),
                                    default='2c')
    snmp_commit = models.CharField(max_length=128, default='public')
    ssh_username = models.CharField(max_length=128, default='root',null=True,blank=True)
    ssh_password = models.CharField(max_length=128, default='111111',null=True,blank=True)

    def __str__(self):
        return "%s-%s" %(self.location, self.hostname)

