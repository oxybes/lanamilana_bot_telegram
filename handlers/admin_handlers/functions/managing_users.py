from os import stat

from aiogram import types
from aiogram.dispatcher import FSMContext
from config import get_text
from database.function import DataBaseFunc
from database.models import User
from handlers.admin_handlers.helpers.admin_state import (
    AdminStateMainMenu, AdminStateManagingUser)
from handlers.admin_handlers.helpers.generate_keyboard import \
    AdminGenerateKeyboard
from handlers.admin_handlers.helpers.help import AdminHelper
from misc import bot, dp

# region Кнопки назад


@dp.callback_query_handler(lambda callback: callback.data == "managing_users_add_course_back", state="*")
async def managing_users_add_course_back(callback: types.CallbackQuery):
    """Возвращает в меню выбора действий в управлении пользователями"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'admin_menu_managing_users'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_users(user))
    await AdminStateManagingUser.main_menu.set()


@dp.callback_query_handler(lambda callback: callback.data == "admin_menu_managing_users_add_course_back", state="*")
async def admin_menu_managing_users_add_course_back(callback: types.CallbackQuery):
    """Возвращает в меню выбора курса для пользователя"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'admin_menu_managing_users'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_users(user))
    await AdminStateManagingUser.main_menu.set()
# endregion


