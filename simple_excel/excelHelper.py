
from  __future__ import print_function

import httplib2

import os

import time

from apiclient import discovery

from oauth2client import client

from oauth2client import tools

from oauth2client.file import Storage

from apiclient import errors

from oauth2client.service_account import ServiceAccountCredentials

import logging
from pprint import pprint


logger = logging.getLogger(__name__)

#try:

#    import argparse

#    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

#except ImportError:

#    flags = None



# If modifying these scopes, delete your previously saved credentials

# at ~/.credentials/drive-python-quickstart.json

#SCOPES = 'https://www.googleapis.com/auth/drive'

#CLIENT_SECRET_FILE = 'client_secret.json'

#APPLICATION_NAME = 'Drive API Python Quickstart'





def get_credentials():

    """Gets valid user credentials from storage.



    If nothing has been stored, or if the stored credentials are invalid,

    the OAuth2 flow is completed to obtain the new credentials.



    Returns:

        Credentials, the obtained credential.

    """
    SCOPES = 'https://www.googleapis.com/auth/drive'

    CLIENT_SECRET_FILE = 'client_secret.json'

    APPLICATION_NAME = 'Drive API Python Quickstart'

    home_dir = os.path.expanduser('~')

    credential_dir = os.path.join(home_dir, '.credentials')

    if not os.path.exists(credential_dir):

        os.makedirs(credential_dir)

    credential_path = os.path.join(credential_dir,

                                   'drive-python-quickstart.json')



    store = Storage(credential_path)

    credentials = store.get()

    if not credentials or credentials.invalid:

        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)

        flow.user_agent = APPLICATION_NAME

        #if flags:

        credentials = tools.run_flow(flow, store)

        #else: # Needed only for compatibility with Python 2.6

        #credentials = tools.run(flow, store)

        print('Storing credentials to ' + credential_path)

    return credentials


def get_credentials_web_service():

    SCOPES = ['https://www.googleapis.com/auth/drive']

    # CLIENT_SECRET_FILE = '/edx/app/edxapp/google/MOOC-fb91d4f340e0.json' # Tammd account exceeded limit
    APPLICATION_NAME = 'Drive API Python Quickstart'

    # use service account: canhdq-mooc-edx
    CLIENT_SECRET_FILE = '/edx/app/edxapp/google-service/service-account/dqcanh-mooc-edx-gsaccount.json'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CLIENT_SECRET_FILE, scopes=SCOPES)
    return credentials

def getSheetService():
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'

                    'version=v4')

    credentials = get_credentials_web_service()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

    return service

def getDriveService():
    credentials = get_credentials_web_service()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)
    return service

def copy_file(drive, origin_file_id, copy_title):
    """Copy an existing file.

    Args:
      service: Drive API service instance.
      origin_file_id: ID of the origin file to copy.
      copy_title: Title of the copy.

    Returns:
      The copied file if successful, None otherwise.
    """

    copied_file = {'title': copy_title}

    try:
       return drive.files().copy(fileId=origin_file_id, body=copied_file).execute()
    except errors.HttpError, error:
       print("An error occurred: %s", error)

    return None


def duplicate ( sheets, origin_sheet_id, sheet_id):   
    #Using spreadsheets.sheets.copyTo 
    new_sheet_request = sheets.spreadsheets().sheets().copyTo(spreadsheetId = origin_sheet_id, sheetId = sheet_id, body = { 'destination_spreadsheet_id' : origin_sheet_id } )
    new_sheet_response = new_sheet_request.execute()

    return new_sheet_response

