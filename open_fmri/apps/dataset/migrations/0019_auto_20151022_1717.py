# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0018_auto_20151021_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revision',
            name='notes',
            field=models.TextField(blank=True),
        ),
    ]
