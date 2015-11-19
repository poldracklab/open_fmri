# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0027_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='revision',
            field=models.ForeignKey(null=True, blank=True, to='dataset.Revision'),
        ),
    ]
