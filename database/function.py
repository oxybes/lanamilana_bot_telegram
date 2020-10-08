from datetime import datetime, timedelta

from requests.api import delete
from .models import User, Course, PurchasedSubscription, Channel, ChannelsInCourse, Contact
from config import MAIN_ADMIN_ID
from .mics import session, metadata, engine
from aiogram import types
from typing import List, Dict
from misc import bot
from sqlalchemy import or_


class DataBaseFunc():
    """Класс для работы с базой данных.
       Содержит в себе функции по управлению БД"""

    # region Иницикализация базы данных при первоначальном запуске для отладки

    @staticmethod
    def add_main_admin() -> None:
        """Добавляет главного администратора при инициализации базы данных"""
        user = session.query(User).filter_by(id=MAIN_ADMIN_ID).first()
        if user == None:
            user = User(id=MAIN_ADMIN_ID, username="oxybes",
                        is_admin=True, is_main_admin=True, lng='Russian', course_id=1, chat_id=454709994, is_register=True)
            session.add(user)
            session.commit()
            return
        if user.is_admin == False:
            user.is_admin = True
            session.commit()

    @staticmethod
    def add_admin_eduard() -> None:
        user = session.query(User).filter_by(id=768383734).first()
        if user == None:
            user = User(id=768383734, username="powered6263",
                        is_admin=True, is_main_admin=True, lng='Russian', is_register = True, course_id = 1)
            session.add(user)
            session.commit()

    @staticmethod
    def add_course_in_me() -> None:
        user = DataBaseFunc.get_user(int(MAIN_ADMIN_ID))
        user.is_register = True
        courses = DataBaseFunc.get_courses()
        for cs in courses:
            date = datetime.now()
            purch = PurchasedSubscription(user_id=user.id, course_id=cs.id,
                                        data_start=date, data_end=date + timedelta(minutes=2))
            user.is_have_subscription = True
            session.add(purch)
            session.commit()

    @staticmethod
    def add_second_test_acc():
        user = session.query(User).filter_by(id=976016932).first()
        if user == None:
            user = User(id=976016932, username="oxybeswork",
                        is_admin=True, is_main_admin=True, lng='Russian', is_register=True)
            session.add(user)
            session.commit()
            courses = DataBaseFunc.get_courses()
            for cs in courses:
                DataBaseFunc.add_course_in_user(user, cs)
                break

    @staticmethod
    def generate_course() -> None:
        """Инициализирует курсы в базе данных."""
        courses = session.query(Course).all()
        if len(courses) == 0:
            course = Course(name="Доступ в группу",
                            description="Дает доступ в группу", time=1, cost=500)
            session.add(course)
            channel = Channel(id="-458757767", name="fdsf")
            session.add(channel)
            session.commit()
            ch_in_course = ChannelsInCourse(
                course_id=course.id, channel_id=channel.id)
            session.add(ch_in_course)
            course2 = Course(name="Доступ в канал",
                             description="Дает доступ в канал", time=1, cost=500)
            session.add(course2)
            channel2 = Channel(id="-1001321466625", name="test_my_channel")
            session.add(channel2)
            session.commit()
            ch_in_course2 = ChannelsInCourse(
                course_id=course2.id, channel_id=channel2.id)
            session.add(ch_in_course2)
            session.commit()

    @staticmethod
    def add_my_contact():
        contact = session.query(Contact).filter(or_(Contact.mail=="oxybes@mail.ru", Contact.phone=="79504905979")).first()
        if (contact == None):
            contact = Contact(phone='79504905979', mail='oxybes@mail.ru')
            session.add(contact)
            session.commit()


    @staticmethod
    def add_contact(phone, mail, course_id):
        contact = session.query(Contact).filter(or_(Contact.mail==mail, Contact.phone==phone)).first()
        if (contact == None):
            contact = Contact(phone=phone, mail=mail, course_id=course_id)
            session.add(contact)
            session.commit()
            return True
        return False

    @staticmethod
    def delete_contact(phone, mail):
        contact = session.query(Contact).filter(or_(Contact.mail==mail, Contact.phone==phone)).first()
        if (contact == None):
            return False
        session.delete(contact)
        session.commit()
        return True

    

    # endregion

    # region Работа с классом Course
    @staticmethod
    def get_courses() -> List[Course]:
        """Возвращает список курсов из базы данных"""
        courses = session.query(Course).all()
        return [course for course in courses if course.is_delete == False]

    @staticmethod
    def get_course(id: int) -> Course:
        """Возвращает объект курса по ID"""
        return session.query(Course).filter_by(id=id).first()

    @staticmethod
    def create_new_course(data: Dict):
        """Добавляет новый курс в базу данных"""
        channels = []
        for ch in data['channels']:
            channel = session.query(Channel).filter_by(
                id=int(ch['id'])).first()
            if channel == None:
                channel = Channel(id=int(ch['id']), name=ch['name'])
                print(channel.id)
                session.add(channel)
            channels.append(channel)

        course = Course(name=data['name_course'], cost=data['cost_course'],
                        time=data['time_course'], description=data['description_course'])

        session.add(course)
        session.commit()

        for ch in channels:
            ch_in_course = ChannelsInCourse(
                course_id=course.id, channel_id=int(ch.id))
            session.add(ch_in_course)

        session.commit()

    @staticmethod
    def add_channel_in_course(message, data):
        """Добавляет канал в курс"""
        ch = {}
        if (message.forward_from_chat != None):
            id_channel = message.forward_from_chat.id
            full_name_channel = message.forward_from_chat.full_name
            ch = {"id": id_channel, "name": full_name_channel}

        else:
            try:
                mas_text = message.text.split(':')
                ch = {"id": mas_text[0], "name": mas_text[1]}
            except:
                pass

        course = DataBaseFunc.get_course(data['id_course'])

        channel = session.query(Channel).filter_by(id=int(ch['id'])).first()
        if channel == None:
            channel = Channel(id=int(ch['id']), name=ch['name'])
            session.add(channel)

        ch_in_course = ChannelsInCourse(
            course_id=course.id, channel_id=int(channel.id))
        session.add(ch_in_course)
        session.commit()

    @staticmethod
    def delete_channel_in_courses(id):
        ch_in_course = session.query(ChannelsInCourse).filter_by(id=id).first()
        session.delete(ch_in_course)
        session.commit()

    # endregion

    # region Работа с классом User

    @staticmethod
    def get_user(param) -> User:
        """Возвращает объект User из базы данных 
        Параметры: 
            id - telegram id пользователя
        Возвращает:
            user - объект пользователя из базы данных"""
        if isinstance(param, int):
            return session.query(User).filter_by(id=param).first()
        elif isinstance(param, str):
            return session.query(User).filter_by(username=param).first()
        else:
            return None

    @staticmethod
    def get_user_for_phone(phone) -> User:
        return session.query(User).filter_by(phone=phone).first()

    @staticmethod
    def get_user_for_mail(mail) -> User:
        return session.query(User).filter_by(mail=mail).first()

    def get_contact(phone=None, mail=None):
        if phone != None:
            return session.query(Contact).filter_by(phone=phone).first()
        if mail != None:
            return session.query(Contact).filter_by(mail=mail).first()
        return None

    @staticmethod
    def get_all_admins():
        return session.query(User).filter_by(is_admin=True).all()

    @staticmethod
    def get_users_with_subscribe():
        return session.query(User).all()

    # endregion

    # region Работа с классом Chanell
    @staticmethod
    def get_channel(id) -> Channel:
        return session.query(Channel).filter_by(id=id).first()

    @staticmethod
    def create_channel(id, name):
        channel = Channel(id=id, name=name)
        session.add(channel)
        session.commit()

    @staticmethod
    async def create_link_invoice(channel):
        id = channel.id
        link = await bot.export_chat_invite_link(id)
        channel.link = link
        session.commit()

    # endregion

    # region Работа по учету Курсов, Истории платежей и другие методы связанные с приобретением курса пользователем

    @staticmethod
    def add_course_in_user(user: User, course: Course):
        """Метод добавляет оплаченный курс конкретному пользователю. """
        date = datetime.now()
        purch = PurchasedSubscription(user_id=user.id, course_id=course.id,
                                      data_start=date, data_end=date + timedelta(days=float(course.time)))
        user.is_have_subscription = True
        user.course_id = course.id
        session.add(purch)
        session.commit()

    @staticmethod
    def add_course_in_user_test(user: User, course: Course):
        """Метод добавляет оплаченный курс конкретному пользователю. """
        date = datetime.now()
        purch = PurchasedSubscription(user_id=user.id, course_id=course.id,
                                      data_start=date, data_end=date + timedelta(minutes=5))
        user.is_have_subscription = True
        session.add(purch)
        session.commit()

    @staticmethod
    async def delete_course_from_user(user: User, course: Course):
        """Удаляет курс у пользователя"""
        date = datetime.now()
        purch = [ph for ph in user.purchased_subscriptions if (
            ph.courses.id == course.id) and (ph.data_end > date)]
        if len(purch) != 0:
            purch[-1].data_end = date
            session.commit()

        DataBaseFunc.delete_user_in_channels_from_course(user, course)

        actualy_subs = [
            ph for ph in user.purchased_subscriptions if ph.data_end > datetime.now()]

        if (len(actualy_subs) == 0):
            user.is_have_subscription = False
            user.subscribe_end = True
            DataBaseFunc.commit()

    @staticmethod
    def add_time_in_course(user: User, course: Course, time: int) -> None:
        """Добавляет время в курс пользователю

        Args:
            user (User): [Пользователь, которому нужно добавить время]
            course (Course): [Подписка, в которую нужно добавить время]
            time (int): [Время в днях]
        """
        date = datetime.now()
        purch = [ph for ph in user.purchased_subscriptions if (
            ph.courses.id == course.id) and (ph.data_end > date)]
        if len(purch) != 0:
            purch[-1].data_end += timedelta(days=time)
            session.commit()


    @staticmethod
    async def delete_user_in_channels_from_course(user : User, course : Course):
        for channel in course.channels:
            try:
                if (await bot.get_chat_member(channel.channels.id, user.id)):
                    await bot.kick_chat_member(channel.channels.id, user.id)
                    await bot.unban_chat_member(channel.channels.id, bot.id)
            except:
                pass

    @staticmethod
    async def delete_time_in_course(user: User, course: Course, time: int) -> None:
        """Убавляет время в курсе пользователю

        Args:
            user (User): [Пользователь, которому нужно убавить время]
            course (Course): [Подписка, в которую нужно убавить время]
            time (int): [Время в днях]
        """
        date = datetime.now()
        purch = [ph for ph in user.purchased_subscriptions if (
            ph.courses.id == course.id) and (ph.data_end > date)]
        if len(purch) != 0:
            purch[-1].data_end -= timedelta(days=time)
            if (purch[-1].data_end < datetime.now()):
                await DataBaseFunc.delete_user_in_channels_from_course(user, course)
            session.commit()
            activs = DataBaseFunc.get_user_subscribes(user)
            if (len(activs) == 0):
                user.is_have_subscription = False
                user.subscribe_end = True
                session.commit()



    @staticmethod
    def get_current_subscribe(user: User) -> PurchasedSubscription:
        """Метод возвращает текущую активную подписку пользователя."""
        purhs = session.query(PurchasedSubscription).filter_by(
            user_id=user.id).all()
        if (len(purhs) == 0):
            return None
        purh = purhs[-1]
        if purh.data_end > datetime.now():
            return purh
        return None

    @staticmethod
    def get_user_subscribes(user: User) -> PurchasedSubscription:
        """ Метод возвращает все активные подписки пользователя"""
        purhs = session.query(PurchasedSubscription).filter_by(
            user_id=user.id).all()
        return [pr for pr in purhs if pr.data_end > datetime.now()]

    # endregion

    # region Базовые методы для базы данных

    @staticmethod
    def commit() -> None:
        """Сохраняет изменения в бд """
        session.commit()

    @staticmethod
    def add(obj=None) -> None:
        """Добавляет объект в базу данных"""
        if obj:
            session.add(obj)
            session.commit()
    # endregion

    @staticmethod
    def drop_all():
        metadata.drop_all(bind=engine)
        metadata.create_all(bind=engine)
