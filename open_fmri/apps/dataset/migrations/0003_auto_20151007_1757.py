# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0002_auto_20151007_1738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='publication_document',
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='publication_full_text',
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='publication_pubmed_link',
        ),
        migrations.AddField(
            model_name='publicationdocument',
            name='dataset',
            field=models.ForeignKey(default=1, to='dataset.Dataset'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publicationfulltext',
            name='dataset',
            field=models.ForeignKey(default=1, to='dataset.Dataset'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publicationpubmedlink',
            name='dataset',
            field=models.ForeignKey(default=1, to='dataset.Dataset'),
            preserve_default=False,
        ),
    ]
