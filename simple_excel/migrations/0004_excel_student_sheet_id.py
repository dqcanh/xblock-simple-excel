# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_excel', '0003_auto_20170711_0848'),
    ]

    operations = [
        migrations.AddField(
            model_name='excel',
            name='student_sheet_id',
            field=models.BigIntegerField(default=0, db_index=True, blank=True),
        ),
    ]
