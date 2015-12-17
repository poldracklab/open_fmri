# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0037_auto_20151207_2330'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='contact_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