# region Добавить курс пользователю
@dp.callback_query_handler(lambda callback: callback.data == "managing_users_main_menu_add_course", state=AdminStateManagingUser.main_menu)
async def managing_users_main_menu_add_course(callback: types.CallbackQuery, state : FSMContext):
    """Добавить курс конкретному пользователю"""
    await callback.answer()
    await state.update_data(message_id = callback.message.message_id)
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(text=get_text(user, 'managing_users_main_menu_add_course_choose_user'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_users_add_course(user))
    await AdminStateManagingUser.add_course_choouse_user.set()


@dp.callback_query_handler(state=AdminStateManagingUser.add_course)
async def managing_users_main_menu_add_course(callback: types.CallbackQuery, state: FSMContext):
    """Выбрать какой курс добавить пользователю"""
    await callback.answer()
    data = await state.get_data()
    user = DataBaseFunc.get_user(callback.from_user.id)
    add_user = DataBaseFunc.get_user(int(data['user_add_course_id']))
    course_id = int(callback.data[26:])
    await state.update_data(message_id=callback.message.message_id, course_id=course_id)
    await callback.message.edit_text(text=AdminHelper.managing_users_get_info_user(user, add_user, course_id), reply_markup=AdminGenerateKeyboard.managing_users_main_menu_add_course_choose_user(user))
    await AdminStateManagingUser.add_course_choouse_user_final.set()


@dp.message_handler(state=AdminStateManagingUser.add_course_choouse_user)
async def managing_users_main_menu_add_course_choose_user(message: types.Message, state: FSMContext):
    """Обрабатывает выбор пользователя для добавления ему курса."""
    user = DataBaseFunc.get_user(int(message.from_user.id))
    user_message = AdminHelper.get_user_from_message(message)
    data = await state.get_data()
    if (user_message):
        await message.delete()
        data = await state.get_data()
        await state.update_data(user_add_course_id = user_message.id)
        await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'], text=get_text(user, 'managing_users_main_menu_add_course'), reply_markup=AdminGenerateKeyboard.managing_user_add_course(user, user_message))
        await AdminStateManagingUser.add_course.set()
    else:
        await message.delete()
        await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'], text=get_text(user, 'managing_users_mein_menu_add_course_choose_user_not_found'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_users_add_course(user))


@dp.callback_query_handler(lambda callback: callback.data == "managing_users_main_menu_add_course_choose_user_add", state=AdminStateManagingUser.add_course_choouse_user_final)
async def managing_users_main_menu_add_course_choose_user_add(callback: types.CallbackQuery, state: FSMContext):
    """Обработка кнопки добавить подписку пользователю"""
    await callback.answer()
    data = await state.get_data()
    user = DataBaseFunc.get_user(callback.from_user.id)
    course = DataBaseFunc.get_course(data['course_id'])
    DataBaseFunc.add_course_in_user(user, course)
    await callback.message.edit_text(get_text(user, 'managing_users_main_menu_add_course_choose_user_add'),  reply_markup=AdminGenerateKeyboard.admin_main_menu(user))
    await AdminStateMainMenu.admin_menu.set()


@dp.callback_query_handler(lambda callback: callback.data == "managing_users_main_menu_add_course_choose_user_cancel", state=AdminStateManagingUser.add_course_choouse_user_final)
async def managing_users_main_menu_add_course_choose_user_cancel(callback: types.CallbackQuery):
    """Обработка кнопки отменить добавление подписки пользователю"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'main_admin_menu'), reply_markup=AdminGenerateKeyboard.admin_main_menu(user))
    await AdminStateMainMenu.admin_menu.set()

# endregion

# region Удалить курс у пользователя

# region Кнопки назад


@dp.callback_query_handler(lambda callback: callback.data == "managing_users_main_menu_delete_course", state=AdminStateManagingUser.delete_course_choouse_user)
async def managing_users_main_menu_delete_course_back(callback: types.CallbackQuery):
    """Вернуться в панель управления пользователями"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'main_admin_menu'), reply_markup=AdminGenerateKeyboard.admin_main_menu(user))
    await AdminStateMainMenu.admin_menu.set()


@dp.callback_query_handler(lambda callback: callback.data == "managin_users_main_menu_delete_course_choose_use_back", state=AdminStateManagingUser.delete_course)
async def managin_users_main_menu_delete_course_choose_use_back(callback: types.CallbackQuery):
    """Вернуться в панель управления пользователями"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'main_admin_menu'), reply_markup=AdminGenerateKeyboard.admin_main_menu(user))
    await AdminStateMainMenu.admin_menu.set()

# endregion


@dp.callback_query_handler(lambda callback: callback.data == "managing_users_main_menu_delete_course", state=AdminStateManagingUser.main_menu)
async def managing_users_main_menu_delete_course(callback: types.CallbackQuery, state: FSMContext):
    """Обработка кнопки "Удалить курс" из меню управления пользователями. """
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await state.update_data(message_id=callback.message.message_id)
    await callback.message.edit_text(text=get_text(user, 'managing_users_main_menu_delete_course'), reply_markup=AdminGenerateKeyboard.managing_users_main_menu_delete_course(user))
    await AdminStateManagingUser.delete_course_choouse_user.set()


@dp.message_handler(state=AdminStateManagingUser.delete_course_choouse_user)
async def managin_users_main_menu_delete_course_choose_user(message: types.Message, state: FSMContext):
    """Обработывает выбор пользователя"""
    user = DataBaseFunc.get_user(int(message.from_user.id))
    user_message = AdminHelper.get_user_from_message(message)
    data = await state.get_data()
    if (user_message):
        await state.update_data(user_delete_id=user_message.id)
        await message.delete()
        await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'], text=get_text(user, 'managin_users_main_menu_delete_course_choose_use'), reply_markup=AdminGenerateKeyboard.managin_users_main_menu_delete_course_choose_use(user))
        await AdminStateManagingUser.delete_course.set()
    else:
        await message.delete()
        await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'], text=get_text(user, 'managing_users_main_menu_add_course_choose_user_not_found'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_users_add_course(user))


@dp.callback_query_handler(state=AdminStateManagingUser.delete_course)
async def managing_users_choose_course_for_delete(callback: types.CallbackQuery, state: FSMContext):
    """Выбор курса для удаления."""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    course_id = callback.data[49:]
    await state.update_data(course_id=course_id)
    data = await state.get_data()
    await callback.message.edit_text(AdminHelper.get_info_for_delete_course(user, data['user_delete_id'], course_id), reply_markup=AdminGenerateKeyboard.managing_users_delete_course_final(user))
    await AdminStateManagingUser.delete_course_final.set()


@dp.callback_query_handler(lambda callback: callback.data == "managing_users_delete_course_final_add", state=AdminStateManagingUser.delete_course_final)
async def managing_users_delete_course_final_add(callback: types.CallbackQuery, state: FSMContext):
    """Удалить курс у пользователя."""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    data = await state.get_data()
    delete_user = DataBaseFunc.get_user(data['user_delete_id'])
    course = DataBaseFunc.get_course(data['course_id'])
    DataBaseFunc.delete_course_from_user(delete_user, course)
    await callback.message.edit_text(get_text(user, 'managing_users_delete_course_final_add').format(course=course.name, username=delete_user.username), reply_markup=AdminGenerateKeyboard.admin_main_menu(user))
    await AdminStateMainMenu.admin_menu.set()


@dp.callback_query_handler(lambda callback: callback.data == "managing_users_delete_course_final_cancel", state=AdminStateManagingUser.delete_course_final)
async def managing_users_delete_course_final_cancel(callback: types.CallbackQuery):
    """Отменяет удаление курса у пользователя."""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'main_admin_menu'), reply_markup=AdminGenerateKeyboard.admin_main_menu(user))
    await AdminStateMainMenu.admin_menu.set()
# endregion

# region Добавить время пользователю

# region Кнопки назад

# Столько много обработчиков, которые возвращают в одно и то же меню - на случай, если понадобится накинуть другие действия на кнопку назад
# И не переписывать потом много кода.


@dp.callback_query_handler(lambda callback: callback.data == "managign_users_add_time_back", state=AdminStateManagingUser.add_time_choose_user)
async def managign_users_add_time_back(callback: types.CallbackQuery):
    """Возвращает в главное меню управления пользователями"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'admin_menu_managing_users'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_users(user))
    await AdminStateManagingUser.main_menu.set()


@dp.callback_query_handler(lambda callback: callback.data == "admin_menu_managing_users_add_time_choose_user_back", state=AdminStateManagingUser.add_time_choose_user)
async def managign_users_add_time_back(callback: types.CallbackQuery):
    """Возвращает в главное меню управления пользователями"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'admin_menu_managing_users'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_users(user))
    await AdminStateManagingUser.main_menu.set()


@dp.callback_query_handler(lambda callback: callback.data == "managing_users_add_time_choose_course_back", state=AdminStateManagingUser.add_time_choose_course)
async def managign_users_add_time_back(callback: types.CallbackQuery):
    """Возвращает в главное меню управления пользователями"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'admin_menu_managing_users'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_users(user))
    await AdminStateManagingUser.main_menu.set()


@dp.callback_query_handler(lambda callback: callback.data == "managing_users_add_time_choose_time_back", state=AdminStateManagingUser.add_time_write_time)
async def managing_users_add_time_choose_time_back(callback: types.CallbackQuery):
    """Возвращает в главное меню управления пользователями"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'admin_menu_managing_users'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_users(user))
    await AdminStateManagingUser.main_menu.set()

# endregion


@dp.callback_query_handler(lambda callback: callback.data == "managing_users_main_menu_add_time", state=AdminStateManagingUser.main_menu)
async def managing_users_main_menu_add_time(callback: types.CallbackQuery, state: FSMContext):
    """Обработка кнопки добавить время из админ панели менеджера пользователей. """
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await state.update_data(message_id=callback.message.message_id)
    await callback.message.edit_text(get_text(user, 'managing_users_add_time_choose_user'), reply_markup=AdminGenerateKeyboard.managign_users_add_time(user))
    await AdminStateManagingUser.add_time_choose_user.set()


@dp.message_handler(state=AdminStateManagingUser.add_time_choose_user)
async def managin_users_main_menu_delete_course_choose_user(message: types.Message, state: FSMContext):
    """Обработывает выбор пользователя"""
    user = DataBaseFunc.get_user(int(message.from_user.id))
    user_message = AdminHelper.get_user_from_message(message)
    data = await state.get_data()
    if (user_message):
        await state.update_data(user_addtime_id=user_message.id)
        await message.delete()
        await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'], text=get_text(user, 'managing_users_add_time_choose_courses'), reply_markup=AdminGenerateKeyboard.managing_users_add_time_choose_course(user))
        await AdminStateManagingUser.add_time_choose_course.set()
    else:
        await message.delete()
        await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'], text=get_text(user, 'managing_users_add_time_choose_user_not_found'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_users_add_time_choose_user_back(user))


@dp.callback_query_handler(state=AdminStateManagingUser.add_time_choose_course)
async def managing_users_add_time_choose_course(callback: types.CallbackQuery, state: FSMContext):
    """Выбор курса для добавления ему времени"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    course_id = int(callback.data[38:])
    await state.update_data(course_id=course_id, message_id=callback.message.message_id)
    await callback.message.edit_text(get_text(user, 'managing_users_add_time_choose_time'), reply_markup=AdminGenerateKeyboard.managing_users_add_time_choose_time(user))
    await AdminStateManagingUser.add_time_write_time.set()


@dp.message_handler(state=AdminStateManagingUser.add_time_write_time)
async def managing_user_add_time_write_time(message: types.Message, state: FSMContext):
    """Ввод времени"""
    data = await state.get_data()
    user = DataBaseFunc.get_user(message.from_user.id)
    try:
        time = int(message.text)
        await state.update_data(time=time)
        await message.delete()
        user_addtime = DataBaseFunc.get_user(data['user_addtime_id'])
        await bot.edit_message_text(text=AdminHelper.get_text_managing_users_add_time_final(user_addtime, data['course_id'], time),
                                    chat_id=message.chat.id, message_id=data['message_id'],
                                    reply_markup=AdminGenerateKeyboard.managing_users_add_time_final(user))
        await AdminStateManagingUser.add_time_final.set()
    except:
        await message.delete()
        await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'],
                                    text=get_text(
                                        user, 'managing_user_add_time_write_time_not_str'),
                                    reply_markup=AdminGenerateKeyboard.managing_users_add_time_choose_time(user))


