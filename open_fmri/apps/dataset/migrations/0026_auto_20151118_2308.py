# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0025_auto_20151118_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicationpubmedlink',
            name='dataset',
            field=models.ForeignKey(to='dataset.Dataset'),
        ),
    ]
