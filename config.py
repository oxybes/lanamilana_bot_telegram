import os
import json


TOKEN=os.getenv("TOKEN")
MAIN_ADMIN_ID=os.getenv("MAIN_ADMIN_ID")
TOKEN_SHOP_YANDEX=os.getenv("TOKEN_SHOP")

if (os.name == "nt"):
    textsFilename = "texts//text.json"
    texts_but_filename = "texts//text_button.json"
    texts_shedule_filename = "texts//shedule1.txt"
    texts_shedule2_filename = "texts//shedule2.txt"
else:
    textsFilename = "//root//lanamilana_bot_telegram//texts//text.json"
    texts_but_filename = "//root//lanamilana_bot_telegram//texts//text_button.json"
    texts_shedule_filename = "//root//lanamilana_bot_telegram//texts//shedule1.txt"
    texts_shedule2_filename = "//root//lanamilana_bot_telegram//texts//shedule2.txt"

TEXTS = {}

with open(textsFilename, 'r', encoding='utf8') as file:
    TEXTS = json.load(file)


def get_text(user, text):
    return TEXTS[user.lng][text]


TEXTS_BUTTON = {}
with open(texts_but_filename, 'r', encoding='utf8') as file:
    TEXTS_BUTTON = json.load(file)

def get_text_but(user, text):
    return TEXTS_BUTTON[user.lng][text]


