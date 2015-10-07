# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='investigator',
        ),
        migrations.AddField(
            model_name='investigator',
            name='dataset',
            field=models.ForeignKey(to='dataset.Dataset', default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dataset',
            name='accession_number',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='acknowledgements',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='aws_link_title',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='aws_link_url',
            field=models.TextField(blank=True, validators=[django.core.validators.URLValidator()]),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='license_title',
            field=models.CharField(max_length=255, default='PPDL'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='license_url',
            field=models.TextField(blank=True, validators=[django.core.validators.URLValidator()]),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='publication_document',
            field=models.ManyToManyField(to='dataset.PublicationDocument', blank=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='publication_full_text',
            field=models.ManyToManyField(to='dataset.PublicationFullText', blank=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='publication_pubmed_link',
            field=models.ManyToManyField(to='dataset.PublicationPubMedLink', blank=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='scanner_type',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='task',
            field=models.ManyToManyField(to='dataset.Task', blank=True),
        ),
    ]
