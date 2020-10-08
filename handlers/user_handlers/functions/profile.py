from database.function import DataBaseFunc
from database.models import User
from misc import dp, bot
from aiogram import types
from config import get_text, TEXTS
from handlers.user_handlers.helpers.generator_keyboards import UserGeneratorKeyboard
from handlers.user_handlers.helpers.help import UserHelp
from handlers.user_handlers.helpers.user_state import UserStateMainMenu, UserStateProfile

@dp.callback_query_handler(lambda callback: callback.data == "start_menu_profile", state='*')
async def start_menu_profile(callback_query: types.CallbackQuery):
    """Обработчик кнопки "Профиль" из главного меню пользователя."""
    await callback_query.answer()
    user = DataBaseFunc.get_user(callback_query.from_user.id)
    await callback_query.message.edit_text(text=UserHelp.get_start_menu_button_profile_text(user, get_text(user, 'start_button_profile')),
                                           parse_mode='markdown',
                                           reply_markup=UserGeneratorKeyboard.profile_button(user))
    await DataBaseFunc.delete_messages_from_callback(user, callback_query.message.message_id)
    await UserStateProfile.menu_profile.set()

    
@dp.callback_query_handler(lambda callback: callback.data == "profile_menu_language", state=UserStateProfile.menu_profile)
async def menu_profile_language(callback:types.CallbackQuery):
    """Обработчик кнопки смены языка из меню профиля."""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(text=TEXTS["selected_language"], reply_markup=UserGeneratorKeyboard.choose_lng())
    await UserStateProfile.choose_language.set()


@dp.callback_query_handler(state=UserStateProfile.choose_language)
async def menu_profile_choose_language(callback_query:types.CallbackQuery):
    """Обработка выбора языка по кнопке смены."""
    await callback_query.answer()
    user = DataBaseFunc.get_user(callback_query.from_user.id)
    lng = callback_query.data[8:]
    user.lng = lng
    DataBaseFunc.commit()
    await start_menu_profile(callback_query)
    await UserStateProfile.menu_profile.set()

@dp.callback_query_handler(lambda callback: callback.data == "profile_menu_history_subscribe",state=UserStateProfile.menu_profile)
async def menu_profile_up_balance(callback:types.CallbackQuery):
    """Обработка кнопки посмотреть историю подписок."""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(text = UserHelp.get_history_menu_profile(user), parse_mode=types.ParseMode.MARKDOWN_V2, reply_markup=UserGeneratorKeyboard.menu_profile_history(user))
    await UserStateProfile.history.set()

@dp.callback_query_handler(lambda callback: callback.data == "menu_profile_history_back", state = UserStateProfile.history)
async def menu_profile_histroy_back(callback: types.CallbackQuery):
    """Обработчик кнопки назад из меню истории платежей пользователя"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(text=UserHelp.get_start_menu_button_profile_text(user, get_text(user, 'start_button_profile')),
                                           parse_mode='markdown',
                                           reply_markup=UserGeneratorKeyboard.profile_button(user))
    await UserStateProfile.menu_profile.set()

@dp.callback_query_handler(state=UserStateProfile.menu_profile)
async def menu_profile_back_main_menu(callback:types.CallbackQuery):
    """Обработка кнопки вернутся в главное меню"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(text = get_text(user, 'start'),reply_markup=UserGeneratorKeyboard.start_button(user))
    await UserStateMainMenu.main_menu.set()



