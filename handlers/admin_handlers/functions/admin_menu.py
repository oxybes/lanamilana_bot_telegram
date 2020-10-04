from aiogram import types
from config import TEXTS, get_text
from database.function import DataBaseFunc
from database.models import User
from handlers.admin_handlers.helpers.admin_state import (
    AdminStateMainMenu, AdminStateManagingUser, AdminStateManagingAdmin)
from handlers.admin_handlers.helpers.generate_keyboard import \
    AdminGenerateKeyboard
from handlers.user_handlers.helpers.generator_keyboards import \
    UserGeneratorKeyboard
from handlers.user_handlers.helpers.user_state import UserStateMainMenu
from misc import bot, dp


@dp.callback_query_handler(lambda callback: callback.data == "admin_menu_back", state=AdminStateMainMenu.admin_menu)
async def admin_menu_back(callback: types.CallbackQuery):
    """Возвращает в главное меню из админ-панели."""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'start'), reply_markup=UserGeneratorKeyboard.start_button(user))
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