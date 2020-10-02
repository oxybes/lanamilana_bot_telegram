from database.function import DataBaseFunc
from database.models import User
from misc import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from config import get_text, TEXTS
from handlers.admin_handlers.helpers.admin_state import AdminStateManagingUser
from handlers.admin_handlers.helpers.generate_keyboard import AdminGenerateKeyboard
from handlers.admin_handlers.helpers.help import AdminHelper

#region Кнопки назад
@dp.callback_query_handler(lambda callback: callback.data == "managing_users_add_course_back", state = "*")
async def managing_users_add_course_back(callback : types.CallbackQuery):
    """Возвращает в меню выбора действий в управлении пользователями"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'admin_menu_managing_users'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_users(user))
    await AdminStateManagingUser.main_menu.set()

@dp.callback_query_handler(lambda callback: callback.data == "admin_menu_managing_users_add_course_back", state = "*")
async def admin_menu_managing_users_add_course_back(callback : types.CallbackQuery):
    """Возвращает в меню выбора курса для пользователя"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(text = get_text(user, 'managing_users_main_menu_add_course'), reply_markup=AdminGenerateKeyboard.managing_user_add_course(user))
    await AdminStateManagingUser.add_course.set()
#endregion


#region Добавить курс пользователю
@dp.callback_query_handler(lambda callback: callback.data == "managing_users_main_menu_add_course", state = AdminStateManagingUser.main_menu)
async def managing_users_main_menu_add_course(callback : types.CallbackQuery):
    """Добавить курс конкретному пользователю"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(text = get_text(user, 'managing_users_main_menu_add_course'), reply_markup=AdminGenerateKeyboard.managing_user_add_course(user))
    await AdminStateManagingUser.add_course.set()


@dp.callback_query_handler(state = AdminStateManagingUser.add_course)
async def managing_users_main_menu_add_course(callback : types.CallbackQuery, state : FSMContext):
    """Выбрать какой курс добавить пользователю"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    course_id = int(callback.data[26:])
    await state.update_data(message_id = callback.message.message_id, course_id=course_id)
    await callback.message.edit_text(text = get_text(user, 'managing_users_main_menu_add_course_choose_user'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_users_add_course(user))
    await AdminStateManagingUser.add_course_choouse_user.set()

@dp.message_handler(state = AdminStateManagingUser.add_course_choouse_user)
async def managing_users_main_menu_add_course_choose_user(message : types.Message, state : FSMContext):
    """Обрабатывает выбор пользователя для добавления ему курса."""
    user = DataBaseFunc.get_user(int(message.from_user.id))
    user_message = AdminHelper.get_user_from_message(message)
    data = await state.get_data()
    if (user_message):
        await message.delete()
        data = await state.get_data()
        await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'],text=AdminHelper.managing_users_get_info_user(user, user_message), reply_markup=AdminGenerateKeyboard.managing_users_main_menu_add_course_choose_user(user))
        await AdminStateManagingUser.add_course_choouse_user_final.set()
    else:
        await message.delete()
        await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'],text=get_text(user, 'managing_users_mein_menu_add_course_choose_user_not_found'), parse_mode=types.ParseMode.MARKDOWN_V2,reply_markup=AdminGenerateKeyboard.admin_menu_managing_users_add_course(user))

@dp.callback_query_handler(lambda callback: callback.data == "managing_users_main_menu_add_course_choose_user_add", state = AdminStateManagingUser.add_course_choouse_user_final)
async def managing_users_main_menu_add_course_choose_user_add(callback : types.CallbackQuery):
    """Обработка кнопки добавить подписку пользователю"""
    await callback.answer()

@dp.callback_query_handler(lambda callback: callback.data == "managing_users_main_menu_add_course_choose_user_cancel", state = AdminStateManagingUser.add_course_choouse_user_final)
async def managing_users_main_menu_add_course_choose_user_cancel(callback : types.CallbackQuery):
    """Обработка кнопки отменить добавление подписки пользователю"""
    await callback.answer()

#endregion




