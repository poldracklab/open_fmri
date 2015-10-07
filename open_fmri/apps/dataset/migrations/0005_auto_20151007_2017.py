# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0004_auto_20151007_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicationdocument',
            name='dataset',
            field=models.ForeignKey(to='dataset.Dataset', default=1),
            preserve_default=False,
        ),
    ]
