from aiogram import types
from config import get_text
from database.function import DataBaseFunc
from database.models import User
from misc import bot, dp

@dp.message_handler(state = "*")
async def default_message_delete(message : types.Message):
    if (message.chat.type == "supergroup"):
        return
    await message.delete()