# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0030_auto_20151123_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='url',
            field=models.TextField(blank=True, null=True, validators=[django.core.validators.URLValidator()]),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='accession_number',
            field=models.CharField(unique=True, default=' ', max_length=60),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='cogat_id',
            field=models.TextField(blank=True, null=True),
        ),
    ]
