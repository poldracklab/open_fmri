# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0040_auto_20151216_2203'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferencePaper',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.TextField(null=True, blank=True)),
                ('url', models.TextField(validators=[django.core.validators.URLValidator()], null=True, blank=True)),
                ('datasets', models.ManyToManyField(to='dataset.Dataset')),
            ],
        ),
    ]
