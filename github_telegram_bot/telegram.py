from telegram import Bot

from .creds import get_telegram_credentials


MESSAGE = """
Hey guys, there's a new PR [here]({url}). Someone might wanna check it out?
"""

def send_telegram_message(pr_url):
    bot_token, chat_id = get_telegram_credentials()
    telegram_bot = Bot(bot_token)
    telegram_bot.send_message(chat_id, MESSAGE.format(url=pr_url), 'Markdown')
