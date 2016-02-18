# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0042_dataset_orientation_warning'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revision',
            name='date_set',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True, null=True),
        ),
    ]
