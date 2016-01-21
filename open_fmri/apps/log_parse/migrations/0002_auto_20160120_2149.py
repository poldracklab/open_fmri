# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_parse', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='s3file',
            name='url',
        ),
        migrations.AddField(
            model_name='s3file',
            name='filename',
            field=models.TextField(default='filename', unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='logfile',
            name='key',
            field=models.TextField(unique=True),
        ),
    ]
