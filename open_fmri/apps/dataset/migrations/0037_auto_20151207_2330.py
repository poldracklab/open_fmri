# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0036_userdatarequest_dataset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='sample_size',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