@dp.callback_query_handler(lambda callback: callback.data == "managing_users_add_time_final_add", state=AdminStateManagingUser.add_time_final)
async def managing_users_add_time_final_add(callback: types.CallbackQuery, state: FSMContext):
    """Добавить время пользователю в конкретный курс."""
    await callback.answer()
    data = await state.get_data()
    user = DataBaseFunc.get_user(callback.from_user.id)
    user_addtime = DataBaseFunc.get_user(data['user_addtime_id'])
    course = DataBaseFunc.get_course(data['course_id'])
    time = data['time']
    DataBaseFunc.add_time_in_course(user_addtime, course, time)
    await callback.message.edit_text(get_text(user, 'managing_users_add_time_final_add'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_users(user))
    await AdminStateManagingUser.main_menu.set()


@dp.callback_query_handler(lambda callback: callback.data == "managing_users_add_time_final_cancel", state=AdminStateManagingUser.add_time_final)
async def managing_users_add_time_final_cancel(callback: types.CallbackQuery, state: FSMContext):
    """Добавить время пользователю в конкретный курс."""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'admin_menu_managing_users'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_users(user))
    await AdminStateManagingUser.main_menu.set()
# endregion

#region Удалить время
# region Кнопки назад

# Столько много обработчиков, которые возвращают в одно и то же меню - на случай, если понадобится накинуть другие действия на кнопку назад
# И не переписывать потом много кода.


