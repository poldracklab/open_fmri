# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0026_auto_20151118_2308'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('url', models.TextField(validators=[django.core.validators.URLValidator()])),
                ('dataset', models.ForeignKey(to='dataset.Dataset')),
                ('revision', models.ForeignKey(to='dataset.Revision', blank=True)),
            ],
        ),
    ]
