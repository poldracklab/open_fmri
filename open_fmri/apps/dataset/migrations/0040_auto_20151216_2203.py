# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0039_auto_20151216_1903'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='dataset',
        ),
        migrations.AddField(
            model_name='dataset',
            name='contact',
            field=models.ForeignKey(to='dataset.Contact', null=True, blank=True),
        ),
    ]
