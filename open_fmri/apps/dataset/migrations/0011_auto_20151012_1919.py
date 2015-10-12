# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0010_auto_20151012_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='number',
            field=models.IntegerField(),
        ),
    ]
