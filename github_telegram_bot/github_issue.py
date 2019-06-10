import re

from collections import namedtuple


BACKLOG_CODE_RE = r'(FE|BE)-\d+'
USER_STORY_RE = r'##\sUser Story(\r\n|\r|\n)(?P<list>(\*[0-9A-Za-z,;\"\s]*[.?!]?(\r|\r\n|\n)?)+)'
DESCRIPTION_RE = r'##\sDescription(\r\n|\r|\n)(?P<list>(\*[0-9A-Za-z,;\"\s]*[.?!]?(\r|\r\n|\n)?)+)'
ROLE_RE = r'As\s(an?\s)?(?P<role>[A-Za-z\s]*,)'
ETA_RE = r'##\sEstimate\sWorking\sTime(\r\n|\r|\n)(?P<list>\*\s*\`?\d*\`?)'

spreadsheet_data = namedtuple(
    'spreadsheet_data',
    ['worksheet_name', 'role', 'user_story', 'code', 'description',
     'eta', 'sprint']
)


def parse_github_issue(issue_title, issue_text, issue_url, issue_milestone):
    print(f'Parsing issue_text={repr(issue_text)}')
    backlog_code = _find_backlog_code(issue_title)
    code_with_url = _build_code_with_url(backlog_code, issue_url)
    worksheet_name = _extract_worksheet_name(backlog_code)
    user_story = _find_data(issue_text, USER_STORY_RE)
    role = _extract_role(user_story)
    description = _find_data(issue_text, DESCRIPTION_RE)
    eta = _find_data(issue_text, ETA_RE)
    sprint = issue_milestone

    return spreadsheet_data(
        worksheet_name, role, user_story, code_with_url, description, eta, sprint
    )

def _build_code_with_url(backlog_code, issue_url):
    return f'=HYPERLINK("{issue_url}","{backlog_code}")'

def _extract_role(user_story):
    match = re.search(ROLE_RE, user_story)
    return match.group('role')[:-1] if match is not None else ''

def _extract_worksheet_name(backlog_code):
    return ('Frontend Backlog' if backlog_code.startswith('FE')
            else 'Backend Backlog')

def _find_data(issue_text, regex):
    match = re.search(regex, issue_text)
    if match is None:
        return ''
    user_story_list = match.group('list').split('\n')
    non_empty_filter = lambda elem: len(elem) != 0
    filtered_list = filter(non_empty_filter, user_story_list)
    return ', '.join((line[2:] for line in filtered_list))

def _find_backlog_code(issue_title):
    match = re.search(BACKLOG_CODE_RE, issue_title)
    return match.group() if match is not None else ''
