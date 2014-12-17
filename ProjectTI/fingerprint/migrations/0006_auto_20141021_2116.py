# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fingerprint', '0005_auto_20141021_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='datetime',
            field=models.DateTimeField(verbose_name=b'record time'),
        ),
    ]
