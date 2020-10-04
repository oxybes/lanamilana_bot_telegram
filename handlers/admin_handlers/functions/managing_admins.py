from aiogram.types import callback_game
from handlers.admin_handlers.helpers.help import AdminHelper
from aiogram.types import labeled_price
from database.function import DataBaseFunc
from database.models import User
from misc import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from config import get_text
from handlers.admin_handlers.helpers.admin_state import AdminStateMainMenu, AdminStateManagingAdmin
from handlers.admin_handlers.helpers.generate_keyboard import AdminGenerateKeyboard


@dp.callback_query_handler(lambda callback: callback.data == "managing_admins_main_menu_back", state=AdminStateManagingAdmin.main_menu)
async def managing_admins_main_menu_back(callback: types.CallbackQuery):
    """Возвращает в главное меню админки"""
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'main_admin_menu'), reply_markup=AdminGenerateKeyboard.admin_main_menu(user))
    await AdminStateMainMenu.admin_menu.set()


@dp.callback_query_handler(lambda callback: callback.data == "managing_admin_list_admins_back", state=AdminStateManagingAdmin.main_menu)
async def managing_admin_list_admins_back(callback: types.CallbackQuery):
    """Возвращает в главное меню управления администрации"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'admin_menu_managing_admins'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_admins(user))
    await AdminStateManagingAdmin.main_menu.set()


@dp.callback_query_handler(lambda callback: callback.data == "managing_admins_main_menu_list_admins", state=AdminStateManagingAdmin.main_menu)
async def managing_admins_main_menu_list_admins(callback: types.CallbackQuery):
    """Отправляет список администраторов бота"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(AdminHelper.get_list_admins(user), reply_markup=AdminGenerateKeyboard.managing_admin_list_admins(user))

# region Добавить администратора


@dp.callback_query_handler(lambda callback: callback.data == "managing_admins_main_menu_add_admin", state=AdminStateManagingAdmin.main_menu)
async def managing_admins_main_menu_add_admin(callback: types.CallbackQuery, state: FSMContext):
    """Добавить администратора"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await state.update_data(message_id=callback.message.message_id)
    await callback.message.edit_text(text=get_text(user, 'managing_admins_main_menu_add_admin'), reply_markup=AdminGenerateKeyboard.managing_admins_main_menu_add_admin(user))
    await AdminStateManagingAdmin.add_admin.set()


@dp.callback_query_handler(lambda callback: callback.data == "managing_admins_main_menu_add_admin_back", state=AdminStateManagingAdmin.add_admin)
async def managing_admins_main_menu_add_admin_back(callback: types.CallbackQuery):
    """Кнопка назад из ввода имени для добавления администратора"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'admin_menu_managing_admins'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_admins(user))
    await AdminStateManagingAdmin.main_menu.set()


@dp.message_handler(state=AdminStateManagingAdmin.add_admin)
async def managing_admin_main_menu_add_admin_write_login(message: types.Message, state: FSMContext):
    """Обработчик ввода логина администратора"""
    user = DataBaseFunc.get_user(int(message.from_user.id))
    user_message = AdminHelper.get_user_from_message(message)
    data = await state.get_data()
    if (user_message):
        await message.delete()
        data = await state.get_data()
        user_message.is_admin = True
        DataBaseFunc.commit()
        await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'],
                                    text=get_text(user, 'managing_admins_main_menu_add_admin_success').format(
                                        username=user_message.username),
                                    reply_markup=AdminGenerateKeyboard.admin_main_menu(user))
        await AdminStateMainMenu.admin_menu.set()
    else:
        await message.delete()
        await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'], text=get_text(user, 'managing_admins_main_menu_add_admin_not_found'),
                                    reply_markup=AdminGenerateKeyboard.managing_admins_main_menu_add_admin(user))

# endregion


#region Удалить администратора

@dp.callback_query_handler(lambda callback : callback.data == "managing_admins_main_menu_delete_admin", state = AdminStateManagingAdmin.main_menu)
async def managing_admins_main_menu_delete_admin(callback : types.CallbackQuery, state : FSMContext):
    """Удалить адинистратора"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await state.update_data(message_id=callback.message.message_id)
    await callback.message.edit_text(text=get_text(user, 'managing_admins_main_menu_delete_admin'), reply_markup=AdminGenerateKeyboard.managing_admins_main_menu_delete_admin(user))
    await AdminStateManagingAdmin.delete_admin.set()


@dp.callback_query_handler(lambda callback: callback.data == "managing_admins_main_menu_delete_admin_back", state=AdminStateManagingAdmin.delete_admin)
async def managing_admins_main_menu_add_admin_back(callback: types.CallbackQuery):
    """Кнопка назад из ввода имени для добавления администратора"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'admin_menu_managing_admins'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_admins(user))
    await AdminStateManagingAdmin.main_menu.set()


@dp.message_handler(state=AdminStateManagingAdmin.delete_admin)
async def managing_admin_main_menu_add_admin_write_login(message: types.Message, state: FSMContext):
    """Обработчик ввода логина администратора"""
    user = DataBaseFunc.get_user(int(message.from_user.id))
    user_message = AdminHelper.get_user_from_message(message)
    data = await state.get_data()
    if (user_message):
        await message.delete()
        data = await state.get_data()
        user_message.is_admin = False
        DataBaseFunc.commit()
        await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'],
                                    text=get_text(user, 'managing_admins_main_menu_delete_admin_success').format(
                                        username=user_message.username),
                                    reply_markup=AdminGenerateKeyboard.admin_main_menu(user))
        await AdminStateMainMenu.admin_menu.set()
    else:
        await message.delete()
        await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'], text=get_text(user, 'managing_admins_main_menu_delete_admin_not_found'),
                                    reply_markup=AdminGenerateKeyboard.managing_admins_main_menu_delete_admin(user))

#endregion
