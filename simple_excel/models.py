# -*- coding: utf-8 -*-
#
# Copyright (c) 2014-2015 Harvard, edX & OpenCraft
#
# This software's license gives you freedom; you can copy, convey,
# propagate, redistribute and/or modify this program under the terms of
# the GNU Affero General Public License (AGPL) as published by the Free
# Software Foundation (FSF), either version 3 of the License, or (at your
# option) any later version of the AGPL published by the FSF.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program in a file in the toplevel directory called
# "AGPLv3".  If not, see <http://www.gnu.org/licenses/>.
#

# Imports ###########################################################

from django.db import models
from django.contrib.auth.models import User


# Classes ###########################################################

class Excel(models.Model):
    """
    Django model used to store AnswerBlock data that need to be shared
    and queried accross XBlock instances (workaround).

    TODO: Deprecate this and move to edx-submissions
    """

    class Meta:
        unique_together = (
            ('student_id', 'course_id'),
            ('student_id', 'course_key'),
        )

    teacher_link = models.CharField(max_length=512, db_index=True, blank=True, default=None, null=True)
    student_id = models.CharField(max_length=32, db_index=True)
    # course_id is deprecated; it will be removed in next release.
    course_id = models.CharField(max_length=50, db_index=True, blank=True, null=True, default=None)
    # course_key is the new course_id replacement with extended max_length.
    course_key = models.CharField(max_length=255, db_index=True)
    student_input = models.TextField(blank=True, default='', null=True)
    student_link_copy = models.CharField(max_length=512, db_index=True, blank=True, default=None, null=True)
    student_link_workbench = models.CharField(max_length=512, db_index=True, blank=True, default=None, null=True)
    student_link_origin = models.CharField(max_length=512, db_index=True, blank=True, default=None, null=True)
    student_sheet_id = models.BigIntegerField(blank=True, default = 0, db_index=True, null=True)
    created_on = models.DateTimeField('created on', auto_now_add=True)
    modified_on = models.DateTimeField('modified on', auto_now=True)

    def save(self, *args, **kwargs):
        # Force validation of max_length
        self.full_clean()
        super(Excel, self).save(*args, **kwargs)