@dp.callback_query_handler(lambda callback: callback.data == "managign_users_add_time_back", state=AdminStateManagingUser.delete_time_choose_user)
async def managign_users_delete_time_back(callback: types.CallbackQuery):
    """Возвращает в главное меню управления пользователями"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'admin_menu_managing_users'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_users(user))
    await AdminStateManagingUser.main_menu.set()


@dp.callback_query_handler(lambda callback: callback.data == "admin_menu_managing_users_add_time_choose_user_back", state=AdminStateManagingUser.delete_time_choose_user)
async def managign_users_delete_time_back(callback: types.CallbackQuery):
    """Возвращает в главное меню управления пользователями"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'admin_menu_managing_users'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_users(user))
    await AdminStateManagingUser.main_menu.set()


@dp.callback_query_handler(lambda callback: callback.data == "managing_users_add_time_choose_course_back", state=AdminStateManagingUser.delete_time_choose_course)
async def managign_users_delete_time_back(callback: types.CallbackQuery):
    """Возвращает в главное меню управления пользователями"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'admin_menu_managing_users'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_users(user))
    await AdminStateManagingUser.main_menu.set()


@dp.callback_query_handler(lambda callback: callback.data == "managing_users_add_time_choose_time_back", state=AdminStateManagingUser.delete_time_write_time)
async def managing_users_delete_time_choose_time_back(callback: types.CallbackQuery):
    """Возвращает в главное меню управления пользователями"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'admin_menu_managing_users'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_users(user))
    await AdminStateManagingUser.main_menu.set()

