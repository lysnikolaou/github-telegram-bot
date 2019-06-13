from github_telegram_bot.github_issue import (
    BACKLOG_CODE_RE,
    _build_code_with_url
)

def test_build_url():
    url = 'https://github.com/repos/blah/issues/blah'
    code = 'BE-1000'
    built_url = _build_code_with_url(code, url)
    assert built_url == '=HYPERLINK("https://github.com/repos/blah/issues/blah","BE-1000")'
