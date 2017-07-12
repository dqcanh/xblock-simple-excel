# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_excel', '0004_excel_student_sheet_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excel',
            name='student_input',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='excel',
            name='student_link_copy',
            field=models.CharField(default=None, max_length=512, null=True, db_index=True, blank=True),
        ),
        migrations.AlterField(
            model_name='excel',
            name='student_link_origin',
            field=models.CharField(default=None, max_length=512, null=True, db_index=True, blank=True),
        ),
        migrations.AlterField(
            model_name='excel',
            name='student_link_workbench',
            field=models.CharField(default=None, max_length=512, null=True, db_index=True, blank=True),
        ),
        migrations.AlterField(
            model_name='excel',
            name='student_sheet_id',
            field=models.BigIntegerField(default=0, null=True, db_index=True, blank=True),
        ),
        migrations.AlterField(
            model_name='excel',
            name='teacher_link',
            field=models.CharField(default=None, max_length=512, null=True, db_index=True, blank=True),
        ),
    ]
