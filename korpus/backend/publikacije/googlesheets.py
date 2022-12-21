from __future__ import print_function
import logging
import os.path
from django.conf import settings
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

log = logging.getLogger(__name__)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SAMPLE_RANGE = 'Korpus!A3:L1355'


def authorize():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(settings.GSHEETS_TOKEN):
        creds = Credentials.from_authorized_user_file(settings.GSHEETS_TOKEN, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                settings.GSHEETS_CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(settings.GSHEETS_TOKEN, 'w') as token:
            token.write(creds.to_json())
    return creds


def read_range(credentials, spreadsheet_id, range):
    try:
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=spreadsheet_id,
            range=range).execute()
        values = result.get('values', [])
        if not values:
            log.warn(f'Nisu pronadjeni podaci u tabeli')
        return values
    except HttpError as err:
        log.error(err)
        return []


def main():
    credentials = authorize()
    values = read_range(credentials, settings.KORPUS_SPREADSHEET_ID, SAMPLE_RANGE)
    print(values)


if __name__ == '__main__':
    main()
