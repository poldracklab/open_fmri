# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0006_auto_20151008_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='dataset',
            field=models.ForeignKey(to='dataset.Dataset', default=1),
            preserve_default=False,
        ),
    ]
