# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fingerprint', '0004_auto_20141021_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='message',
            field=models.TextField(max_length=800),
        ),
    ]
