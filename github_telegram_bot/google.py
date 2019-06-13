import re

import gspread
from gspread import utils, exceptions

from .creds import get_google_credentials


SPREADSHEET_ID = '1PvUZSk_UoNGQ24Z7QNeeksLGuvYllM3rro04foMOsBw'

def update_row_google_spreadsheets_backlog(spreadsheet_data):
    credentials = get_google_credentials()
    gc = gspread.authorize(credentials)
    _update_worksheet_row(gc, spreadsheet_data)

def _update_worksheet_row(gc, spreadsheet_data):
    spreadsheet = gc.open_by_key(SPREADSHEET_ID)
    worksheet = spreadsheet.worksheet(spreadsheet_data.worksheet_name)
    try:
        cell = worksheet.find(spreadsheet_data.code_without_url)
    except exceptions.CellNotFound:
        return

    worksheet.update_cell(cell.row, cell.col, spreadsheet_data.code_with_url)
