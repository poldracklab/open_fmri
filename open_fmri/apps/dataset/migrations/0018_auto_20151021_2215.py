# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0017_auto_20151020_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='revision',
            name='aws_link_title',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='revision',
            name='aws_link_url',
            field=models.TextField(validators=[django.core.validators.URLValidator()], blank=True),
        ),
    ]
