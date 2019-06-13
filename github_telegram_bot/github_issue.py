import re

from collections import namedtuple


BACKLOG_CODE_RE = r'(FE|BE)-\d+'

spreadsheet_data = namedtuple(
    'spreadsheet_data',
    ['worksheet_name', 'code_with_url', 'code_without_url']
)


def parse_github_issue(issue_title, issue_url):
    backlog_code = _find_backlog_code(issue_title)
    code_with_url = _build_code_with_url(backlog_code, issue_url)
    worksheet_name = _extract_worksheet_name(backlog_code)

    return spreadsheet_data(
        worksheet_name, code_with_url, backlog_code
    )

def _build_code_with_url(backlog_code, issue_url):
    return f'=HYPERLINK("{issue_url}","{backlog_code}")'

def _extract_worksheet_name(backlog_code):
    return ('Frontend Backlog' if backlog_code.startswith('FE')
            else 'Backend Backlog')

def _find_backlog_code(issue_title):
    match = re.search(BACKLOG_CODE_RE, issue_title)
    return match.group() if match is not None else ''
