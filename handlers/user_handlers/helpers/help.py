from database.models import User
from config import get_text

class UserHelp:
    """Класс помогает формировать некоторые функции для обработки User_Handlers"""

    @staticmethod
    def get_start_menu_button_profile_text(user: User, text):
        """Формирует текст для информации профиля."""
        text += '\n\n'
        text += f"*{get_text(user,'start_button_profile_id')}*" + str(user.id) + "\n"
        text += f"*{get_text(user, 'start_button_profile_current_course')}*"

        if (user.is_have_subscription):
            raise Exception() #реализовать вывод курса
        else:
            text += get_text(user, 'start_button_profile_dont_have_course') + "\n"
        text += f"*{get_text(user, 'start_button_profile_balance')}*" + str(user.balance)
        return text

