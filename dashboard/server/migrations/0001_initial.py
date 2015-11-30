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
            name='IDC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.GenericIPAddressField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('snmp_version', models.CharField(default=b'2c', max_length=4, choices=[(b'1', b'1'), (b'2', b'2c')])),
                ('snmp_commit', models.CharField(default=b'public', max_length=128)),
                ('ssh_username', models.CharField(default=b'root', max_length=128, null=True, blank=True)),
                ('ssh_password', models.CharField(default=b'111111', max_length=128, null=True, blank=True)),
                ('collector', models.ForeignKey(related_name='collector_server', to='server.Collector')),
                ('location', models.ForeignKey(related_name='idc_server', to='server.IDC')),
            ],
        ),
        migrations.CreateModel(
            name='ServerRules',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('type', models.CharField(max_length=32, choices=[(b'CPU Usgae', b'CPU Usgae'), (b'CPU Load', b'CPU Load'), (b'Memory Usgae', b'Memory Usgae'), (b'Disk Usgae', b'Disk Usgae'), (b'Process Num', b'Process Num')])),
                ('threshold_usage', models.CharField(max_length=32, choices=[(b'30', b'30-50%'), (b'50', b'50-80%'), (b'80', b'80+%')])),
                ('threshold_load', models.CharField(max_length=32, choices=[(b'1.0', b'1.0-1.5'), (b'1.5', b'1.5-2.0'), (b'2.0', b'2.0+')])),
                ('threshold_num', models.CharField(max_length=32, choices=[(b'200', b'200-250'), (b'250', b'250-300'), (b'300', b'300')])),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='server',
            name='rules',
            field=models.ManyToManyField(related_name='rules_server', to='server.ServerRules', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='user',
            field=models.ForeignKey(related_name='user_server', blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
