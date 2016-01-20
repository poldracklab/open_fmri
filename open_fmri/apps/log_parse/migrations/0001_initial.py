# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogFile',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('key', models.TextField()),
                ('parsed', models.BooleanField()),
                ('lock', models.BooleanField()),
                ('last_line_read', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='S3File',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('url', models.URLField()),
                ('count', models.IntegerField()),
            ],
        ),
    ]
