# -*- coding: utf-8 -*-
"""
An XBlock to represent a capability to intergate excel and drive client lib
into the open edx system

"""

from __future__ import unicode_literals

import jinja2
from xblock.fields import String, Integer, Boolean
from xblock.core import XBlock
from xblock.exceptions import JsonHandlerError
from xblock.fields import Scope
from xblock.fragment import Fragment
from xblockutils.studio_editable import StudioEditableXBlockMixin
import logging
import excelHelper
import pkg_resources
from .models import Excel
from submissions import api as sub_api
from .sub_api import SubmittingXBlockMixin

template_engine = jinja2.Environment(loader=jinja2.PackageLoader('simple_excel'))

logger = logging.getLogger(__name__)

def _(text):
    """ No-op fucntion used to mark strings that will need to be translated. """
    return text

@XBlock.needs("i18n")
class SimpleExcelXBlock(StudioEditableXBlockMixin, SubmittingXBlockMixin, XBlock):
    """ 
    Implements the simple excel xblock now
    """

    display_name = String (
        display_name = _('Problem'),
        help = _("Put the title of the problem here"),
        scope = Scope.settings,
        default = "Excel Mentoring"
        )

    spreadsheetId = String (
        display_name = _("ID of google sheets"),
        help = _("Given We have [https://docs.google.com/spreadsheets/d/17ERkDVfRdC-FjY1mxR3dSlZL2XInqlU9LQxKVsJkiMo/edit#gid=0] the spreadsheetId is 17ERkDVfRdC-FjY1mxR3dSlZL2XInqlU9LQxKVsJkiMo, please copy and paste it in this field"),
        scope = Scope.settings,
        # default = "1h6QvSTDKEAEi7Sx02zaf1KhE-AAVB6aOrhyeyzuIRhQ"
        default = "1bSoQE7PRa3EIRCypfJTHGvzWrjDIY-1U9e9jxqCCc9A"
    )

    student_input = String (
        display_name = _("Student Simple Input"),
        help = _("Please put your answer here"),
        scope =Scope.user_state,
        default = ""
        )

    answer_range = String (
	    display_name = _("Problem solver"),
	    help = _("Provide the sheetname and cells to look for problem solver in given spreadsheets. For example:  Sheet1!A1:D5"),
	    scope = Scope.settings,
	    default = "Problem Answer!B13"
	)

    question_range = String (
        display_name =_("Question Range"),
        help = _("Provide the sheetname and cells that contain the question"),
        scope = Scope.settings,
        default = "Problem Answer!A1:L12"
        )

    max_attempts = Integer(
        display_name="Maximum Attempts",
        help="Defines the number of times a student can try to answer this problem.",
        default=1,
        values={"min": 1}, scope=Scope.settings)
    
    max_points = Integer(
        display_name="Possible points",
        help="Defines the maximum points that the learner can earn.",
        default=1,
        scope=Scope.settings)
    
    show_points_earned = Boolean(
        display_name="Shows points earned",
        help="Shows points earned",
        default=True,
        scope=Scope.settings)
    
    show_submission_times = Boolean(
        display_name="Shows submission times",
        help="Shows submission times",
        default=True,
        scope=Scope.settings)

    copy_spreadsheet_id = None
    copy_sheet_id = None

    editable_fields = ( "display_name", "spreadsheetId", "answer_range", "question_range", "max_attempts", "show_points_earned", "show_submission_times")
    has_score = True
    attempt_number = 0


    def getFormalHttp(self, spreadsheetId, sheetId):
        if sheetId is not None:
            text = "https://docs.google.com/spreadsheets/d/" + spreadsheetId + "/pubhtml?" + "gid=" + str(sheetId) + "&amp;" + "single=true&amp;" + "widget=true&amp;headers=false"
        else:
            text = "https://docs.google.com/spreadsheets/d/" + spreadsheetId + "/pubhtml?" + "widget=true&amp;headers=false"

        return text


    def getWorksheetLink(self, spreadsheetId, sheetId):
        text = "https://docs.google.com/spreadsheets/d/" + spreadsheetId + "/edit#gid=" + str(sheetId)
        return text


    def getUrl(self, url):
	"""
	<iframe
    	src="https://docs.google.com/presentation/d/1x2ZuzqHsMoh1epK8VsGAlanSo7r9z55ualwQlj-ofBQ/embed?start=true&loop=true&delayms=10000"
    	frameborder="0"
    	width="960"
    	height="569"
    	allowfullscreen="true"
    	mozallowfullscreen="true"
    	webkitallowfullscreen="true">
	</iframe>
	https://docs.google.com/spreadsheets/d/17ERkDVfRdC-FjY1mxR3dSlZL2XInqlU9LQxKVsJkiMo/pubhtml?gid=2020115585&amp;single=true&amp;widget=t	       rue&amp;headers=false
	https://docs.google.com/spreadsheets/d/17ERkDVfRdC-FjY1mxR3dSlZL2XInqlU9LQxKVsJkiMo/pubhtml?widget=true&amp;headers=false
	"""

        url = '<iframe src=' + '"' + url + '"' ' frameborder="0"' + ' width="960"' + ' height="569"' + ' allowfullscreen="true"' + ' mozallowfullscreen="true"' + ' webkitallowfullscreen="true"' + '> </iframe>'
        return url
    

    def _get_course_id(self):
        """ Get a course ID if available """
        return getattr(self.runtime, 'course_id', 'all')


    def _get_student_id(self):
        """ Get student anonymous ID or normal ID """
        try:
            return self.runtime.anonymous_student_id
        except AttributeError:
            return self.scope_ids.user_id


    def get_model_object(self):
        """
        Fetches the Excel model object for the answer named `name`
        """
        # Consistency check - we should have a name by now
                  
        student_id = self._get_student_id()
        course_key = self._get_course_id()

        excel_data, _ = Excel.objects.get_or_create(
            student_id=student_id,
            course_key=course_key,
        )

        logger.info(u"Canhdq want to know data of excel model: {}" .format(excel_data))

        return excel_data


    def student_view(self, context = None):
        """
        Implementing the view of student

        """
        model_object= self.get_model_object()
        
        if self.spreadsheetId != model_object.teacher_link or self.question_range != model_object.student_link_origin:
            model_object.teacher_link = self.spreadsheetId
            sheets = excelHelper.getSheetService()
            spreadsheet_workbench_id, sheet_workbench_id, newly_spreadsheet_solution_id, newly_spreadsheet_original_id = excelHelper.processSpreadsheet2(sheets, self.spreadsheetId, self.question_range, self.answer_range)
            model_object.student_link_workbench = spreadsheet_workbench_id
            model_object.student_link_origin = self.question_range
            model_object.student_link_copy = newly_spreadsheet_solution_id
            model_object.student_sheet_id = sheet_workbench_id
            model_object.save()

        self.copy_spreadsheet_id = model_object.student_link_workbench
        self.copy_sheet_id = model_object.student_sheet_id

        logger.info(_(u"Tammd want to know copy_spreadsheet_id: %s"), self.copy_spreadsheet_id)
        logger.info(_(u"Tammd want to know solution_spreadsheet_id: %s"), model_object.student_link_copy)

        http = self.getFormalHttp( self.copy_spreadsheet_id, self.copy_sheet_id)
        emb_code = self.getUrl(http)
        link = self.getWorksheetLink( self.copy_spreadsheet_id, self.copy_sheet_id)
        self.runtime.service(self, 'i18n')

        should_disabled = ''
        submissions = sub_api.get_submissions(self.student_item_key, 1)
        if submissions:
            latest_submission = submissions[0]
            # parse the answer
            answer = latest_submission['answer'] # saved "answer information"         
            self.attempt_number = latest_submission['attempt_number']
            if (self.attempt_number >= self.max_attempts):
                should_disabled = 'disabled'

        context["title"] = self.display_name
        context["emb_code"] = emb_code
        context["answer"] = self.student_input
        context['link'] = link
        context['disabled'] = should_disabled
        context['attempt_number'] = self.attempt_number_string
        context['point_string'] = self.point_string

        template = template_engine.get_template('student_view.html')
        html = template.render(context)
        frag = Fragment(html)
        frag.add_javascript(self.resource_string('public/js/client.js'))
        frag.initialize_js("SimpleExcelXBlock")

        return frag



    def validate_field_data(self, validation, data):
        """""
        Ask this xblock to validate itself.
        XBlock subclass are expected to override this method. Any overiding method should call super() to collect 
        validation results from its superclass, and then add any additional results as necesary.
        """""
        super(SimpleExcelXBlock, self).validate_field_data(validation, data)


    @XBlock.json_handler
    def student_submit(self, submissions, suffix=''):
        """
        Handle problem grading submission

        :param self:
        :param submissions:
        :param suffix:
        :return: submit_result

        """

	logger.info(_(u"Tammd want to know json data: %s"), submissions['student_answer'])
        logger.info(u'Received submissions: {}'.format(submissions))

        model_object= self.get_model_object()

        submission_data = {
            'student_link_workbench': model_object.student_link_workbench,
            'student_link_origin' : model_object.student_link_origin,
            'student_link_copy' : model_object.student_link_copy,
            'student_sheet_id' : str(model_object.student_sheet_id),
        }
        submission = sub_api.create_submission(self.student_item_key, submission_data)

        # logger.info(u'Canhdq want to know values of newly created submission: {}'.format(submission))

        points_earned = 0

        # get final grading result
        sheets = excelHelper.getSheetService()
        evaluation_result = excelHelper.evaluateResult(sheets, model_object.student_link_workbench, model_object.student_link_copy, self.answer_range)

        logger.info(u"Canhdq want to know evaluation_result: %s", evaluation_result)

        if evaluation_result == True:
            points_earned = self.max_points

        sub_api.set_score(submission['uuid'], points_earned, self.max_points)
        
        submit_result = {}
        submit_result['point_string'] = self.point_string

        # disable the "Submit" button once the submission attempts reach max_attemps value
        self.attempt_number = submission['attempt_number']
        submit_result['attempt_number'] = self.attempt_number_string

        if (self.attempt_number >= self.max_attempts):
            submit_result['submit_disabled'] = 'disabled'
        else:
            submit_result['submit_disabled'] = ''

        logger.info(u"Canhdq want to know JSON data of submit_result: {}".format(submit_result))

        return submit_result
        #return {'result': 'success' }

    def resource_string(self, path):
        '''Handy helper for getting resources from our kit.'''
        data = pkg_resources.resource_string(__name__, path)
        return data.decode('utf8')
                                                                                               
    @property
    def point_string(self):
        if self.show_points_earned:
            score = sub_api.get_score(self.student_item_key)
            if score != None:
                return str(score['points_earned']) + ' / ' + str(score['points_possible']) + ' point(s)'
            
        return str(self.max_points) + ' point(s) possible'
    
    
    @property
    def attempt_number_string(self):
        if (self.show_submission_times):
            return "You have submitted " + str(self.attempt_number) + "/" + str(self.max_attempts) + " time(s)"
        
        return ""                        
                                
        
