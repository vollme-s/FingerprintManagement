# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fingerprint', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='door',
            name='user',
        ),
        migrations.AddField(
            model_name='door',
            name='fingerprint',
            field=models.ManyToManyField(to='fingerprint.Fingerprint'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='log',
            name='user',
            field=models.ForeignKey(to='fingerprint.Fingerprint'),
        ),
    ]
