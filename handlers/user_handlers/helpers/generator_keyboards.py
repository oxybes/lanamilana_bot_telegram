from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TEXTS, get_text_but
from database.models import User, Course
from database.function import DataBaseFunc


class UserGeneratorKeyboard():
    """Генерирует клавиатуру для пользователей""" 

    @staticmethod
    def choose_lng() -> InlineKeyboardMarkup:
        """Генерирует клавиатуру для выбора языка при инициализации пользователя."""
        but = []
        for key in TEXTS.keys():
            if not isinstance(TEXTS[key],dict):
                continue
            b = InlineKeyboardButton(key, callback_data=f"chs_lng_{key}")
            but.append(b)

        keyboard = InlineKeyboardMarkup()
        keyboard.row(*but)
        return keyboard

    @staticmethod
    def start_button(user: User) -> InlineKeyboardMarkup:
        """Генерирует клавиатуру для команды /start"""
        keyboard = InlineKeyboardMarkup()
        buttons = []
        if (user.subscribe_end == True):
            buttons.append(InlineKeyboardButton(get_text_but(user,'subscribe_continue_pay'), callback_data='subscribe_continue_pay'))
        for key, value in get_text_but(user, 'start_menu').items():
            but = InlineKeyboardButton(value, callback_data=f"start_menu_{key}")
            if (key == 'admin') and (not user.is_admin):
                continue
            buttons.append(but)

        
        keyboard.row_width = 1
        keyboard.add(*buttons)
        # keyboard.row(*buttons)
        return keyboard


    @staticmethod
    def register_button(user: User) -> InlineKeyboardMarkup:
        """Генерирует кнопки регистрации пользователя."""
        keyboard = InlineKeyboardMarkup(row_width=1)
        phone = InlineKeyboardButton(get_text_but(user, 'register_phone'), callback_data="register_phone")
        mail = InlineKeyboardButton(get_text_but(user, 'register_mail'), callback_data="register_mail")
        contact = InlineKeyboardButton(get_text_but(user, 'register_contact'), callback_data="register_contact", url=get_text_but(user, 'register_contact_url'))
        keyboard.add(phone, mail, contact)
        return keyboard

    @staticmethod
    def main_menu_subscribe(user: User) -> InlineKeyboardMarkup:
        """Генерирует клавиатуру для выбора тарифа"""
        keyboard = InlineKeyboardMarkup()

        courses = DataBaseFunc.get_courses()
        for course in courses:
            but = InlineKeyboardButton(text=f"{course.name}", callback_data=f"main_menu_subscrube_{course.id}")
            keyboard.add(but)

        keyboard.add(InlineKeyboardButton(text=get_text_but(user, "main_menu_back"), callback_data="main_menu_back"))

        return keyboard

    @staticmethod
    def menu_profile_history(user:User) -> InlineKeyboardMarkup:
        """Возвращает кнопку "Назад" в истории платежей пользователя"""
        keyboard  = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text=get_text_but(user, 'profile_menu_back'), callback_data="menu_profile_history_back"))
        return keyboard

    @staticmethod
    def course_back_in_list(user: User) -> InlineKeyboardMarkup:
        """Вовзращает кнопку "Назад" при выборе какого-либо курса"""
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text=get_text_but(user, 'profile_menu_back'), callback_data="course_back_in_list"))
        return keyboard

    @staticmethod
    def profile_button(user: User) -> InlineKeyboardMarkup:
        """Генерирует клавиатуру для кнопки "Профиль" """
        keyboard = InlineKeyboardMarkup(row_width=2)
        buttons = []

        for key, val in get_text_but(user, 'profile_menu').items():
            but = InlineKeyboardButton(val, callback_data=f'profile_menu_{key}')
            buttons.append(but)
        keyboard.add(*buttons)
        return keyboard


    @staticmethod
    def get_user_courses(user : User) -> InlineKeyboardMarkup:
        """Формирует кнопки с выбором купленных курсов у пользователя."""

        keyboard = InlineKeyboardMarkup(row_width=2)
        buttons = []

        for purch in DataBaseFunc.get_user_subscribes(user):
            buttons.append(InlineKeyboardButton(purch.courses.name, callback_data=f"access_menu_get_course_{purch.courses.id}"))
        
        keyboard.add(*buttons)
        keyboard.add(InlineKeyboardButton(get_text_but(user, 'access_menu_get_course_back'), callback_data="access_menu_get_course_back"))
        return keyboard

    @staticmethod
    async def get_user_channels(user : User) -> InlineKeyboardMarkup:
        """Формирует кнопки со всеми доступными каналами пользователя"""
        keyboard = InlineKeyboardMarkup(row_width=2)
        buttons = []
        channels = []

        for purch in DataBaseFunc.get_user_subscribes(user):
            for channel in purch.courses.channels:
                ids = [x.id for x in channels]
                if (channel.channel_id in ids) == False:
                    channels.append(channel.channels)
      
        for channel in channels:
            if channel.link == None:
                await DataBaseFunc.create_link_invoice(channel)
            buttons.append(InlineKeyboardButton(channel.name, callback_data=f"access_menu_get_channels_{channel.id}", url=channel.link))

        keyboard.add(*buttons)
        keyboard.add(InlineKeyboardButton(get_text_but(user, 'get_access_choose_channels_back'), callback_data="get_access_choose_channels_back"))

        return keyboard

    @staticmethod
    async def get_channels_from_course(user : User, course : Course) -> InlineKeyboardMarkup:
        """Формирует кнопки с выбором каналлов или чатов для вступления в них"""

        keyboard = InlineKeyboardMarkup(row_width=2)
        buttons = []

        for channel in course.channels:
            if (channel.channels.link == None):
                await DataBaseFunc.create_link_invoice(channel.channels)
            buttons.append(InlineKeyboardButton(channel.channels.name, callback_data=f"access_menu_get_channels_{channel.channels.id}", url=channel.channels.link))
        keyboard.add(*buttons)
        keyboard.add(InlineKeyboardButton(get_text_but(user, 'get_access_choose_channels_back'), callback_data="get_access_choose_channels_back"))

        return keyboard


    @staticmethod
    def get_keyboard(*buttons):
        keyboard = InlineKeyboardMarkup()
        for but in buttons:
            keyboard.add(but)
        return keyboard
