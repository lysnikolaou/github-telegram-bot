from github_telegram_bot.github_issue import (
    BACKLOG_CODE_RE,
    USER_STORY_RE,
    DESCRIPTION_RE,
    ETA_RE,
    _find_data,
    _build_code_with_url,
    _extract_role
)

def test_find_data_success_oneliners():
    issue_text = """## User Story
* As a user I want to test things.

## Description
* Testing bot

## Estimate Working Time
* 8
"""
    assert _find_data(issue_text, USER_STORY_RE) == 'As a user I want to test things.'
    assert _find_data(issue_text, DESCRIPTION_RE) == 'Testing bot'
    assert _find_data(issue_text, ETA_RE) == '8'

def test_find_data_success_multiple_lines():
    issue_text = """## User Story
* As a user I want to test things.
* As a user I want to test things twice.

## Description
* Testing bot
* Testing bot twice

## Estimate Working Time
* 8
"""
    assert _find_data(issue_text, USER_STORY_RE) == 'As a user I want to test things., As a user I want to test things twice.'
    assert _find_data(issue_text, DESCRIPTION_RE) == 'Testing bot, Testing bot twice'

def test_find_data_success_real_issue():
    issue_text="""## User Story
* As a Frontend Developer I want to have access to the backend Docs.

## Description
* Include docs in backend app.

## Estimate Working Time
* `2` hours
"""
    assert _find_data(issue_text, USER_STORY_RE) == 'As a Frontend Developer I want to have access to the backend Docs.'
    assert _find_data(issue_text, DESCRIPTION_RE) == 'Include docs in backend app.'
    assert _find_data(issue_text, ETA_RE) == '`2`'

def test_build_url():
    url = 'https://github.com/repos/blah/issues/blah'
    code = 'BE-1000'
    built_url = _build_code_with_url(code, url)
    assert built_url == '=HYPERLINK("https://github.com/repos/blah/issues/blah","BE-1000")'

def test_extract_role():
    user_story = 'As Lys, I want to test things.'
    assert _extract_role(user_story) == 'Lys'
    user_story = 'As a user, I want to test thing.'
    assert _extract_role(user_story) == 'user'
    user_story = 'As an event admin, I want to test thing.'
    assert _extract_role(user_story) == 'event admin'
