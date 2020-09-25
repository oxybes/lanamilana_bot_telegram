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

        for value in get_text_but(user, 'start_menu'):
            for key, val in value.items():
                but = InlineKeyboardButton(val, callback_data=f'start_menu_{key}')
            buttons.append(but)
        
        keyboard.row_width = 1
        keyboard.add(*buttons)
        # keyboard.row(*buttons)
        return keyboard


    @staticmethod
    def main_menu_subscribe(user: User) -> InlineKeyboardMarkup:
        """Генерирует клавиатуру для выбора тарифа"""
        keyboard = InlineKeyboardMarkup()

        courses = DataBaseFunc.get_courses()
        for course in courses:
            but = InlineKeyboardButton(text=f"{course.name} {course.time}д. {course.cost}р.", callback_data=f"main_menu_subscrube_{course.id}")
            keyboard.add(but)

        keyboard.add(InlineKeyboardButton(text=get_text_but(user, "main_menu_back"), callback_data="main_menu_back"))

        return keyboard

        

        


    @staticmethod
    def profile_button(user: User) -> InlineKeyboardMarkup:
        """Генерирует клавиатуру для кнопки "Профиль" """
        keyboard = InlineKeyboardMarkup(row_width=2)
        buttons = []

        for value in get_text_but(user, 'profile_menu'):
            for key, val in value.items():
                but = InlineKeyboardButton(val, callback_data=f'profile_menu_{key}')
            buttons.append(but)
        keyboard.add(*buttons)
        return keyboard


    @staticmethod
    def get_keyboard(*buttons):
        keyboard = InlineKeyboardMarkup()
        for but in buttons:
            keyboard.add(but)
        return keyboard
