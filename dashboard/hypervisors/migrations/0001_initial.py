# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('key', models.CharField(max_length=128, editable=False)),
                ('hostname', models.GenericIPAddressField()),
                ('port', models.IntegerField(default=18888)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(related_name='user_collector', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hypervisors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.GenericIPAddressField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('snmp_version', models.CharField(default=b'2c', max_length=4, choices=[(b'1', b'1'), (b'2', b'2c')])),
                ('snmp_commit', models.CharField(default=b'public', max_length=128)),
                ('ssh_username', models.CharField(default=b'root', max_length=128)),
                ('ssh_password', models.CharField(default=b'111111', max_length=128)),
                ('collector', models.ForeignKey(related_name='collector_hypervisors', to='hypervisors.Collector')),
            ],
        ),
        migrations.CreateModel(
            name='HypervisorsRules',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('type', models.CharField(max_length=32, choices=[(b'CPU\xe4\xbd\xbf\xe7\x94\xa8\xe7\x8e\x87', b'CPU\xe4\xbd\xbf\xe7\x94\xa8\xe7\x8e\x87'), (b'CPU\xe8\xb4\x9f\xe8\xbd\xbd', b'CPU\xe8\xb4\x9f\xe8\xbd\xbd'), (b'\xe5\x86\x85\xe5\xad\x98\xe4\xbd\xbf\xe7\x94\xa8\xe7\x8e\x87', b'\xe5\x86\x85\xe5\xad\x98\xe4\xbd\xbf\xe7\x94\xa8\xe7\x8e\x87'), (b'\xe7\xa3\x81\xe7\x9b\x98\xe4\xbd\xbf\xe7\x94\xa8\xe7\x8e\x87', b'\xe7\xa3\x81\xe7\x9b\x98\xe4\xbd\xbf\xe7\x94\xa8\xe7\x8e\x87'), (b'\xe7\xb3\xbb\xe7\xbb\x9f\xe8\xbf\x9b\xe7\xa8\x8b\xe6\x95\xb0', b'\xe7\xb3\xbb\xe7\xbb\x9f\xe8\xbf\x9b\xe7\xa8\x8b\xe6\x95\xb0')])),
                ('threshold_usage', models.CharField(max_length=32, choices=[(30, b'>= 30%, < 50%'), (50, b'>= 50%, < 80%'), (80, b'>= 80%, < 100%')])),
                ('threshold_load', models.CharField(max_length=32, choices=[(b'1.0', b'>= 1.0, < 1.5'), (b'1.5', b'>= 1.5, < 2.0'), (b'2.0', b'>= 2.0')])),
                ('threshold_num', models.CharField(max_length=32, choices=[(200, b'>= 200, <250'), (250, b'>= 250, <300'), (300, b'>= 300')])),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='hypervisors',
            name='location',
            field=models.ForeignKey(related_name='idc_hypervisors', to='hypervisors.IDC'),
        ),
        migrations.AddField(
            model_name='hypervisors',
            name='rules',
            field=models.ManyToManyField(related_name='rules_hypervisors', to='hypervisors.HypervisorsRules', blank=True),
        ),
        migrations.AddField(
            model_name='hypervisors',
            name='user',
            field=models.ForeignKey(related_name='user_hypervisors', to=settings.AUTH_USER_MODEL),
        ),
    ]
