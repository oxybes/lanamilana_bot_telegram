import re
from sqlalchemy.orm import session
from database.function import DataBaseFunc
from database.models import Contact, User
from misc import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from config import get_text, TEXTS, get_text_but
from handlers.user_handlers.helpers.generator_keyboards import UserGeneratorKeyboard
from handlers.user_handlers.helpers.user_state import UserStateMainMenu, UserStateRegister
from handlers.admin_handlers.helpers.admin_state import AdminStateMainMenu
from handlers.admin_handlers.helpers.generate_keyboard import AdminGenerateKeyboard


@dp.message_handler(commands = ['start'], state = '*')
async def start_message(message: types.Message):
    """Обработчик команды /start."""

    user = DataBaseFunc.get_user(message.from_user.id)
    await message.delete()

    if user == None:
        user = User(id = message.from_user.id, username=message.from_user.username, chat_id=message.chat.id)
        DataBaseFunc.add(user)
        DataBaseFunc.commit()
        info_mes = await message.answer(get_text(user, 'register'), reply_markup=UserGeneratorKeyboard.register_button(user))
        user.last_message_id_bot = info_mes.message_id
        await UserStateRegister.main_menu.set()

    elif user.is_register == False:
        info_mes = await message.answer(get_text(user, 'register'), reply_markup=UserGeneratorKeyboard.register_button(user))
        user.last_message_id_bot = info_mes.message_id
        await UserStateRegister.main_menu.set()

    else:
        if user.last_message_id_bot:
            await bot.delete_message(chat_id=message.chat.id, message_id=user.last_message_id_bot)
        await message.answer(get_text(user,'start'), reply_markup=UserGeneratorKeyboard.start_button(user))
        await UserStateMainMenu.main_menu.set()


@dp.callback_query_handler(lambda callback : callback.data == "register_write_back", state='*')
async def register_write_back(callback : types.CallbackQuery):
    """Прекратить ввод номера или почты при регистрации."""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    await callback.message.edit_text(get_text(user, 'register'), reply_markup=UserGeneratorKeyboard.register_button(user))
    await UserStateRegister.main_menu.set()

@dp.callback_query_handler(lambda callback : callback.data == "register_phone", state=UserStateRegister.main_menu)
async def register_phone(callback : types.CallbackQuery, state : FSMContext):
    """Обработчик кнопки войти по телефону."""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(get_text_but(user, 'register_write_back'), callback_data="register_write_back"))
    await state.update_data(callback_message_id = callback.message.message_id)
    await callback.message.edit_text(get_text(user, 'register_phone_write'), reply_markup=keyboard)
    await UserStateRegister.write_phone.set()

@dp.callback_query_handler(lambda callback : callback.data == "register_mail", state=UserStateRegister.main_menu)
async def register_mail(callback : types.CallbackQuery, state : FSMContext):
    """Обработчик кнопки войти по почте."""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(get_text_but(user, 'register_write_back'), callback_data="register_write_back"))
    await callback.message.edit_text(get_text(user, 'register_mail_write'), reply_markup=keyboard)
    await state.update_data(callback_message_id = callback.message.message_id)
    await UserStateRegister.write_mail.set()


@dp.message_handler(state = UserStateRegister.write_phone)
async def register_phone_write(message : types.Message, state : FSMContext):
    """Ввод номера телефона."""
    await message.delete()
    user = DataBaseFunc.get_user(message.from_user.id)
    data = await state.get_data()
    message_id = data['callback_message_id']
    phone = "".join(ch for ch in message.text if  ch.isdigit())
    errors = get_text(user, 'write_phone_errors')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(get_text_but(user, 'register_write_back'), callback_data="register_write_back"))
    
    if len(phone) == 0:
        await bot.edit_message_text(text=errors['empty'], chat_id=message.chat.id, message_id=message_id, reply_markup=keyboard)
        return

    check_user = DataBaseFunc.get_user_for_phone(phone)
    if (check_user != None):
        await bot.edit_message_text(text=errors['is_register'], chat_id=message.chat.id, message_id=message_id, reply_markup=keyboard)
        return

    contact = DataBaseFunc.get_contact(phone=phone)
    if (contact == None):
        await bot.edit_message_text(text=errors['not_found'], chat_id=message.chat.id, message_id=message_id, reply_markup=keyboard)
        return
    
    user.phone = phone
    user.mail = contact.mail
    user.is_register = True
    user.course_id = contact.course_id
    contact.is_register = True
    DataBaseFunc.commit()
    
    ###### УБРАТЬ ТЕСТОВОЕ ДОБАВЛЕНИЕ КУРСОВ ######
    DataBaseFunc.add_course_in_user_test(user, DataBaseFunc.get_course(user.course_id))
    await bot.edit_message_text(text=get_text(user, 'start'), chat_id=message.chat.id, message_id=message_id, reply_markup=UserGeneratorKeyboard.start_button(user))
    await UserStateMainMenu.main_menu.set()
    


@dp.message_handler(state = UserStateRegister.write_mail)
async def register_mail_write(message : types.Message, state : FSMContext):
    """Ввод номера телефона."""
    await message.delete()
    user = DataBaseFunc.get_user(message.from_user.id)
    data = await state.get_data()
    message_id = data['callback_message_id']
    mail = message.text
    errors = get_text(user, 'write_mail_errors')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(get_text_but(user, 'register_write_back'), callback_data="register_write_back"))
    
    if  ("@" in mail) == False:
        await bot.edit_message_text(text=errors['empty'], chat_id=message.chat.id, message_id=message_id, reply_markup=keyboard)
        return

    check_user = DataBaseFunc.get_user_for_mail(mail)
    if (check_user != None):
        await bot.edit_message_text(text=errors['is_register'], chat_id=message.chat.id, message_id=message_id, reply_markup=keyboard)
        return

    contact = DataBaseFunc.get_contact(mail=mail)
    if (contact == None):
        await bot.edit_message_text(text=errors['not_found'], chat_id=message.chat.id, message_id=message_id, reply_markup=keyboard)
        return
    
    user.mail = mail
    user.phone = contact.phone
    user.is_register = True
    contact.is_register = True
    user.course_id = contact.course_id
    DataBaseFunc.commit()

    ###### УБРАТЬ ТЕСТОВОЕ ДОБАВЛЕНИЕ КУРСОВ ######
    DataBaseFunc.add_course_in_user_test(user, DataBaseFunc.get_course(user.course_id))
    await bot.edit_message_text(text=get_text(user, 'start'), chat_id=message.chat.id, message_id=message_id, reply_markup=UserGeneratorKeyboard.start_button(user))
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

    