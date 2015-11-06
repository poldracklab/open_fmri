# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0022_auto_20151024_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='license_url',
            field=models.TextField(default='http://opendatacommons.org/licenses/pddl/1.0/', validators=[django.core.validators.URLValidator()], blank=True),
        ),
    ]
