# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0034_auto_20151202_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdatarequest',
            name='user_email_address',
            field=models.EmailField(max_length=254),
        ),
    ]
