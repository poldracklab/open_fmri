# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0041_referencepaper'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='orientation_warning',
            field=models.NullBooleanField(default=False),
        ),
    ]
