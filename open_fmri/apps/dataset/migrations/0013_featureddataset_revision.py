# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0012_auto_20151014_2030'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeaturedDataset',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('date_featured', models.DateField()),
                ('dataset', models.ForeignKey(to='dataset.Dataset')),
            ],
        ),
        migrations.CreateModel(
            name='Revision',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('revision_number', models.CharField(max_length=200)),
                ('notes', models.TextField()),
                ('dataset', models.ForeignKey(to='dataset.Dataset')),
                ('previous_revision', models.ForeignKey(to='dataset.Revision')),
            ],
        ),
    ]
