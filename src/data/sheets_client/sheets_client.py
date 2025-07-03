# src/data/sheets_client/sheets_client.py

import os, gspread
from google.oauth2.service_account import Credentials
from typing import Dict, Any
from gspread.utils import ValueInputOption


# 1) Load configuration from environment
SERVICE_ACCOUNT_PATH = os.environ['GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH']
SPREADSHEET_ID = os.environ['GOOGLE_SHEETS_TEMPLATE_ID']


# 2) Define the OAuth scopes for Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# 3) Authenticate once at import time
_creds = Credentials.from_service_account_file( # type:ignore
    SERVICE_ACCOUNT_PATH,
    scopes=SCOPES
)
_gc = gspread.authorize(_creds)

# 4) Open the spreadsheet by ID
_spreadsheet = _gc.open_by_key(SPREADSHEET_ID) # type:ignore


def update_sheet_for_agent(record: Dict[str, Any]) -> None:
    """
    1) Locate or create the agent’s worksheet tab.
    2) Format talk_time as HH:MM:SS.
    3) Append a new row.
    4) Apply background colors to Attendance and Leads cells.
    """
    agent = record['agent_name']

    # 1) Get or create the worksheet for this agent
    try:
        ws = _spreadsheet.worksheet(agent)
    except gspread.exceptions.WorksheetNotFound:
        raise RuntimeError(f"Worksheet for agent '{agent}' not found. Please add a tab named '{agent}'.")

    # 2) Convert talk_time (minutes float) to HH:MM:SS
    total_seconds: int = round(record['talk_time'] * 60)
    hours: int = total_seconds // 3600
    minutes: int = (total_seconds % 3600) // 60
    seconds: int = total_seconds % 60
    talk_time_str: str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    # 3) Append the data row
    # Capture current number of rows to compute new row index
    ws.append_row([
        record['date'],
        record['attendance'],
        record['leads'],
        record['dials'],
        talk_time_str,
        record['notes']
    ], ValueInputOption.user_entered)
    all_rows = ws.get_all_values()  # Get all rows after appending
    new_row = len(all_rows) 
    # 4) Conditional coloring using gspread's `format` method [22]
    #    Attendance cell (column B)
    attendance_cell = f"B{new_row}"
    if record['attendance'] in ("Office", "Home"):
        color = {'red': 0.2, 'green': 0.4, 'blue': 0.2}
    else:
        color = {'red': 0.4, 'green': 0.2, 'blue': 0.2}
    ws.format(attendance_cell, {'backgroundColor': color})

    #    Leads cell (column C)
    leads_cell = f"C{new_row}"
    if record['leads'] > 0:
        ws.format(leads_cell, {'backgroundColor': {'red': 0.2, 'green': 0.4, 'blue': 0.2}})
