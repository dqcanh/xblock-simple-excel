
from  __future__ import print_function

import httplib2

import os

import time

from apiclient import discovery

from oauth2client import client

from oauth2client import tools

from oauth2client.file import Storage


from oauth2client.service_account import ServiceAccountCredentials

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

    CLIENT_SECRET_FILE = '/edx/app/edxapp/google/MOOC-fb91d4f340e0.json'
    APPLICATION_NAME = 'Drive API Python Quickstart'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CLIENT_SECRET_FILE, scopes=SCOPES)
    #http_auth = credentials.authorize(httplib2.Http())
    return credentials

def getSheetService():
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'

                    'version=v4')
    credentials = get_credentials_web_service()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
    return service

def main():

    """Shows basic usage of the Google Drive API.



    Creates a Google Drive API service object and outputs the names and IDs

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

    main()


