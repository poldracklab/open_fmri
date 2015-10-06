# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('workflow_stage', models.CharField(default='SUBMITTED', choices=[('SUBMITTED', 'Submitted'), ('IN_PROCESS', 'In Process'), ('STAGED', 'Staged'), ('SHARED', 'Shared'), ('REVIEW', 'Review')], max_length=200)),
                ('project_name', models.CharField(max_length=255)),
                ('summary', models.TextField()),
                ('sample_size', models.IntegerField()),
                ('scanner_type', models.TextField()),
                ('accession_number', models.CharField(max_length=200)),
                ('acknowledgements', models.TextField()),
                ('license_title', models.CharField(max_length=255)),
                ('license_url', models.TextField(validators=[django.core.validators.URLValidator()])),
                ('aws_link_title', models.CharField(max_length=255)),
                ('aws_link_url', models.TextField(validators=[django.core.validators.URLValidator()])),
            ],
        ),
        migrations.CreateModel(
            name='Investigator',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('investigator', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='PublicationDocument',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('document', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='PublicationFullText',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('full_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PublicationPubMedLink',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('url', models.TextField(validators=[django.core.validators.URLValidator()])),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('cogat_id', models.TextField()),
                ('name', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='dataset',
            name='investigator',
            field=models.ManyToManyField(to='dataset.Investigator'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='publication_document',
            field=models.ManyToManyField(to='dataset.PublicationDocument'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='publication_full_text',
            field=models.ManyToManyField(to='dataset.PublicationFullText'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='publication_pubmed_link',
            field=models.ManyToManyField(to='dataset.PublicationPubMedLink'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='task',
            field=models.ManyToManyField(to='dataset.Task'),
        ),
    ]
