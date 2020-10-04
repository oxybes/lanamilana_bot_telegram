from database.function import DataBaseFunc
from database.models import User
from misc import dp, bot
from aiogram import types
from config import get_text, TEXTS
from handlers.user_handlers.helpers.generator_keyboards import UserGeneratorKeyboard
from handlers.user_handlers.helpers.user_state import UserStateMainMenu
from handlers.admin_handlers.helpers.admin_state import AdminStateMainMenu
from handlers.admin_handlers.helpers.generate_keyboard import AdminGenerateKeyboard


@dp.message_handler(commands = ['start'], state = '*')
async def start_message(message: types.Message):
    """Обработчик команды /start."""

    user = DataBaseFunc.get_user(message.from_user.id)
    await message.delete()
    if user == None or user.lng == None:
        user = User(id = message.from_user.id, username=message.from_user.username, lng="Russian")
        DataBaseFunc.add(user)
        DataBaseFunc.commit()
        info_mes = await message.answer(get_text(user, 'start'), reply_markup=UserGeneratorKeyboard.start_button(user))
        user.last_message_id_bot = info_mes.message_id
        await UserStateMainMenu.main_menu.set()

    else:
        if user.last_message_id_bot:
            await bot.delete_message(chat_id=message.chat.id, message_id=user.last_message_id_bot)
        await message.answer(get_text(user,'start'), reply_markup=UserGeneratorKeyboard.start_button(user))
        await UserStateMainMenu.main_menu.set()



@dp.callback_query_handler(state=UserStateMainMenu.chooselng)
async def choose_lng(callback_query:types.CallbackQuery):
    """Меняет язык пользователя"""
    user = DataBaseFunc.get_user(callback_query.from_user.id)
    lng = callback_query.data[8:]
    user.lng = lng
    DataBaseFunc.commit()
    await callback_query.message.edit_text(get_text(user, 'start'), reply_markup=UserGeneratorKeyboard.start_button(user))
    await UserStateMainMenu.main_menu.set()
    

@dp.callback_query_handler(lambda callback: callback.data == "start_menu_get_subscribe", state='*')
async def main_menu_subscribe(callback:types.CallbackQuery):
    """Реализует отправку доступных для покупки курсов."""
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, "main_menu_subscribe"), reply_markup=UserGeneratorKeyboard.main_menu_subscribe(user))
    await UserStateMainMenu.get_subscribe.set()

@dp.callback_query_handler(lambda callback: callback.data == "main_menu_back", state=UserStateMainMenu.get_subscribe)
async def main_menu_back(callback:types.CallbackQuery):
    """Возвращает пользователя в главное меню из меню с выбором тарифа для оплаты."""
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'start'), reply_markup=UserGeneratorKeyboard.start_button(user))
    await UserStateMainMenu.main_menu.set()


@dp.callback_query_handler(lambda callback: callback.data == "start_menu_admin", state='*')
async def admin_menu(callback:types.CallbackQuery):
    """Отправляет админ-панель."""
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user,'main_admin_menu'), reply_markup=AdminGenerateKeyboard.admin_main_menu(user))
    await AdminStateMainMenu.admin_menu.set()

    