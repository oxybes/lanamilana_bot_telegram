from database.function import DataBaseFunc
from database.models import User
from misc import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from config import get_text, TEXTS
from handlers.admin_handlers.helpers.admin_state import AdminStateMainMenu, AdminStateManagingCourses, AdminStateManaginCourseEdit, AdminStateManaginCourseDelete
from handlers.admin_handlers.helpers.generate_keyboard import AdminGenerateKeyboard
from handlers.admin_handlers.helpers.help import AdminHelper


# region Обработка кнопок "Добавить"
@dp.callback_query_handler(lambda callback: callback.data == 'managing_courses_add', state=AdminStateMainMenu.managing_courses)
async def managing_courses_add(callback: types.CallbackQuery, state: FSMContext):
    """Обрабатывает кнопку добавить курс. """
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'managing_courses_add'))
    await state.update_data(message_id=callback.message.message_id, chat_id=callback.message.chat.id)
    await AdminStateManagingCourses.add_course.set()


@dp.message_handler(state=AdminStateManagingCourses.add_course, content_types=types.ContentTypes.TEXT)
async def managing_courses_write_name(message: types.Message, state: FSMContext):
    """Ввод имени при добавлении новой подписки."""
    user = DataBaseFunc.get_user(message.from_user.id)
    await state.update_data(name_course=message.text)
    data = await state.get_data()
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.edit_message_text(text=get_text(user, 'managing_course_add_write_description'), chat_id=data['chat_id'], message_id=data['message_id'])
    await AdminStateManagingCourses.write_description.set()


@dp.message_handler(state=AdminStateManagingCourses.write_description, content_types=types.ContentTypes.TEXT)
async def managing_courses_write_description(message: types.Message, state=FSMContext):
    """Ввод описания при добавлении новой подписки"""
    user = DataBaseFunc.get_user(message.from_user.id)
    await state.update_data(description_course=message.text)
    data = await state.get_data()
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.edit_message_text(text=get_text(user, 'managing_course_add_write_cost'), chat_id=data['chat_id'], message_id=data['message_id'])
    await AdminStateManagingCourses.write_cost.set()


@dp.message_handler(state=AdminStateManagingCourses.write_cost, content_types=types.ContentTypes.TEXT)
async def managin_courses_write_cost(message: types.Message, state=FSMContext):
    """Ввод цены при добавлении новой подписки"""
    user = DataBaseFunc.get_user(message.from_user.id)
    await state.update_data(cost_course=message.text)
    data = await state.get_data()
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.edit_message_text(text=get_text(user, 'managing_course_add_write_time'), chat_id=data['chat_id'], message_id=data['message_id'])
    await AdminStateManagingCourses.write_time.set()


@dp.message_handler(state=AdminStateManagingCourses.write_time, content_types=types.ContentTypes.TEXT)
async def managin_courses_write_time(message: types.Message, state=FSMContext):
    """Ввод времени при добавлении нового курса"""
    user = DataBaseFunc.get_user(message.from_user.id)
    await state.update_data(time_course=message.text)
    data = await state.get_data()
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.edit_message_text(text=get_text(user, 'managing_course_add_channels'), chat_id=data['chat_id'],
                                message_id=data['message_id'], reply_markup=AdminGenerateKeyboard.managing_courses_add_channels_continue(user))
    await AdminStateManagingCourses.add_channels.set()


@dp.callback_query_handler(lambda callback: callback.data == "managing_courses_add_continue", state=AdminStateManagingCourses.add_channels)
async def managing_courses_add_continue(callback: types.CallbackQuery, state: FSMContext):
    """Кнопка продолжить при добавлении курса."""
    user = DataBaseFunc.get_user(callback.from_user.id)
    data = await state.get_data()
    text = AdminHelper.get_text_for_additionaly_course(user, data)
    keyboard = AdminGenerateKeyboard.managing_courses_additionaly(user)
    await callback.message.edit_text(text, parse_mode="markdown", reply_markup=keyboard)
    await AdminStateManagingCourses.confirm.set()


