# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fingerprint', '0003_auto_20141021_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='door',
            name='fingerprint',
            field=models.ManyToManyField(to=b'fingerprint.Fingerprint', blank=True),
        ),
    ]
