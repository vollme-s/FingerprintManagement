# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fingerprint', '0006_auto_20141021_2116'),
    ]

    operations = [
        migrations.CreateModel(
            name='Privilege',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('privilege', models.CharField(max_length=100)),
                ('user', models.ForeignKey(to='fingerprint.Fingerprint')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
