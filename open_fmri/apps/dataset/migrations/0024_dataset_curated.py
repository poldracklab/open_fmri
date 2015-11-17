# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0023_auto_20151105_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='curated',
            field=models.NullBooleanField(default=False),
        ),
    ]
