import os

import aiohttp
from aiohttp import web
from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp
from telegram import Bot

router = routing.Router()


@router.register("pull_requests", action="opened")
def send_telegram_message(event, gh, *args, **kwargs):
    url = event.data['pull_request']['url']

    bot_token = os.environ.get("BOT_TOKEN")
    chat_id = os.environ.get("BOT_CHAT_ID")
    telegram_bot = Bot(bot_token)
    telegram_bot.send_message(chat_id, 'Hey guys')


async def main(request):
    # read the GitHub webhook payload
    body = await request.read()

    # our authentication token and secret
    secret = os.environ.get("GH_SECRET")
    oauth_token = os.environ.get("GH_AUTH")

    # a representation of GitHub webhook event
    event = sansio.Event.from_http(request.headers, body, secret=secret)

    async with aiohttp.ClientSession() as session:
        gh = gh_aiohttp.GitHubAPI(session, "lysnikolaou",
                                  oauth_token=oauth_token)

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