def get_value_from_a_range(sheets, spreadsheetId, rangeName):
    # The ID of the spreadsheet to retrieve data from.
    spreadsheet_id = spreadsheetId  # TODO: Update placeholder value.

    # The A1 notation of the values to retrieve.
    range_ = rangeName  # TODO: Update placeholder value.

    # How values should be represented in the output.
    # The default render option is ValueRenderOption.FORMATTED_VALUE.
    value_render_option = 'FORMULA'  # TODO: Update placeholder value.

    # How dates, times, and durations should be represented in the output.
    # This is ignored if value_render_option is
    # FORMATTED_VALUE.
    # The default dateTime render option is [DateTimeRenderOption.SERIAL_NUMBER].
    # date_time_render_option = ''  # TODO: Update placeholder value.

    request = sheets.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_, valueRenderOption=value_render_option)
    response = request.execute()

    return response

def get_raw_value_from_a_range(sheets, spreadsheetId, rangeName):
    # The ID of the spreadsheet to retrieve data from.
    spreadsheet_id = spreadsheetId  # TODO: Update placeholder value.

    # The A1 notation of the values to retrieve.
    range_ = rangeName  # TODO: Update placeholder value.

    # How values should be represented in the output.
    # The default render option is ValueRenderOption.FORMATTED_VALUE.
    value_render_option = 'FORMATTED_VALUE'  # TODO: Update placeholder value.

    # How dates, times, and durations should be represented in the output.
    # This is ignored if value_render_option is
    # FORMATTED_VALUE.
    # The default dateTime render option is [DateTimeRenderOption.SERIAL_NUMBER].
    # date_time_render_option = ''  # TODO: Update placeholder value.

    request = sheets.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_, valueRenderOption=value_render_option)
    response = request.execute()

    return response

def update_value_to_a_range(sheets, spreadsheetId, rangeName, rangeValue):
    # The ID of the spreadsheet to update.
    spreadsheet_id = spreadsheetId  # TODO: Update placeholder value.

    # The A1 notation of the values to update.
    range_ = rangeName  # TODO: Update placeholder value.

    # How the input data should be interpreted.
    value_input_option = 'USER_ENTERED'  # TODO: Update placeholder value.

    value_range_body = {
    # TODO: Add desired entries to the request body. All existing entries
    # will be replaced.
	"values" : rangeValue
	
    }

    request = sheets.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, body=value_range_body)
    response = request.execute()

    return response

def clear_spreadsheet_for_a_range(sheets, spreadsheetId, rangeName):
    # The ID of the spreadsheet to update.
    spreadsheet_id = spreadsheetId  # TODO: Update placeholder value.

    # The A1 notation of the values to clear.
    range_ = rangeName  # TODO: Update placeholder value.
    clear_values_request_body = {
    # TODO: Add desired entries to the request body.
    }

    request = sheets.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=range_, body=clear_values_request_body)
    response = request.execute()

def public_to_web(drive, spreadsheetId):

    pub = drive.revisions().update(fileId = spreadsheetId , revisionId='head',body={'published':True, 'publishAuto': True}).execute()

    return pub

