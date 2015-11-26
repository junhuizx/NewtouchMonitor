# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hypervisors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hypervisors',
            name='ssh_password',
            field=models.CharField(default=b'111111', max_length=128, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='hypervisors',
            name='ssh_username',
            field=models.CharField(default=b'root', max_length=128, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='hypervisors',
            name='user',
            field=models.ForeignKey(related_name='user_hypervisors', blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
