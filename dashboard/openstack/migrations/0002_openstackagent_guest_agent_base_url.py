# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('openstack', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='openstackagent',
            name='guest_agent_base_url',
            field=models.GenericIPAddressField(default=b'192.168.205.10'),
        ),
    ]
