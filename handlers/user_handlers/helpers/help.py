from os import stat
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
        cur_subs = DataBaseFunc.get_current_subscribe(user)
        if ((user.is_have_subscription) and (cur_subs != None)):
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
    def get_shedule():
        text = """Расписание курса

15.10 (четверг) - УРОК №1 «Введение»

19.10 (понедельник) - УРОК №2 «Анатомия кожи и типы кожи»

21.10 (среда) - УРОК №3 «Вебинар — Ответы на вопросы»

23.10 (пятница) - УРОК №4 «Ежедневный уход для всех»

26.10 (понедельник) - УРОК №5 «Еженедельный уход для всех»

28.10 (среда) - УРОК №6 «Вебинар — Уход для всех»

30.10 (пятница) - УРОК №7 «Разбор косметички» 

02.11 (понедельник) - УРОК №8 «Массаж и гимнастика лица»

04.11 (среда) - УРОК №9 «Вебинар — Домашняя косметичка»

06.11 (пятница) – УРОК №10 «Косметология»

09.11 (понедельник) – УРОК №11 «Вебинар — Что делать у косметолога?»
"""
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