@dp.message_handler(state=AdminStateManagingCourses.add_channels)
async def managing_courses_add_channels(message: types.Message, state=FSMContext):
    """Добавление новых каналов в подписку"""  # -458757767
    user = DataBaseFunc.get_user(message.from_user.id)
    data = await state.get_data()

    if (not ("channels" in data.keys())):
        await state.update_data(channels=[])

    data = await state.get_data()
    channels = data["channels"]

    if (message.forward_from_chat != None):
        id_channel = message.forward_from_chat.id
        full_name_channel = message.forward_from_chat.full_name
        channels.append({"id": id_channel, "name": full_name_channel})

    else:
        try:
            mas_text = message.text.split(':')
            channels.append({"id": mas_text[0], "name": mas_text[1]})
        except:
            pass

    await state.update_data(channels=channels)
    await bot.delete_message(message.chat.id, message.message_id)
    text = AdminHelper.add_channels_in_message(
        get_text(user, 'managing_course_add_channels'), channels)
    await bot.edit_message_text(text=text, chat_id=data['chat_id'], message_id=data['message_id'], reply_markup=AdminGenerateKeyboard.managing_courses_add_channels_continue(user))


@dp.callback_query_handler(lambda callback: callback.data == "managing_courses_add_additionaly_cancel", state=AdminStateManagingCourses.confirm)
async def managing_courses_add_additionaly_cancel(callback: types.CallbackQuery, state: FSMContext):
    """Возвращает в менеджер управления подписками"""
    await state.reset_data()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'admin_menu_managing_courses'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_courses(user))
    await AdminStateMainMenu.managing_courses.set()


