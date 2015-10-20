# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0014_auto_20151015_2320'),
    ]

    operations = [
        migrations.AddField(
            model_name='revision',
            name='date_set',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2015, 10, 20, 19, 18, 13, 931186, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='revision',
            name='previous_revision',
            field=models.ForeignKey(blank=True, to='dataset.Revision'),
        ),
    ]
