from database.function import DataBaseFunc
from database.models import User
from misc import dp, bot
from aiogram import types
from config import get_text, TEXTS
from handlers.user_handlers.helpers.generator_keyboards import UserGeneratorKeyboard
from handlers.user_handlers.helpers.user_state import UserStateMainMenu

@dp.message_handler(commands = ['start'], state = '*')
async def start_message(message: types.Message):
    """Обработчик команды /start."""

    user = DataBaseFunc.get_user(message.from_user.id)
    
    if user == None or user.lng == None:
        user = User(id = message.from_user.id, username=message.from_user.username)
        DataBaseFunc.add(user)
        DataBaseFunc.commit()
        await message.answer(TEXTS["selected_language"], reply_markup=UserGeneratorKeyboard.choose_lng())
        await UserStateMainMenu.chooselng.set()

    else:
        await message.answer(get_text(user,'start'), reply_markup=UserGeneratorKeyboard.start_button(user))
        await UserStateMainMenu.main_menu.set()

@dp.callback_query_handler(state=UserStateMainMenu.chooselng)
async def choose_lng(callback_query:types.CallbackQuery):
    user = DataBaseFunc.get_user(callback_query.from_user.id)
    lng = callback_query.data[8:]
    user.lng = lng
    DataBaseFunc.commit()
    await callback_query.message.edit_text(get_text(user, 'start'), reply_markup=UserGeneratorKeyboard.start_button(user))
    await UserStateMainMenu.main_menu.set()
    

@dp.callback_query_handler(lambda callback: callback.data == "start_menu_get_subscribe", state='*')
async def main_menu_subscribe(callback:types.CallbackQuery):
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, "main_menu_subscribe"), reply_markup=UserGeneratorKeyboard.main_menu_subscribe(user))
    await UserStateMainMenu.get_subscribe.set()

@dp.callback_query_handler(lambda callback: callback.data == "main_menu_back", state=UserStateMainMenu.get_subscribe)
async def main_menu_back(callback:types.CallbackQuery):
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'start'), reply_markup=UserGeneratorKeyboard.start_button(user))
    await UserStateMainMenu.main_menu.set()


    