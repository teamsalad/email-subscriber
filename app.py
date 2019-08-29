from flask import Flask, request
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1Mzli_hZ-y_RojspIBrye5fkOnK6sMa0bcqlxk_QYP6s'
RANGE_NAME = 'A1'


app = Flask(__name__)


@app.route("/email_subscriptions", methods=["POST"])
def subscribe_email():
    """
    Subscribe email and write to Google Spreadsheet
    """
    email = request.get_json()["email"]
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
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


if __name__ == "__main__":
    app.run()
    
