from database.function import DataBaseFunc
from database.models import User
from misc import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from config import get_text, TEXTS
from handlers.admin_handlers.helpers.admin_state import AdminStateManagingUser
from handlers.admin_handlers.helpers.generate_keyboard import AdminGenerateKeyboard
from handlers.admin_handlers.helpers.help import AdminHelper


@dp.callback_query_handler(lambda callback: callback.data == "managing_users_main_menu_add_course", state = AdminStateManagingUser.main_menu)
async def managing_users_main_menu_add_course(callback : types.CallbackQuery):
    """Добавить курс конкретному пользователю"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(text = get_text(user, 'managing_users_main_menu_add_course'), reply_markup=AdminGenerateKeyboard.managing_user_add_course(user))

#region Кнопки назад
@dp.callback_query_handler(lambda callback: callback.data == "managing_users_add_course_back", state = "*")
async def managing_users_add_course_back(callback : types.CallbackQuery):
    """Возвращает в меню выбора действий в управлении пользователями"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'admin_menu_managing_users'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_users(user))
    await AdminStateManagingUser.main_menu.set()
#endregion