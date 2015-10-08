# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0005_auto_20151007_2017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='task',
        ),
        migrations.AddField(
            model_name='task',
            name='number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
