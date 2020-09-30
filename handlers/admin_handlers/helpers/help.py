from config import get_text, get_text_but
from database.models import User, Course

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
