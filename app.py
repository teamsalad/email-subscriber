from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SPREADSHEET_ID = '1Mzli_hZ-y_RojspIBrye5fkOnK6sMa0bcqlxk_QYP6s'
RANGE_NAME = 'A1'


def main(event, context):
    """
    Subscribe email and write to Google Spreadsheet
    """
    email = event["email"]
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    service = build('sheets', 'v4', credentials=creds)
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().append(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME, valueInputOption='USER_ENTERED',
                                body={ 'values': [[email]] }).execute()
    return {
        'updatedCells': result.get('updates').get('updatedCells'),
        'updatedColumns': result.get('updates').get('updatedColumns'),
        'updatedRange': result.get('updates').get('updatedRange'),
        'updatedRows': result.get('updates').get('updatedRows')
    }

