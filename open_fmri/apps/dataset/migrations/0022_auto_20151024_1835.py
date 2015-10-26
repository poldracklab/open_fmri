# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0021_userdatarequest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdatarequest',
            old_name='url_token',
            new_name='token',
        ),
    ]
