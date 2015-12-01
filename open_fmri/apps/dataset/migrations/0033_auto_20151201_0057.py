# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import dataset.models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0032_auto_20151130_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='accession_number',
            field=models.CharField(max_length=60, primary_key=True, default=dataset.models.acc_num_gen, serialize=False),
        ),
    ]
