import pickle
from pathlib import Path

import pandas as pd
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def parse_google_sheet(sheet_id, sheet_name):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    token_path = Path("./data/token.pickle")
    if token_path.exists():
        with open(token_path, "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "./data/stt_cred.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    service = build("sheets", "v4", credentials=creds)

    # Fetch the range dynamically to include all columns
    sheet_range = f"{sheet_name}!A:ZZ"  # Include all columns from A to ZZ

    # Call the Sheets API
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=sheet_id, range=sheet_range)
        .execute()
    )
    values = result.get("values", [])

    if not values:
        print("No data found.")
        return None
    else:
        # Infer column names from the first row of the data
        columns = values[0][: min(len(values[0]), len(values[1]))]
        # Convert the values to a pandas DataFrame
        df = pd.DataFrame(values[1:], columns=columns)
    return df
