# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0040_auto_20151216_2203'),
        ('log_parse', '0002_auto_20160120_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='s3file',
            name='dataset',
            field=models.ForeignKey(to='dataset.Dataset', null=True),
        ),
    ]
