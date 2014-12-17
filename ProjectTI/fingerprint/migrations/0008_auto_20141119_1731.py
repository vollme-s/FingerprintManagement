# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fingerprint', '0007_privilege'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='door',
            name='fingerprint',
        ),
        migrations.AddField(
            model_name='door',
            name='allowed_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='log',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True),
        ),
        migrations.AlterField(
            model_name='privilege',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
