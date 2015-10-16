# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0013_featureddataset_revision'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featureddataset',
            name='date_featured',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='featureddataset',
            name='image',
            field=models.ImageField(upload_to='', blank=True),
        ),
    ]