@dp.callback_query_handler(lambda callback: callback.data == "managing_courses_add_additionaly_complete", state=AdminStateManagingCourses.confirm)
async def managing_courses_add_additionaly_complete(callback: types.CallbackQuery, state: FSMContext):
    """Добавляет новый курс в базу данных"""
    user = DataBaseFunc.get_user(callback.from_user.id)
    data = await state.get_data()
    DataBaseFunc.create_new_course(data)
    channels = data["channels"]
    channels = []
    await state.update_data(channels = channels)
    await callback.message.edit_text(get_text(user, 'admin_menu_managing_courses'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_courses(user))
    await AdminStateMainMenu.managing_courses.set()
# endregion

# region Обработка кнопок "Редактировать"


@dp.callback_query_handler(lambda callback: callback.data == "managing_courses_edit", state=AdminStateMainMenu.managing_courses)
async def managing_courses_edit(callback: types.CallbackQuery):
    """Обработка кнопки редактировать"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    text = get_text(user, 'managing_courses_edit')
    keyboard = AdminGenerateKeyboard.managing_courses_edit(user)
    await callback.message.edit_text(text, reply_markup=keyboard)
    await AdminStateManaginCourseEdit.get_course.set()


@dp.callback_query_handler(lambda callback: callback.data == "managing_course_edit_back", state=AdminStateManaginCourseEdit.get_course)
async def managing_courses_edit(callback: types.CallbackQuery):
    """Обработка кнопки назад"""
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'admin_menu_managing_courses'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_courses(user))
    await AdminStateMainMenu.managing_courses.set()


@dp.callback_query_handler(state=AdminStateManaginCourseEdit.get_course)
async def managing_course_edit_choose(callback: types.CallbackQuery, state: FSMContext):
    """Обрабатывает редакт конкретного курса"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    course = DataBaseFunc.get_course(int(callback.data[21:]))
    await state.update_data(id_course=course.id)
    text = AdminHelper.get_text_info_course(user, course)
    keyboard = AdminGenerateKeyboard.managing_courses_edit_button(user)
    await callback.message.edit_text(text, parse_mode="markdown", reply_markup=keyboard)
    await AdminStateManaginCourseEdit.choose_edit.set()


# region Обработка колбэков на выбор того, что конкретно редактировать в курсе
@dp.callback_query_handler(lambda callback: callback.data == "managing_courses_edit_name", state=AdminStateManaginCourseEdit.choose_edit)
async def managing_courses_edit_name(callback: types.CallbackQuery, state=FSMContext):
    """Обрабатывает кнопки редактировать имя при выбранном для редакта курсе"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    text = get_text(user, 'managing_courses_edit_name')
    await state.update_data(message_id=callback.message.message_id)
    await callback.message.edit_text(text)
    await AdminStateManaginCourseEdit.edit_name.set()


@dp.message_handler(state=AdminStateManaginCourseEdit.edit_name, content_types=types.ContentTypes.TEXT)
async def managing_courses_edit_name_msg(message: types.Message, state: FSMContext):
    data = await state.get_data()
    new_name = message.text
    course = DataBaseFunc.get_course(data['id_course'])
    course.name = new_name
    DataBaseFunc.commit()
    await message.delete()
    user = DataBaseFunc.get_user(message.from_user.id)
    text = AdminHelper.get_text_info_course(user, course)
    keyboard = AdminGenerateKeyboard.managing_courses_edit_button(user)
    await bot.edit_message_text(text=text, chat_id=message.chat.id, message_id=data['message_id'], reply_markup=keyboard, parse_mode="markdown")
    await AdminStateManaginCourseEdit.choose_edit.set()


@dp.callback_query_handler(lambda callback: callback.data == "managing_courses_edit_description", state=AdminStateManaginCourseEdit.choose_edit)
async def managing_courses_edit_description(callback: types.CallbackQuery, state=FSMContext):
    """Обрабатывает кнопки редактировать описание при выбранном для редакта курсе"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    text = get_text(user, 'managing_courses_edit_description')
    await state.update_data(message_id=callback.message.message_id)
    await callback.message.edit_text(text)
    await AdminStateManaginCourseEdit.edit_description.set()


@dp.callback_query_handler(lambda callback: callback.data == "managing_courses_edit_cost", state=AdminStateManaginCourseEdit.choose_edit)
async def managing_courses_edit_description(callback: types.CallbackQuery, state=FSMContext):
    """Обрабатывает кнопки редактировать цену при выбранном для редакта курсе"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    text = get_text(user, 'managing_courses_edit_cost')
    await state.update_data(message_id=callback.message.message_id)
    await callback.message.edit_text(text)
    await AdminStateManaginCourseEdit.edit_cost.set()


@dp.callback_query_handler(lambda callback: callback.data == "managing_courses_edit_time", state=AdminStateManaginCourseEdit.choose_edit)
async def managing_courses_edit_description(callback: types.CallbackQuery, state=FSMContext):
    """Обрабатывает кнопки редактировать описание при выбранном для редакта курсе"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    text = get_text(user, 'managing_courses_edit_time')
    await state.update_data(message_id=callback.message.message_id)
    await callback.message.edit_text(text)
    await AdminStateManaginCourseEdit.edit_time.set()


@dp.callback_query_handler(lambda callback: callback.data == "managing_courses_edit_access_add", state=AdminStateManaginCourseEdit.choose_edit)
async def managing_courses_edit_description(callback: types.CallbackQuery, state=FSMContext):
    """Обрабатывает кнопки редактировать описание при выбранном для редакта курсе"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    text = get_text(user, 'managing_courses_edit_access_add')
    await state.update_data(message_id=callback.message.message_id)
    await callback.message.edit_text(text)
    await AdminStateManaginCourseEdit.edit_access_add.set()


@dp.callback_query_handler(lambda callback: callback.data == "managing_courses_edit_access_delete", state=AdminStateManaginCourseEdit.choose_edit)
async def managing_courses_edit_description(callback: types.CallbackQuery, state=FSMContext):
    """Обрабатывает кнопки редактировать описание при выбранном для редакта курсе"""
    await callback.answer()
    data = await state.get_data()
    user = DataBaseFunc.get_user(callback.from_user.id)
    text = get_text(user, 'managing_courses_edit_access_delete')
    course = DataBaseFunc.get_course(data['id_course'])
    text = AdminHelper.get_channel_for_managing_courses_edit_access_delete(
        text, course)
    await state.update_data(message_id=callback.message.message_id)
    await callback.message.edit_text(text)
    await AdminStateManaginCourseEdit.edit_access_delete.set()


@dp.callback_query_handler(lambda callback: callback.data == "managing_courses_edit_back", state=AdminStateManaginCourseEdit.choose_edit)
async def managing_courses_edit_back(callback: types.CallbackQuery, state=FSMContext):
    """Вернуться назад к курсам"""
    await callback.answer()
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    text = get_text(user, 'managing_courses_edit')
    keyboard = AdminGenerateKeyboard.managing_courses_edit(user)
    await callback.message.edit_text(text, reply_markup=keyboard)
    await AdminStateManaginCourseEdit.get_course.set()
# endregion

# region Обработка сообщений пользователя для редакта


@dp.message_handler(state=AdminStateManaginCourseEdit.edit_description, content_types=types.ContentTypes.TEXT)
async def managing_courses_edit_description_msg(message: types.Message, state: FSMContext):
    data = await state.get_data()
    new_description = message.text
    course = DataBaseFunc.get_course(data['id_course'])
    course.description = new_description
    DataBaseFunc.commit()
    await message.delete()
    user = DataBaseFunc.get_user(message.from_user.id)
    text = AdminHelper.get_text_info_course(user, course)
    keyboard = AdminGenerateKeyboard.managing_courses_edit_button(user)
    await bot.edit_message_text(text=text, chat_id=message.chat.id, message_id=data['message_id'], reply_markup=keyboard, parse_mode="markdown")
    await AdminStateManaginCourseEdit.choose_edit.set()


@dp.message_handler(state=AdminStateManaginCourseEdit.edit_cost, content_types=types.ContentTypes.TEXT)
async def managing_courses_edit_name_msg(message: types.Message, state: FSMContext):
    data = await state.get_data()
    new_cost = message.text
    course = DataBaseFunc.get_course(data['id_course'])
    course.cost = int(new_cost)
    DataBaseFunc.commit()
    await message.delete()
    user = DataBaseFunc.get_user(message.from_user.id)
    text = AdminHelper.get_text_info_course(user, course)
    keyboard = AdminGenerateKeyboard.managing_courses_edit_button(user)
    await bot.edit_message_text(text=text, chat_id=message.chat.id, message_id=data['message_id'], reply_markup=keyboard, parse_mode="markdown")
    await AdminStateManaginCourseEdit.choose_edit.set()


@dp.message_handler(state=AdminStateManaginCourseEdit.edit_time, content_types=types.ContentTypes.TEXT)
async def managing_courses_edit_name_msg(message: types.Message, state: FSMContext):
    data = await state.get_data()
    new_time = message.text
    course = DataBaseFunc.get_course(data['id_course'])
    course.time = int(new_time)
    DataBaseFunc.commit()
    await message.delete()
    user = DataBaseFunc.get_user(message.from_user.id)
    text = AdminHelper.get_text_info_course(user, course)
    keyboard = AdminGenerateKeyboard.managing_courses_edit_button(user)
    await bot.edit_message_text(text=text, chat_id=message.chat.id, message_id=data['message_id'], reply_markup=keyboard, parse_mode="markdown")
    await AdminStateManaginCourseEdit.choose_edit.set()


@dp.message_handler(state=AdminStateManaginCourseEdit.edit_access_add)
async def managing_courses_edit_access_msg(message: types.Message, state: FSMContext):
    user = DataBaseFunc.get_user(message.from_user.id)
    data = await state.get_data()
    DataBaseFunc.add_channel_in_course(message, data)
    await message.delete()
    course = DataBaseFunc.get_course(data['id_course'])
    text = AdminHelper.get_text_info_course(user, course)
    keyboard = AdminGenerateKeyboard.managing_courses_edit_button(user)
    await bot.edit_message_text(text=text, chat_id=message.chat.id, message_id=data['message_id'], reply_markup=keyboard, parse_mode="markdown")
    await AdminStateManaginCourseEdit.choose_edit.set()


@dp.message_handler(state=AdminStateManaginCourseEdit.edit_access_delete)
async def managing_courses_edit_access_delete_msg(message: types.Message, state: FSMContext):
    user = DataBaseFunc.get_user(message.from_user.id)
    data = await state.get_data()
    id_ch_course = int(message.text)
    DataBaseFunc.delete_channel_in_courses(id_ch_course)
    course = DataBaseFunc.get_course(data['id_course'])
    text = AdminHelper.get_text_info_course(user, course)
    keyboard = AdminGenerateKeyboard.managing_courses_edit_button(user)
    await message.delete()
    await bot.edit_message_text(text=text, chat_id=message.chat.id, message_id=data['message_id'], reply_markup=keyboard, parse_mode="markdown")
    await AdminStateManaginCourseEdit.choose_edit.set()
# endregion

# endregion

# region Обработка кнопки "Удалить"


@dp.callback_query_handler(lambda callback: callback.data == "managing_courses_delete", state=AdminStateMainMenu.managing_courses)
async def managing_courses_delete(callback: types.CallbackQuery):
    """Обработка кнопки удалить"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    text = get_text(user, 'managing_courses_delete')
    keyboard = AdminGenerateKeyboard.managing_courses_delete(user)
    await callback.message.edit_text(text, reply_markup=keyboard)
    await AdminStateManaginCourseDelete.get_course.set()


@dp.callback_query_handler(lambda callback: callback.data == "managin_courses_delete_back", state="*")
async def managing_courses_delete_back(callback: types.CallbackQuery):
    """Обработка кнопки назад"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'admin_menu_managing_courses'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_courses(user))
    await AdminStateMainMenu.managing_courses.set()


@dp.callback_query_handler(state=AdminStateManaginCourseDelete.get_course)
async def managing_courses_delete_choose(callback: types.CallbackQuery):
    """Удаление конкретно выбранного курса"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    course = DataBaseFunc.get_course(int(callback.data[23:]))
    course.is_delete = True
    DataBaseFunc.commit()
    await callback.message.edit_text(get_text(user, 'admin_menu_managing_courses'), reply_markup=AdminGenerateKeyboard.admin_menu_managing_courses(user))
    await AdminStateMainMenu.managing_courses.set()

# endregion
