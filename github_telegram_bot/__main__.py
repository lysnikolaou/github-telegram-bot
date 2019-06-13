import os

import aiohttp
from aiohttp import web
from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp

from github_telegram_bot.creds import get_github_credentials
from github_telegram_bot.telegram import send_telegram_message
from github_telegram_bot.github_issue import parse_github_issue
from github_telegram_bot.google import update_row_google_spreadsheets_backlog


router = routing.Router()

@router.register("issues", action="opened")
@router.register("issues", action="reopened")
async def new_issue(event, gh, *args, **kwargs):
    issue_title = event.data['issue']['title']
    issue_url = event.data['issue']['html_url']
    spreadsheet_data = parse_github_issue(
        issue_title,
        issue_url
    )
    update_row_google_spreadsheets_backlog(spreadsheet_data)

@router.register("pull_request", action="opened")
@router.register("pull_request", action="reopened")
async def new_pr(event, gh, *args, **kwargs):
    pr_url = event.data['pull_request']['html_url']
    send_telegram_message(pr_url)

async def main(request):
    # read the GitHub webhook payload
    body = await request.read()

    # our authentication token and secret
    github_secret, github_oauth_token = get_github_credentials()

    # a representation of GitHub webhook event
    event = sansio.Event.from_http(request.headers, body, secret=github_secret)

    async with aiohttp.ClientSession() as session:
        gh = gh_aiohttp.GitHubAPI(session, "lysnikolaou",
                                  oauth_token=github_oauth_token)

        # call the appropriate callback for the event
        await router.dispatch(event, gh)

    # return a "Success"
    return web.Response(status=200)


if __name__ == "__main__":
    app = web.Application()
    app.router.add_post("/", main)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)
    web.run_app(app, port=port)
