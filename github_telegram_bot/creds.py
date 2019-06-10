import os
import json

from oauth2client.service_account import ServiceAccountCredentials

def get_github_credentials():
    secret = os.environ.get("GH_SECRET")
    oauth_token = os.environ.get("GH_AUTH")
    return secret, oauth_token

def get_telegram_credentials():
    bot_token = os.environ.get("BOT_TOKEN")
    chat_id = os.environ.get("BOT_CHAT_ID")
    return bot_token, chat_id

def get_google_credentials():
    scopes = ['https://spreadsheets.google.com/feeds',
              'https://www.googleapis.com/auth/drive']
    service_account_info = os.environ.get("GOOGLE_CREDENTIALS")
    service_account_info_dict = json.loads(service_account_info)
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        service_account_info_dict,
        scopes
    )
    return credentials
