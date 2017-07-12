# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_excel', '0002_auto_20170711_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excel',
            name='student_link_copy',
            field=models.CharField(default=None, max_length=512, db_index=True, blank=True),
        ),
        migrations.AlterField(
            model_name='excel',
            name='student_link_origin',
            field=models.CharField(default=None, max_length=512, db_index=True, blank=True),
        ),
        migrations.AlterField(
            model_name='excel',
            name='student_link_workbench',
            field=models.CharField(default=None, max_length=512, db_index=True, blank=True),
        ),
        migrations.AlterField(
            model_name='excel',
            name='teacher_link',
            field=models.CharField(default=None, max_length=512, db_index=True, blank=True),
        ),
    ]
