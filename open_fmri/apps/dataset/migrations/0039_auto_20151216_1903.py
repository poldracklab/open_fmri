# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0038_auto_20151214_2141'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('name', models.CharField(max_length=200, blank=True)),
                ('website', models.TextField(validators=[django.core.validators.URLValidator()], blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='contact_email',
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='contact_name',
        ),
        migrations.AddField(
            model_name='contact',
            name='dataset',
            field=models.ManyToManyField(null=True, blank=True, to='dataset.Dataset'),
        ),
    ]