# endregion


@dp.callback_query_handler(lambda callback: callback.data == "managing_users_main_menu_delete_time", state=AdminStateManagingUser.main_menu)
async def managing_users_main_menu_delete_time(callback: types.CallbackQuery, state: FSMContext):
    """Обработка кнопки добавить время из админ панели менеджера пользователей. """
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await state.update_data(message_id=callback.message.message_id)
    await callback.message.edit_text(get_text(user, 'managing_users_add_time_choose_user'), reply_markup=AdminGenerateKeyboard.managign_users_add_time(user))
    await AdminStateManagingUser.delete_time_choose_user.set()


@dp.message_handler(state=AdminStateManagingUser.delete_time_choose_user)
async def managin_users_main_menu_delete_course_choose_user(message: types.Message, state: FSMContext):
    """Обработывает выбор пользователя"""
    user = DataBaseFunc.get_user(int(message.from_user.id))
    user_message = AdminHelper.get_user_from_message(message)
    data = await state.get_data()
    if (user_message):
        await state.update_data(user_addtime_id=user_message.id)
        await message.delete()
        await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'], text=get_text(user, 'managing_users_delete_time_choose_courses'), reply_markup=AdminGenerateKeyboard.managing_users_add_time_choose_course(user))
        await AdminStateManagingUser.delete_time_choose_course.set()
    else:
        await message.delete()
        await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'], text=get_text(user, 'managing_users_add_time_choose_user_not_found'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_users_add_time_choose_user_back(user))


@dp.callback_query_handler(state=AdminStateManagingUser.delete_time_choose_course)
async def managing_users_delete_time_choose_course(callback: types.CallbackQuery, state: FSMContext):
    """Выбор курса для добавления ему времени"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    course_id = int(callback.data[38:])
    await state.update_data(course_id=course_id, message_id=callback.message.message_id)
    await callback.message.edit_text(get_text(user, 'managing_users_delete_time_choose_time'), reply_markup=AdminGenerateKeyboard.managing_users_add_time_choose_time(user))
    await AdminStateManagingUser.delete_time_write_time.set()


@dp.message_handler(state=AdminStateManagingUser.delete_time_write_time)
async def managing_user_add_time_write_time(message: types.Message, state: FSMContext):
    """Ввод времени"""
    data = await state.get_data()
    user = DataBaseFunc.get_user(message.from_user.id)
    try:
        time = int(message.text)
        await state.update_data(time=time)
        await message.delete()
        user_addtime = DataBaseFunc.get_user(data['user_addtime_id'])
        await bot.edit_message_text(text=AdminHelper.get_text_managing_users_delete_time_final(user_addtime, data['course_id'], time),
                                    chat_id=message.chat.id, message_id=data['message_id'],
                                    reply_markup=AdminGenerateKeyboard.managing_users_add_time_final(user))
        await AdminStateManagingUser.delete_time_final.set()
    except:
        await message.delete()
        await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'],
                                    text=get_text(
                                        user, 'managing_user_add_time_write_time_not_str'),
                                    reply_markup=AdminGenerateKeyboard.managing_users_add_time_choose_time(user))


@dp.callback_query_handler(lambda callback: callback.data == "managing_users_add_time_final_add", state=AdminStateManagingUser.delete_time_final)
async def managing_users_delete_time_final_add(callback: types.CallbackQuery, state: FSMContext):
    """Удалить время пользователю в конкретный курс."""
    await callback.answer()
    data = await state.get_data()
    user = DataBaseFunc.get_user(callback.from_user.id)
    user_addtime = DataBaseFunc.get_user(data['user_addtime_id'])
    course = DataBaseFunc.get_course(data['course_id'])
    time = data['time']
    DataBaseFunc.delete_time_in_course(user_addtime, course, time)
    await callback.message.edit_text(get_text(user, 'managing_users_delete_time_final_add'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_users(user))
    await AdminStateManagingUser.main_menu.set()


@dp.callback_query_handler(lambda callback: callback.data == "managing_users_add_time_final_cancel", state=AdminStateManagingUser.delete_time_final)
async def managing_users_add_time_final_cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'admin_menu_managing_users'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_users(user))
    await AdminStateManagingUser.main_menu.set()
#endregion
