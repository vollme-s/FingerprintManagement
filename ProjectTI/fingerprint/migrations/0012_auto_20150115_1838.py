# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fingerprint', '0011_auto_20150115_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fingerprint',
            name='template',
            field=models.CharField(max_length=5000),
            preserve_default=True,
        ),
    ]
