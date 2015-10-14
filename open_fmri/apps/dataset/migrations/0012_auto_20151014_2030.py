# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0011_auto_20151012_1919'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicationfulltext',
            name='dataset',
        ),
        migrations.DeleteModel(
            name='PublicationFullText',
        ),
    ]