def processSpreadsheet(sheets, spreadsheetid, teacher_range):
    # sheets = getSheetService()
    
    # The ranges to retrieve from the spreadsheet.

    # ranges = ['Sheet1']  # TODO: Update placeholder value.

    # True if grid data should be returned.

    # This parameter is ignored if a field mask was set in the request.

    # include_grid_data = True  # TODO: Update placeholder value.

    # request_step1 = sheets.spreadsheets().get(spreadsheetId=spreadsheetid, ranges=ranges, includeGridData=include_grid_data)

    # response_step1 = request_step1.execute()
    # data = { "properties":

    #         {

    #             "title" : "Student_sheet : [%s]" % time.ctime()

    #        }

    # }
    # step1_prop = response_step1["properties"]
    # step1_prop["title"] = "Student_sheet : [%s]" % time.ctime()

    # sheet1 = sheets.spreadsheets().create(body = response_step1).execute()

    # sheet_id = sheet1["spreadsheetId"]
    drive = getDriveService()
    #try to copy exactly what is from original spreadsheet
    newly_sheet1 = copy_file(drive, spreadsheetid, "Student Sheet copy: [%s]" % time.ctime() )
    newly_sheet1_id = newly_sheet1['id']
    #newly_sheet1_id = '1bBsPgQ1GXl1k0aBEWyaw0tiVYwaA2MOMuKZrtEeAvYY'
    print("newly spreadsheets is: %s", newly_sheet1_id)
    # step 1: copy the new one to take control over
    request_step1 = sheets.spreadsheets().get(spreadsheetId=newly_sheet1_id, ranges="sheet1", includeGridData=False)
    response_step1 = request_step1.execute()
    sheet_list = response_step1['sheets']
    sheet_id = 0
    for sheet in sheet_list:
	prop = sheet["properties"]  	
   	sheet_id = prop["sheetId"]
	break
    # step 2: duplicate a new sheet to process result
    Copy_of_sheet1 = duplicate(sheets, newly_sheet1_id, sheet_id)
    #TODO Step 3: replace the formula from sheet1 to Copy of Sheet1
    rangeName = "'Copy of Sheet1'!" + teacher_range
    response_step3 = get_value_from_a_range(sheets, newly_sheet1_id, rangeName)
    range_values = response_step3["values"]
    new_value = []
    for row in range_values:
        new_row_value = []
	for value in row:
	     new = value.split('=')
             value = new[1]
 	     value = '=' +  "'Sheet1'!" + value	
	     print("value is: %s", value)
	     new_row_value.append(value)
	new_value.append(new_row_value)
    range_values = new_value
    for row in range_values:
        for value in row:
            print("new value is: " , value)

    response_step4 = update_value_to_a_range(sheets, newly_sheet1_id, rangeName, range_values)
    sheet1_range = 'Sheet1!' + teacher_range
    response_step4 = clear_spreadsheet_for_a_range(sheets, newly_sheet1_id, sheet1_range)
    response_step5 = get_raw_value_from_a_range(sheets, newly_sheet1_id, rangeName)
    range_values = response_step5["values"]
    for row in range_values:
         for value in row:
	     print("checking value 1: ", value)
    new_permission = {
      'value': 'delgemoon@gmail.com',
      'type': 'anyone',
      'role': 'writer'
    }
    try:
    	importPermission =  drive.permissions().insert(fileId=newly_sheet1_id, body=new_permission).execute()
    except errors.HttpError, error:
    	print('An error occurred: %s', error)

    #print('the newly sheet id is: ' + str(sheet_id))
    response_step6 = get_raw_value_from_a_range(sheets, newly_sheet1_id, rangeName)
    range_values = response_step6["values"]
    for row in range_values:
         for value in row:
             print("checking value 2: ", value)
    public = public_to_web(drive, newly_sheet1_id)
    print("public link is: ", str(public))

    return newly_sheet1_id, sheet_id

