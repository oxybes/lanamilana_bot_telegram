from datetime import datetime
from aiogram import types
from aiogram.types import contact
from config import get_text, get_text_but
from database.models import User, Course
from database.function import DataBaseFunc

class AdminHelper():
    """Помощник для админ-панели"""
    
    @staticmethod
    def add_channels_in_message(text, channels):
        for ch in channels:
            text += str(ch['id'])+ " : " + str(ch['name']) + "\n"
        text = AdminHelper.escape_telegrambot_underscore(text)
        return text

    @staticmethod
    def get_text_for_additionaly_course(user, data):
        """Формирует форму с информацией о добавляемом курсе"""
        data_text = get_text(user, 'managing_course_confirm')
        text = f"""*{data_text['name']}*: {data['name_course']}
*{data_text['description']}*: {data['description_course']}
*{data_text['cost']}*: {data['cost_course']}
*{data_text['time']}*: {data['time_course']}
*{data_text['access']}*:\n"""

        for ch in data['channels']:
            text = text + f"  *{ch['name']}*\n"
        text = AdminHelper.escape_telegrambot_underscore(text)
        return text

    @staticmethod
    def get_text_info_course(user : Course, course : User) -> str:
        """Формирует текст с информацией о курсе."""
        data_text  = get_text(user, 'managing_courses_edit_info')
        text = f"""*{data_text['name']}*: {course.name}
*{data_text['description']}*: {course.description}
*{data_text['cost']}*: {course.cost}
*{data_text['time']}*: {course.time}
*{data_text['access']}*:\n"""

        for ch in course.channels:
            text = text + f"  *{ch.channels.name}*\n"
        text = AdminHelper.escape_telegrambot_underscore(text)
        return text


    @staticmethod
    def get_whos_admin(user):
        text = "Контакты, которые не прошли регистрацию в боте:\n---------\n"
        for contact in DataBaseFunc.get_contacts():
            text += f"• {contact.phone}\n• {contact.mail}\n---------\n"
        text = AdminHelper.escape_telegrambot_underscore(text)
        return text


    @staticmethod
    def get_channel_for_managing_courses_edit_access_delete(text, course):
        """Добавляет номера каналов."""
        text += "\n"
        for channel in course.channels:
            text = text + f"{channel.id}  {channel.channels.name}\n"
        text = AdminHelper.escape_telegrambot_underscore(text)
        return text


    @staticmethod
    def get_user_from_message(message : types.Message):
        """Возвращает пользователя из сообщения администратора"""
        if (message.forward_from):
            user = DataBaseFunc.get_user(message.forward_from.id)
            if (user == None):
                user = User(id=message.forward_from.id, username=message.forward_from.username, is_register = True, lng = "Russian")
                DataBaseFunc.add(user)
            return user
            

        else:
            return DataBaseFunc.get_user(message.text)
            
    @staticmethod
    def managing_users_get_info_user(admin_user : User, user:User, course_id):
        """Возврщаает инфорацию о пользователе при добавлении курса"""
        text = get_text(admin_user, 'managing_users_get_info_user')
        subs = "• "
        for ph in [purch for purch in user.purchased_subscriptions if purch.data_end > datetime.now()]:
            subs += ph.courses.name + '\n• '
        text = text.format(username=user.username, id=user.id, subs=subs[:-2])
        course = DataBaseFunc.get_course(course_id)
        text += f"\n*Добавляемая подписка:* {course.name}"
        text = AdminHelper.escape_telegrambot_underscore(text)
        return text

    @staticmethod
    def get_info_for_delete_course(user : User, user_delete_id, course_id):
        """Генерирут тект с иформацией о пользователе для подтверждения удаления курса о пользователе

        Args:
            user (User): [Объект администратура]
            user_delete_id ([int]): [id пользователя у которого удаляем курс]
            course_id ([int]): [id удаляемого курса]
        """
        user_delete = DataBaseFunc.get_user(user_delete_id)
        course = DataBaseFunc.get_course(course_id)
        text = f"*Пользователь:* {user_delete.username}\n"
        text += f"*Активные курсы пользователя:* "
        for ph in DataBaseFunc.get_user_subscribes(user_delete):
            text += f"{ph.courses.name}, "
        text = text[:-2]
        text += "\n"
        text += f"*Удаляемый курс:* {course.name}"
        text = AdminHelper.escape_telegrambot_underscore(text)
        return text

    @staticmethod
    def get_text_managing_users_add_time_final(user : User, course_id : int, time : int) -> str:
        """Возвращает текст с информацией о добавлении времени польователю в определенный курс

        Args:
            user (User): [Пользователь, которому добавить курс]
            course_id (int): [ID курса, в который добавить время]
            time (int): [Время в днях.]

        Returns:
            str: [Сформированный текст с инфомрацей]
        """

        course = DataBaseFunc.get_course(course_id)
        text = f"*Пользователь:* {user.username}\n"
        text += f"*Активные курсы пользователя:* "
        for ph in DataBaseFunc.get_user_subscribes(user):
            text += f"{ph.courses.name}, "
        text = text[:-2]
        text += "\n"
        text += f"*Курс, в который добавить время:* {course.name}\n"
        text += f"*Количество добавляемых дней:* {time}"
        text = AdminHelper.escape_telegrambot_underscore(text)
        return text

    @staticmethod
    def get_text_managing_users_delete_time_final(user : User, course_id : int, time : int) -> str:
        """Возвращает текст с информацией о добавлении времени польователю в определенный курс

        Args:
            user (User): [Пользователь, которому добавить курс]
            course_id (int): [ID курса, в который добавить время]
            time (int): [Время в днях.]

        Returns:
            str: [Сформированный текст с инфомрацей]
        """

        course = DataBaseFunc.get_course(course_id)
        text = f"*Пользователь:* {user.username}\n"
        text += f"*Активные курсы пользователя:* "
        for ph in DataBaseFunc.get_user_subscribes(user):
            text += f"{ph.courses.name}, "
        text = text[:-2]
        text += "\n"
        text += f"*Курс, в котором убавить время:* {course.name}\n"
        text += f"*Количество убавляемых дней:* {time}"
        text = AdminHelper.escape_telegrambot_underscore(text)
        return text

    @staticmethod
    def get_list_admins(user):
        """ВОзвращает список администраторов бота"""
        data = get_text(user, 'get_list_admins')
        users = DataBaseFunc.get_all_admins()
        text = f"*{data['admin']}*\n"
        for admin in users:
            text += "• " + AdminHelper.escape_telegrambot_underscore(admin.username) + "\n"
        text = text[:-1]
        return text


    @staticmethod
    def escape_telegrambot_underscore(txt):
        return txt.replace("_", "\\_")

    @staticmethod
    def get_whos(user):
        text = ""
