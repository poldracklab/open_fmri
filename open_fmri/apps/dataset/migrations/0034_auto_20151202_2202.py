# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0033_auto_20151201_0057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdatarequest',
            name='user_email_address',
            field=models.EmailField(max_length=75),
            preserve_default=True,
        ),
    ]
