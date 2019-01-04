from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import Assignment_DB as a
import Preference as p
import Instructor as ins
import TeachingAssistant as ta
import Course as c

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

# The ID and range of a sample spreadsheet.



def main(link, pref_type):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    SAMPLE_SPREADSHEET_ID = link
    SAMPLE_RANGE_NAME = 'Form Responses 1'

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    pref_list = []
    index = 0
    result = []
    assignee_list = []
    task_list = []
    authority_list = []
    authorities = []
    tasks = []
    if pref_type is 'Assignee':
        if not values:
            print('No data found.')
        else:
            for row in values:
                # Print columns A and E, which correspond to indices 0 and 4.
                #print('%s, %s' % (row[0], row[1]))
                if index is 0:
                    index = index + 1
                    continue
                else:


                    assignee_email = row[1]
                    id = row[2]
                    pref_list = row[3:6]#manually written
                    rank = 1
                    teaching_assistant = ta.TeachingAssistant(id, '--', '--', '--')
                    assignee_list.append(teaching_assistant)
                    for task_id in pref_list:
                        pref = p.Preference(None, id, task_id, rank)
                        rank = rank + 1
                        result.append(pref)

                    index = index + 1
        return result, assignee_list

    if 'High Authority' in pref_type:
        if not values:
            print('No data found.')
        else:
            for row in values:
                # Print columns A and E, which correspond to indices 0 and 4.
                #print('%s, %s' % (row[0], row[1]))
                if index is 0:
                    index = index + 1
                    continue
                else:
                    authority_email = row[1]
                    authority_id = row[2]
                    task_id = row[3]
                    tasks.append(task_id)
                    task_requirement = row[4]
                    if authority_id not in authorities:
                        authority = ins.Instructor(authority_id, '--', [], [], '--')
                        authority_list.append(authority)
                        cou = c.Course(task_id, '--', '--', authority_id, task_requirement)
                        authority.courses.append(cou)
                        task_list.append(cou)
                    else:
                        loc = authorities.index(authority_id)
                        aut = authority_list.get(loc)
                        cou = c.Course(task_id, '--', '--', authority_id, task_requirement)
                        aut.courses.append(cou)
                        task_list.append(cou)

                    pref_list = row[5:18] #manually written
                    rank = 1
                    for assignee_id in pref_list:
                        pref = p.Preference(authority_id, assignee_id, task_id, rank)
                        rank = rank + 1
                        result.append(pref)
                    index = index + 1
        return result, authority_list, task_list, tasks


