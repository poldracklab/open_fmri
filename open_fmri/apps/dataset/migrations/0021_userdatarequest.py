# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0020_dataset_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDataRequest',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('user_email_address', models.EmailField(max_length=254)),
                ('request_sent', models.DateTimeField(auto_now_add=True)),
                ('url_token', models.CharField(blank=True, max_length=200)),
            ],
        ),
    ]
