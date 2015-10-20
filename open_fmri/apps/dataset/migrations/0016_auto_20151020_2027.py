# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0015_auto_20151020_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revision',
            name='previous_revision',
            field=models.ForeignKey(to='dataset.Revision', null=True),
        ),
    ]