def processSpreadsheet2(sheets, spreadsheetId, question_range, answer_range):

    # ranges = ['Sheet1']  # TODO: Update placeholder value.
    ranges = answer_range

    # True if grid data should be returned.

    # This parameter is ignored if a field mask was set in the request.
    include_grid_data = False  # TODO: Update placeholder value.

    # create problem solver (the workbench_spreadsheet)
    request_step1 = sheets.spreadsheets().get(spreadsheetId=spreadsheetId, ranges=ranges, includeGridData=include_grid_data)
    response_step1 = request_step1.execute()

    print("Original spreadsheetId is: ", str(spreadsheetId))
    print("Content of original spreadsheets: ")
    pprint(response_step1)

    # get first worksheet from the original spreadsheets
    #
    sheet_list = response_step1['sheets']
    sheet_workbench_id = 0

    for sheet in sheet_list:
        prop = sheet["properties"]
        sheet_workbench_id = prop["sheetId"]
        break

    print("sheetId of active worksheet (sheet_workbench_id): ", str(sheet_workbench_id))

    # logger.info(u"Canhdq want to know values of response_step1: {}".format(pprint(response_step1)))

    # # TODO: data not used? TBD.
    # data = { "properties":
    #          {
    #
    #              "title" : "Student Sheet Workbench : [%s]" % time.ctime()
    #
    #          }
    # }

    step1_prop = response_step1["properties"]
    step1_prop["title"] = "Student_sheet : [%s]" % time.ctime()

    # Create a new spreadsheets for problem grading (workbench)
    #
    spreadsheet_workbench = sheets.spreadsheets().create(body = response_step1).execute()
    spreadsheet_workbench_id = spreadsheet_workbench["spreadsheetId"]
    print( "spreadsheet_workbench_id is: ", spreadsheet_workbench_id)

    # get google drive service
    #
    drive = getDriveService()

    new_permission = {
      'value': 'delgemoon@gmail.com',
      'type': 'user',
      'role': 'writer'
    }

    # grant permission to the spreadsheets spreadsheet_workbench
    #
    try:
        importPermission =  drive.permissions().insert(fileId=spreadsheet_workbench_id, body=new_permission).execute()
    except errors.HttpError, error:
        print('An error occurred: %s', error)

    # TODO: remove this redundant block
    #
    # get content of spreadsheets spreadsheet_workbench
    #
    request_step2 = sheets.spreadsheets().get(spreadsheetId=spreadsheet_workbench_id, ranges=ranges, includeGridData=False)
    response_step2 = request_step2.execute()

    # print("Content of spreadsheet_workbench after importPermission: ")
    # logger.info(u"Canhdq want to know values of response_step2: spreadsheet_workbench {}".format(pprint(response_step2)))


    # copy exactly what is from original spreadsheet
    #
    newly_spreadsheet_original = copy_file(drive, spreadsheetId, "Student Sheet Original: [%s]" % time.ctime() )
    newly_spreadsheet_original_id = newly_spreadsheet_original['id']
    print("newly_spreadsheet_original spreadsheetId is: ", newly_spreadsheet_original_id)

    # logger.info(u"Canhdq want to know values of newly_spreadsheet_original: {}".format(pprint(newly_spreadsheet_original)))

    newly_spreadsheet_solution = copy_file(drive, spreadsheetId, "Student Sheet Copy: [%s]" % time.ctime() )
    newly_spreadsheet_solution_id = newly_spreadsheet_solution['id']
    print("newly_spreadsheet_solution spreadsheetId is: ", newly_spreadsheet_solution_id)

    print("###################")
    print("Content of newly_spreadsheet_solution: ")
    logger.info(u"Canhdq want to know values of newly_spreadsheet_solution: {}".format(pprint(newly_spreadsheet_solution)))

    # grant permission to the spreadsheets 'newly_spreadsheet_original'
    #
    try:
        importPermission =  drive.permissions().insert(fileId=newly_spreadsheet_original_id, body=new_permission).execute()
    except errors.HttpError, error:
        print('An error occurred: %s', error)

    # grant permission to the spreadsheets 'newly_spreadsheet_solution'
    #
    try:
        importPermission =  drive.permissions().insert(fileId=newly_spreadsheet_solution_id, body=new_permission).execute()
    except errors.HttpError, error:
        print('An error occurred: %s', error)

    # question range include sheetname and cells
    #
    # rangeName = 'Sheet1!' + question_range
    rangeName = question_range

    # get content (question) from the original spreadsheets 'newly_spreadsheet_original'
    #
    response_step3 = get_raw_value_from_a_range(sheets, newly_spreadsheet_original_id, rangeName)
    range_values = response_step3["values"]

    print("###################")
    print("Content (Question only) from newly_spreadsheet_original: ")
    logger.info(u"Canhdq want to know updated values of newly_spreadsheet_solution: {}".format(pprint(response_step3)))

    ## print values for debugging:
    #
    #for row in range_values:
    #    for value in row:
    #        print("new value is: " , value)


    # update content (question) to the student problem spreadsheets 'newly_spreadsheet_solution'
    #
    response_step4 = update_value_to_a_range(sheets, newly_spreadsheet_solution_id, rangeName, range_values) # TODO: check what newly_spreadsheet_solution is for?
    # print("Updated Content of newly_spreadsheet_solution: ")
    # logger.info(u"Canhdq want to know updated values of newly_spreadsheet_solution: {}".format(pprint(response_step4)))

    # update values (question) to the student problem spreadsheets 'newly_spreadsheet_solution'
    #
    response_step5 = update_value_to_a_range(sheets, spreadsheet_workbench_id , rangeName, range_values) # TODO: check what spreadsheet_workbench is for?
    public = public_to_web(drive, spreadsheet_workbench_id)
    # print("Updated Content of spreadsheet_workbench: ")
    # logger.info(u"Canhdq want to know updated values of spreadsheet_workbench: {}".format(pprint(response_step5)))

    # public the spreadsheets during the test
    #
    new_permission_1 = {
                        'type': 'anyone',
                        'role': 'writer'
    }

    # grant permission to the spreadsheets
    #
    try:
        importPermission =  drive.permissions().insert(fileId=spreadsheet_workbench_id, body=new_permission_1).execute()
    except errors.HttpError, error:
        print('An error occurred: %s', error)

    # print("Updated Content of spreadsheet_workbench after importPermission: ")
    # logger.info(u"Canhdq want to know updated values of spreadsheet_workbench: {}".format(pprint(importPermission)))

    return spreadsheet_workbench_id, sheet_workbench_id, newly_spreadsheet_solution_id, newly_spreadsheet_original_id

    
