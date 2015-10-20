# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0016_auto_20151020_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revision',
            name='date_set',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
