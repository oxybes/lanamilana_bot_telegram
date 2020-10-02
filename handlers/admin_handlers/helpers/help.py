from datetime import datetime
from aiogram import types
from config import get_text, get_text_but
from database.models import User, Course
from database.function import DataBaseFunc

class AdminHelper():
    """Помощник для админ-панели"""
    
    @staticmethod
    def add_channels_in_message(text, channels):
        for ch in channels:
            text += str(ch['id'])+ " : " + str(ch['name']) + "\n"
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

        return text

    @staticmethod
    def get_channel_for_managing_courses_edit_access_delete(text, course):
        """Добавляет номера каналов."""
        text += "\n"
        for channel in course.channels:
            text = text + f"{channel.id}  {channel.channels.name}\n"
        return text


    @staticmethod
    def get_user_from_message(message : types.Message):
        """Возвращает пользователя из сообщения администратора"""
        if (message.forward_from):
            return DataBaseFunc.get_user(message.from_user.id)
        else:
            return DataBaseFunc.get_user(message.text)
            
    @staticmethod
    def managing_users_get_info_user(admin_user : User, user:User):
        """Возврщаает инфорацию о пользователе при добавлении курса"""
        text = get_text(admin_user, 'managing_users_get_info_user')
        subs = "• "
        for ph in [purch for purch in user.purchased_subscriptions if purch.data_end > datetime.now()]:
            subs += ph.courses.name + '\n• '
        text = text.format(username=user.username, id=user.id, subs=subs[:-1])
        return text