def evaluateResult(sheets, student_worksheet, solution_worksheet, answer_range):

    # Range include sheetname and cells where the solver is defined, for example: 'Sheet1!A1:D5'
    #
    # rangeName = 'Sheet1!' + answer_range
    rangeName = answer_range

    logger.info(u"Canhdq want to know student_worksheet spreadsheetId: %s", student_worksheet)
    logger.info(u"Canhdq want to know solution_worksheet spreadsheetId: %s", solution_worksheet)
    logger.info(u"Canhdq want to know answer rangeName: %s", rangeName)

    # Get Student answer
    response = get_raw_value_from_a_range(sheets, student_worksheet, rangeName)
    response_student = response.get("values")

    logger.info(u"Canhdq want to know full submitted answer: {}".format(response))
    logger.info(u"Canhdq want to know values of submitted answer: {}".format(response_student))

    if response_student is None:
	    return False

    # Get Teacher answer
    response = get_raw_value_from_a_range(sheets, solution_worksheet, rangeName)
    response_solution = response.get("values")

    logger.info(u"Canhdq want to know full problem solver: {}".format(pprint(response)))
    logger.info(u"Canhdq want to know values of problem solver: {}".format(pprint(response_solution)))

    if response_solution is None:
	    return False

    if  len(response_student) != len(response_solution):
	    return False

    length_row_student = 0
    for row in response_student:
        length_row_student = len(row)
        break

    length_row_solution = 0
    for row in response_solution:
	    length_row_solution = len(row)
	    break

    if length_row_solution != length_row_student:
	    return False
    for i in range(len(response_student)):
        for j in range(len(response_student[i])):
            if response_student[i][j] != response_solution[i][j]:
                return False

    return True
	 

def main2():
    # processSpreadsheet2(getSheetService(), "1h6QvSTDKEAEi7Sx02zaf1KhE-AAVB6aOrhyeyzuIRhQ", question_range="Sheet1!A1:L7", answer_range = "Sheet1!A8:A9")

    # use canhdq's service account
    processSpreadsheet2(getSheetService(), "1bSoQE7PRa3EIRCypfJTHGvzWrjDIY-1U9e9jxqCCc9A", question_range="Problem Answer!A1:L12", answer_range="Problem Answer!B13")


