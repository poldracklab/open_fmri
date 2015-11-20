# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0028_auto_20151119_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='accession_number',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='acknowledgements',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='aws_link_title',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='aws_link_url',
            field=models.TextField(validators=[django.core.validators.URLValidator()], null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='summary',
            field=models.TextField(null=True),
        ),
    ]
