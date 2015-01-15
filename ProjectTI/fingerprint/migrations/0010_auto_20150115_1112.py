# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fingerprint', '0009_auto_20141120_0101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fingerprint',
            name='first_finger',
            field=models.CharField(max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fingerprint',
            name='second_finger',
            field=models.CharField(max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fingerprint',
            name='third_finger',
            field=models.CharField(max_length=500),
            preserve_default=True,
        ),
    ]
