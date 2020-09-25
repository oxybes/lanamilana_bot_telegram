from .models import User, Course
from config import MAIN_ADMIN_ID
from .mics import session
from aiogram import types
from typing import List

class DataBaseFunc():
    """Класс для работы с базой данных.
       Содержит в себе функции по управлению БД"""

    @staticmethod
    def add_main_admin() -> None:
        """Добавляет главного администратора при инициализации базы данных"""
        user = session.query(User).filter_by(id=MAIN_ADMIN_ID).first()
        if user == None:
            user = User(id=MAIN_ADMIN_ID, username="oxybes", is_admin = True, is_main_admin = True, lng='rus')
            session.add(user)
            session.commit()

    @staticmethod
    def initial_course_in_db() -> None:
        """Добавляет в базу данных тарифы"""
        courses = session.query(Course).all()
        if (len(courses) != 0):
            return
        
        course = Course(name = "Базовый", cost = 990, time = 21)
        session.add(course)
        
        course = Course(name = "Всё, что нужно", cost = 2990, time = 62)
        session.add(course)

        course = Course(name = "Индивидуальный", cost = 19000, time = 181)
        session.add(course)
        session.commit()

    #region Работа с классом Course
    @staticmethod
    def get_courses() -> List[Course]:
        """Возвращает список курсов из базы данных"""
        courses = session.query(Course).all()
        return courses
    #endregion

    #region Работа с классом User
    @staticmethod
    def get_user(id: int) -> User:
        """Возвращает объект User из базы данных 
        Параметры: 
            id - telegram id пользователя
        Возвращает:
            user - объект пользователя из базы данных"""
        return session.query(User).filter_by(id=id).first()
    #endregion

    #region Базовые методы для базы данных
    @staticmethod
    def commit() -> None:
        """Сохраняет изменения в бд """
        session.commit()

    @staticmethod
    def add(obj = None) -> None:
        """Добавляет объект в базу данных"""
        if obj:
            session.add(obj)
            session.commit()
    #endregion