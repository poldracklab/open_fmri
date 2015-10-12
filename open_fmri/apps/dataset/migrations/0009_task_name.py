# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0008_remove_task_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='name',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
