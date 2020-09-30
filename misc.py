import logging
import asyncio
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN

logging.basicConfig(filename="log.log", level=logging.DEBUG)

loop = asyncio.get_event_loop()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage(), loop=loop)