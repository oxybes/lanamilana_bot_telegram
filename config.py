import os
import json

TOKEN = os.getenv("TOKEN")
MAIN_ADMIN_ID = os.getenv("MAIN_ADMIN_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")
GROUP_ID = os.getenv("GROUP_ID")

TEXTS = {}
with open('texts//text.json', 'r', encoding='utf8') as file:
    TEXTS = json.load(file)

def get_text(user, text):
    return TEXTS[user.lng][text]


TEXTS_BUTTON = {}
with open('texts//text_button.json', 'r', encoding='utf8') as file:
    TEXTS_BUTTON = json.load(file)

def get_text_but(user, text):
    return TEXTS_BUTTON[user.lng][text]
