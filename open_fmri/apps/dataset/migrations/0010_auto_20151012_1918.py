# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0009_task_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='number',
            field=models.IntegerField(blank=True),
        ),
    ]
