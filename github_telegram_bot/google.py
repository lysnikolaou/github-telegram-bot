import re

import gspread

from .creds import get_google_credentials


SPREADSHEET_ID = '1PvUZSk_UoNGQ24Z7QNeeksLGuvYllM3rro04foMOsBw'

def update_google_spreadsheets_backlog(spreadsheet_data):
    credentials = get_google_credentials()
    gc = gspread.authorize(credentials)
    _update_worksheet_cells(gc, spreadsheet_data)

def _update_worksheet_cells(gc, spreadsheet_data):
    spreadsheet = gc.open_by_key(SPREADSHEET_ID)
    worksheet = spreadsheet.worksheet(spreadsheet_data.worksheet_name)
    data = [spreadsheet_data.role, spreadsheet_data.user_story,
            spreadsheet_data.code, spreadsheet_data.description,
            spreadsheet_data.eta, spreadsheet_data.sprint]
    worksheet.append_row(data, 'USER_ENTERED')
