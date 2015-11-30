# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0031_auto_20151124_1908'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='id',
        ),
        migrations.AlterField(
            model_name='dataset',
            name='accession_number',
            field=models.CharField(max_length=60, serialize=False, primary_key=True),
        ),
    ]
