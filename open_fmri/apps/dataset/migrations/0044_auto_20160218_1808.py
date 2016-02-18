# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0043_auto_20160218_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revision',
            name='date_set',
            field=models.DateTimeField(default=django.utils.timezone.now, blank=True, null=True),
        ),
    ]
