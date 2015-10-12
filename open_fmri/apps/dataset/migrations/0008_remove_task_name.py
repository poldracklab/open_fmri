# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0007_task_dataset'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='name',
        ),
    ]
