# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0035_auto_20151202_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdatarequest',
            name='dataset',
            field=models.ForeignKey(null=True, blank=True, to='dataset.Dataset'),
        ),
    ]
