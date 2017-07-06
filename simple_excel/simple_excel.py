# -*- coding: utf-8 -*-
"""
An XBlock to represent a capability to intergate excel and drive client lib
into the open edx system

"""

from __future__ import unicode_literals

import jinja2
from xblock.fields import String
from xblock.core import XBlock
from xblock.exceptions import JsonHandlerError
from xblock.fields import Scope
from xblock.fragment import Fragment
from xblockutils.studio_editable import StudioEditableXBlockMixin
import logging
import excelHelper
import pkg_resources
template_engine = jinja2.Environment(loader=jinja2.PackageLoader('simple_excel'))

logger = logging.getLogger(__name__)

def _(text):
    """ No-op fucntion used to mark strings that will need to be translated. """
    return text

@XBlock.needs("i18n")
class SimpleExcelXBlock(StudioEditableXBlockMixin, XBlock):
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
        help = _("Example with this url [https://docs.google.com/spreadsheets/d/17ERkDVfRdC-FjY1mxR3dSlZL2XInqlU9LQxKVsJkiMo/edit#gid=0] the spreadsheetId is 17ERkDVfRdC-FjY1mxR3dSlZL2XInqlU9LQxKVsJkiMo, please paste it in this field"),
        scope = Scope.settings,
        default = "https://docs.google.com/spreadsheets/d/17ERkDVfRdC-FjY1mxR3dSlZL2XInqlU9LQxKVsJkiMo/pubhtml?gid=2020115585&amp;single=true&amp;widget=true&amp;headers=false"
        )

    student_input = String (
        display_name = _("Student Simple Input"),
        help = _("Please put your answer here"),
        scope =Scope.user_state,
        default = ""
        )
    teacher_hint = String (
	display_name = _("Teacher Hint"),
	help = _("Here is where to get the answer. For example:  Sheet1!A1:D5"),
	scope = Scope.settings,
	default = ""
	)
    
    editable_fields = ( "display_name", "spreadsheetId", "teacher_hint")
    has_score = True

    def getFormalHttp(self, spreadsheetId, sheetId):
	if sheetId is not None:
		text = "https://docs.google.com/spreadsheets/d/" + spreadsheetId + "/pubhtml?" + "gid=" + sheetId + "&amp;" + "single=true&amp;" + "widget=true&amp;headers=false"
	else:
		text = "https://docs.google.com/spreadsheets/d/" + spreadsheetId + "/pubhtml?" + "widget=true&amp;headers=false"

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
    
    def student_view(self, context = None):
        """
        Implementing the view of student

        """
	sheets = excelHelper.getSheetService()
	temp = "2020115585"
	http = getFormalHttp( self.spreadsheetId, temp)
	emb_code = getUrl(http)
        self.runtime.service(self, 'i18n')
        context["title"] = self.display_name
        context["emb_code"] = emb_code
        context["answer"] = self.student_input
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
    def student_submit(self, data, suffix=''):
	logger.info(_(u"Tammd want to know json data: %s"), data['student_answer'])
        return {'result': 'success' }

    def resource_string(self, path):
        '''Handy helper for getting resources from our kit.'''
        data = pkg_resources.resource_string(__name__, path)
        return data.decode('utf8')
                                                                                               
                            
                                
        
