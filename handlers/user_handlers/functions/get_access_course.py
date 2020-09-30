from database.function import DataBaseFunc
from database.models import User
from misc import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from config import get_text, TEXTS
from handlers.user_handlers.helpers.generator_keyboards import UserGeneratorKeyboard
from handlers.user_handlers.helpers.help import UserHelp
from handlers.user_handlers.helpers.user_state import UserStateProfile, UserStateGetAccessCourse, UserStateMainMenu


@dp.callback_query_handler(lambda callback: callback.data == "start_menu_get_access", state = '*')
async def start_menu_get_access(callback : types.CallbackQuery):
    """Отправляет меню с доступными курсами для того, чтобы пользователь мог вступить в них."""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)

    if (user.is_have_subscription == False):
        text = get_text(user, 'get_access_main_menu_no_courses')
    else:
        text = get_text(user, 'get_access_main_menu')

    keyboard = await UserGeneratorKeyboard.get_user_channels(user)

    await callback.message.edit_text(text= text, reply_markup=keyboard)
    await UserStateGetAccessCourse.choose_course.set()

@dp.callback_query_handler(lambda callback: callback.data == "access_menu_get_course_back", state ='*')
async def get_access_main_menu_back(callback : types.CallbackQuery):
    """Кнпка назад, возвращает пользователя в главное меню"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'start'), reply_markup=UserGeneratorKeyboard.start_button(user))
    await UserStateMainMenu.main_menu.set()

@dp.callback_query_handler(lambda callback : callback.data == "get_access_choose_channels_back", state = UserStateGetAccessCourse.choose_course)
async def get_access_choose_channels_back(callback : types.CallbackQuery):
    """Возвращает пользователя обратно в выбор курса"""
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user,'start'), reply_markup=UserGeneratorKeyboard.start_button(user))
    await UserStateMainMenu.main_menu.set()

@dp.callback_query_handler(state = UserStateGetAccessCourse.choose_course)
async def get_link_for_access_course(callback : types.CallbackQuery):
    """Обработчик выбора курса для которого получить ссылки на каналы и чаты"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    id_course = int(callback.data[23:])
    course = DataBaseFunc.get_course(id_course)
    text = get_text(user, 'get_access_choose_channels')
    keyboard = await UserGeneratorKeyboard.get_channels_from_course(user, course)
    await callback.message.edit_text(text, reply_markup=keyboard)
    await UserStateGetAccessCourse.choose_channels.set()



