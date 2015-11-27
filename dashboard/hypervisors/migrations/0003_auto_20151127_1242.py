# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hypervisors', '0002_auto_20151125_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hypervisorsrules',
            name='threshold_load',
            field=models.CharField(max_length=32, choices=[(b'1.0', b'1.0-1.5'), (b'1.5', b'1.5-2.0'), (b'2.0', b'2.0+')]),
        ),
        migrations.AlterField(
            model_name='hypervisorsrules',
            name='threshold_num',
            field=models.CharField(max_length=32, choices=[(b'200', b'200-250'), (b'250', b'250-300'), (b'300', b'300')]),
        ),
        migrations.AlterField(
            model_name='hypervisorsrules',
            name='threshold_usage',
            field=models.CharField(max_length=32, choices=[(b'30', b'30-50%'), (b'50', b'50-80%'), (b'80', b'80+%')]),
        ),
        migrations.AlterField(
            model_name='hypervisorsrules',
            name='type',
            field=models.CharField(max_length=32, choices=[(b'CPU Usgae', b'CPU Usgae'), (b'CPU Load', b'CPU Load'), (b'Memory Usgae', b'Memory Usgae'), (b'Disk Usgae', b'Disk Usgae'), (b'Process Num', b'Process Num')]),
        ),
    ]
