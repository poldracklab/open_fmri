# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0003_auto_20151007_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicationdocument',
            name='dataset',
            field=models.ForeignKey(to='dataset.Dataset', null=True),
        ),
    ]
