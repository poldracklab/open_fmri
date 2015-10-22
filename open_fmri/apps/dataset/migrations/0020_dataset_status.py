# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0019_auto_20151022_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='status',
            field=models.CharField(default='UNPUBLISHED', choices=[('PUBLISHED', 'Published'), ('UNPUBLISHED', 'Unpublished')], max_length=200),
        ),
    ]
