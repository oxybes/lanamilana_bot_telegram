from os import stat
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.sql.elements import Label
from config import TEXTS, get_text, texts_shedule_filename, texts_shedule2_filename
from database.function import DataBaseFunc
from database.models import User
from handlers.admin_handlers.helpers.admin_state import (
    AdminStateMainMenu, AdminStateManagingUser, AdminStateManagingAdmin)
from handlers.admin_handlers.helpers.generate_keyboard import \
    AdminGenerateKeyboard
from handlers.user_handlers.helpers.generator_keyboards import \
    UserGeneratorKeyboard
from handlers.user_handlers.helpers.user_state import UserStateMainMenu
from handlers.admin_handlers.helpers.help import AdminHelper
from misc import bot, dp


@dp.callback_query_handler(lambda callback: callback.data == "admin_menu_back", state=AdminStateMainMenu.admin_menu)
async def admin_menu_back(callback: types.CallbackQuery):
    """Возвращает в главное меню из админ-панели."""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'start'), reply_markup=await UserGeneratorKeyboard.start_button(user))
    await UserStateMainMenu.main_menu.set()


@dp.callback_query_handler(lambda callback: callback.data == "admin_menu_managing_courses", state=AdminStateMainMenu.admin_menu)
async def admin_menu_managing_courses(callback: types.CallbackQuery):
    """Отправляет меню по управлению и настройке подписок администрацией бота"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'admin_menu_managing_courses'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_courses(user))
    await AdminStateMainMenu.managing_courses.set()


@dp.callback_query_handler(lambda callback: callback.data == "admin_menu_managing_users", state=AdminStateMainMenu.admin_menu)
async def admin_main_menu_managing_users(callback: types.CallbackQuery):
    """Отправляет меню управления пользователями"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'admin_menu_managing_users'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_users(user))
    await AdminStateManagingUser.main_menu.set()


@dp.callback_query_handler(lambda callback: callback.data == "admin_menu_whos", state=AdminStateMainMenu.admin_menu)
async def admin_whos(callback: types.CallbackQuery):
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="admin_in_admin_menu"))
    await callback.message.edit_text(text=AdminHelper.get_whos_admin(user), reply_markup=keyboard)
    await AdminStateMainMenu.whos.set()



@dp.callback_query_handler(lambda callback: callback.data == "admin_in_admin_menu", state='*')
async def admin_in_admnin_menu(callback: types.CallbackQuery):
    """Возвращает в главное меню администрации"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'main_admin_menu'), reply_markup=AdminGenerateKeyboard.admin_main_menu(user))
    await AdminStateMainMenu.admin_menu.set()


@dp.callback_query_handler(lambda callback: callback.data == "managing_users_main_menu_back", state=AdminStateManagingUser.main_menu)
async def managing_users_main_menu_back(callback: types.CallbackQuery):
    """Возвращает в админ панель"""
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'main_admin_menu'), reply_markup=AdminGenerateKeyboard.admin_main_menu(user))
    await AdminStateMainMenu.admin_menu.set()

@dp.callback_query_handler(lambda callback : callback.data == "admin_menu_managing_admins", state = AdminStateMainMenu.admin_menu)
async def admin_menu_managing_admins(callback : types.CallbackQuery):
    """Отправляет меню управление администрацией бота"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'admin_menu_managing_admins'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_admins(user))
    await AdminStateManagingAdmin.main_menu.set()


@dp.callback_query_handler(lambda callback: callback.data == "admin_menu_new_shedule", state = AdminStateMainMenu.admin_menu)
async def new_shedule(callback : types.CallbackQuery):
    await callback.answer()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text = "1", callback_data="new_shedule_1_potok"))
    keyboard.add(InlineKeyboardButton(text = "2", callback_data="new_shedule_2_potok"))
    await callback.message.edit_text("Выберите поток, у которого сменить расписание.", reply_markup=keyboard)

@dp.callback_query_handler(lambda callback : callback.data == "new_shedule_1_potok", state = AdminStateMainMenu.admin_menu)
async def new_shedule_1_potok_handler(callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()
    await state.update_data(id_shedule = 1)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text = "Назад", callback_data="new_shedule_back"))
    await callback.message.edit_text("Отправьте новый текст с расписанием", reply_markup=keyboard)
    await AdminStateMainMenu.write_new_shedule.set()

@dp.callback_query_handler(lambda callback : callback.data == "new_shedule_2_potok", state = AdminStateMainMenu.admin_menu)
async def new_shedule_1_potok_handler(callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()
    await state.update_data(id_shedule = 2)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text = "Назад", callback_data="new_shedule_back"))
    await callback.message.edit_text("Отправьте новый текст с расписанием", reply_markup=keyboard)
    await AdminStateMainMenu.write_new_shedule.set()

@dp.message_handler(state  = AdminStateMainMenu.write_new_shedule)
async def write_shedule(message : types.Message, state : FSMContext):
    user = DataBaseFunc.get_user(message.from_user.id)
    id_shedule = (await state.get_data())["id_shedule"]
    if id_shedule == 1:
        with open(texts_shedule_filename, 'w', encoding='utf8') as file:
            file.write(message.text)
    else:
        with open(texts_shedule2_filename, 'w', encoding='utf8') as file:
            file.write(message.text)

    await message.answer('Расписание изменено',  reply_markup=AdminGenerateKeyboard.admin_main_menu(user))
    await AdminStateMainMenu.admin_menu.set()

@dp.callback_query_handler(lambda callback : callback.data == "new_shedule_back", state = AdminStateMainMenu.write_new_shedule)
async def new_shedule_1_potok_handler(callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user,'main_admin_menu'),  reply_markup=AdminGenerateKeyboard.admin_main_menu(user))
    await AdminStateMainMenu.admin_menu.set()



