# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fingerprint', '0002_auto_20141012_0154'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='message',
            field=models.TextField(max_length=800, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='door',
            name='fingerprint',
            field=models.ManyToManyField(to=b'fingerprint.Fingerprint', null=True),
        ),
    ]
