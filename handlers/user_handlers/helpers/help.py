from database.models import User
from database.function import DataBaseFunc
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
            info_subscribe = DataBaseFunc.get_current_subscribe(user)
            course = DataBaseFunc.get_course(info_subscribe.course_id)
            data_start = info_subscribe.data_start.strftime("%d.%m-%Y")
            data_end = info_subscribe.data_end.strftime("%d.%m.%Y")
            text += course.name + " " + data_start + "-" + data_end + "\n"
        else:
            text += get_text(user, 'start_button_profile_dont_have_course') + "\n"
        # text += f"*{get_text(user, 'start_button_profile_balance')}*" + str(user.balance)
        return text

    @staticmethod
    def get_history_menu_profile(user: User):
        """Формирует историю подписок пользователя. """
        text = get_text(user, 'menu_profile_history') + "\n\n"

        for purch in user.purchased_subscriptions:
            data_start = purch.data_start.strftime("%d\.%m\.%Y")
            data_end = purch.data_end.strftime("%d\.%m\.%Y")
            text += "• " + f"*{purch.courses.name}* {data_start} \- {data_end}\n"
        
        return text


