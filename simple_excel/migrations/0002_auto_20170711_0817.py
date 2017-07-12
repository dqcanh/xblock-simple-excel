# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_excel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Excel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('teacher_link', models.CharField(max_length=512, db_index=True)),
                ('student_id', models.CharField(max_length=32, db_index=True)),
                ('course_id', models.CharField(default=None, max_length=50, null=True, db_index=True, blank=True)),
                ('course_key', models.CharField(max_length=255, db_index=True)),
                ('student_input', models.TextField(default=b'', blank=True)),
                ('student_link_copy', models.CharField(max_length=512, db_index=True)),
                ('student_link_workbench', models.CharField(max_length=512, db_index=True)),
                ('student_link_origin', models.CharField(max_length=512, db_index=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name=b'created on')),
                ('modified_on', models.DateTimeField(auto_now=True, verbose_name=b'modified on')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='excel',
            unique_together=set([('student_id', 'course_key'), ('student_id', 'course_id')]),
        ),
    ]
