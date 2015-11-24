# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import dataset.models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0029_auto_20151120_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicationdocument',
            name='document',
            field=models.FileField(upload_to=dataset.models.get_upload_path),
        ),
    ]