def main():

    """Shows basic usage of the Google Drive API.



    Creates a Google Drive API service object

    for up to 10 files.

    """

    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'

                    'version=v4')

    credentials = get_credentials()

    http = credentials.authorize(httplib2.Http())

    service = discovery.build('drive', 'v3', http=http)

    sheets = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)



    results = service.files().list(

        pageSize=10,fields="nextPageToken, files(id, name)").execute()

    items = results.get('files', [])

    if not items:

        print('No files found.')

    else:

        print('Files:')

        for item in items:

            print('{0} ({1})'.format(item['name'], item['id']))

    spreadsheetId = '1QdcKKun8hp1wHY8CrXWJav3b7Wi6m__mv5C38NPQkxE'

    rangeName = 'Sheet1!A8:A9'

    request = sheets.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName)

    response = request.execute()

    next = response

    values = response.get('values',[])

    if not values:

        print('No data found.')

    else:   

        for row in values:

            print('range name: %s' % row[0])

    #if not values:

    #    print('No data found.')

    #else:

    #    print('Name, Major:')

    #    for row in values:

            # Print columns A and E, which correspond to indices 0 and 4.

    #        print('%s' % row[0])

    #data = { "properties":

    #         {

    #             "title" : "Student_sheet : [%s]" % time.ctime()

    #         }

    #}

    #sheet1 = sheets.spreadsheets().create(body = data).execute()

    #sheet_id = sheet1["spreadsheetId"]

    #print('the newly sheet id is: ' + str(sheet_id))

    _body = {

        'values' : values

    }

    request1 = sheets.spreadsheets().values().update(spreadsheetId='1iTLv_fDgODN0fMvUWWLYOczEgg3kTMsLJ1KuTcpmxLY', range=rangeName, valueInputOption='USER_ENTERED',  body=_body)

    response1 = request1.execute()

    request2 = sheets.spreadsheets().values().get(spreadsheetId='1iTLv_fDgODN0fMvUWWLYOczEgg3kTMsLJ1KuTcpmxLY', range=rangeName)

    response2 = request2.execute()

    values = response2.get('values',[])

    #if not values:

    #    print('No data found.')

    #else:

    #   for row in values:

    #        print('range name 2: %s' % row[0])

                                             

    

    pub = service.revisions().update(fileId = '1iTLv_fDgODN0fMvUWWLYOczEgg3kTMsLJ1KuTcpmxLY' , revisionId='head',body={'published':True, 'publishAuto': True}).execute()

    spreadsheet_id ='1QdcKKun8hp1wHY8CrXWJav3b7Wi6m__mv5C38NPQkxE'  # TODO: Update placeholder value.



    # The ranges to retrieve from the spreadsheet.

    ranges = ['Sheet1']  # TODO: Update placeholder value.



    # True if grid data should be returned.

    # This parameter is ignored if a field mask was set in the request.

    include_grid_data = False  # TODO: Update placeholder value.



    request3 = sheets.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=ranges, includeGridData=include_grid_data)

    response3 = request3.execute()

    sheet_id = 1

    for s in response3['sheets']:

        prop = s['properties']

        sheet_id = prop['sheetId']

        print('sheet_id is: %d' % sheet_id)

    # The ID of the spreadsheet containing the sheet to copy.

    #spreadsheet_id = 'my-spreadsheet-id'  # TODO: Update placeholder value.



    # The ID of the sheet to copy.

    #sheet_id = 0  # TODO: Update placeholder value.



    copy_sheet_to_another_spreadsheet_request_body = {

            # The ID of the spreadsheet to copy the sheet to.

            'destination_spreadsheet_id': '1iTLv_fDgODN0fMvUWWLYOczEgg3kTMsLJ1KuTcpmxLY',  # TODO: Update placeholder value.



            # TODO: Add desired entries to the request body.

        }



    request = sheets.spreadsheets().sheets().copyTo(spreadsheetId=spreadsheet_id, sheetId=sheet_id, body=copy_sheet_to_another_spreadsheet_request_body)

    response = request.execute()



if __name__ == '__main__':

    main2()


