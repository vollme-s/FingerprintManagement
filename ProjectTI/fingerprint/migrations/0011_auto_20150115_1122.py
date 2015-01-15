# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fingerprint', '0010_auto_20150115_1112'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fingerprint',
            old_name='first_finger',
            new_name='template',
        ),
        migrations.RemoveField(
            model_name='fingerprint',
            name='second_finger',
        ),
        migrations.RemoveField(
            model_name='fingerprint',
            name='third_finger',
        ),
    ]
