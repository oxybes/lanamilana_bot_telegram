from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TEXTS, get_text_but
from database.models import User, Course
from database.function import DataBaseFunc

class AdminGenerateKeyboard():
    """Класс отвечает за генерацию клавиатуры для администрации"""

    @staticmethod
    def admin_main_menu(user : User) -> InlineKeyboardMarkup:
        """Клавиатура главного меню админ панели."""
        keyboard = InlineKeyboardMarkup(row_width=2)
        ls_dict_buttons = get_text_but(user,'main_admin_menu')
        butt_managing_courses = InlineKeyboardButton(text=ls_dict_buttons['managing_courses'], callback_data='admin_menu_managing_courses')
        butt_managing_users = InlineKeyboardButton(ls_dict_buttons['managing_users'], callback_data='admin_menu_managing_users')
        butt_managing_admins = InlineKeyboardButton(ls_dict_buttons['managing_admins'], callback_data='admin_menu_managing_admins')
        butt_who_used = InlineKeyboardButton(ls_dict_buttons['whos'], callback_data='admin_menu_whos')
        # butt_generate_new_link = InlineKeyboardButton(ls_dict_buttons['generate_new_link'], callback_data='admin_menu_generate_new_link')
        # butt_spam = InlineKeyboardButton(ls_dict_buttons['spam'], callback_data='admin_menu_spam')
        butt_back = InlineKeyboardButton(ls_dict_buttons['back'], callback_data='admin_menu_back')

        keyboard.row(butt_managing_courses, butt_managing_users)
        keyboard.add(butt_managing_admins)
        # keyboard.add(butt_spam)
        # keyboard.add(butt_generate_new_link)
        keyboard.add(butt_back)
        return keyboard

    @staticmethod
    def admin_menu_managing_courses(user : User) -> InlineKeyboardMarkup():
        """Клавиатура для управления подписками"""
        keyboard = InlineKeyboardMarkup()
        dict_buttons = get_text_but(user, 'admin_menu_managing_courses')
        # butt_add = InlineKeyboardButton(dict_buttons['add'], callback_data='managing_courses_add')
        butt_edit = InlineKeyboardButton(dict_buttons['edit'], callback_data='managing_courses_edit')
        # butt_delete = InlineKeyboardButton(dict_buttons['delete'], callback_data='managing_courses_delete')
        butt_back = InlineKeyboardButton(get_text_but(user,'in_admin_menu'), callback_data='admin_in_admin_menu')
        # keyboard.add(butt_add, butt_edit, butt_delete, butt_back)
        keyboard.add(butt_edit, butt_back)
        return keyboard


    @staticmethod
    def managing_courses_add_channels_continue(user:User) -> InlineKeyboardMarkup():
        """Кнопка продолжить при пересылке канналов и чатов при их добавлении"""
        keyboard = InlineKeyboardMarkup()
        butt = InlineKeyboardButton(get_text_but(user, 'managing_courses_add_continue'), callback_data='managing_courses_add_continue')
        keyboard.add(butt)
        return keyboard

    @staticmethod
    def managing_courses_additionaly(user:User) -> InlineKeyboardMarkup():
        """Клавиатура для подтверждния или отмены созданного курса"""
        keyboard = InlineKeyboardMarkup()
        butt_complete = InlineKeyboardButton(get_text_but(user, 'managing_courses_add_additionaly_complete'), callback_data="managing_courses_add_additionaly_complete")
        butt_cancel = InlineKeyboardButton(get_text_but(user, 'managing_courses_add_additionaly_cancel'), callback_data="managing_courses_add_additionaly_cancel")
        keyboard.row(butt_complete, butt_cancel)
        return keyboard


    #region Клавиатуры для редактирования курсов
    @staticmethod
    def managing_courses_edit(user : User) -> InlineKeyboardMarkup():
        """Отправляет кнопки с выбором курса для редактирования"""
        keyboard = InlineKeyboardMarkup(row_width=2)
        courses = DataBaseFunc.get_courses()
        buttons = []
        for course in courses:
            buttons.append(InlineKeyboardButton(course.name, callback_data=f"managing_course_edit_{course.id}"))
        keyboard.add(*buttons)
        keyboard.add(InlineKeyboardButton(text=get_text_but(user, 'managing_course_edit_back'), callback_data="managing_course_edit_back"))
        return keyboard


    @staticmethod
    def managing_courses_delete(user) -> InlineKeyboardMarkup():
        """Обработка кнопки удалить курс"""
        keyboard = InlineKeyboardMarkup(row_width=2)
        courses = DataBaseFunc.get_courses()
        buttons = []
        for course in courses:
            buttons.append(InlineKeyboardButton(course.name, callback_data=f"managing_course_delete_{course.id}"))
        keyboard.add(*buttons)
        keyboard.add(InlineKeyboardButton(text=get_text_but(user,'managing_course_delete_back'), callback_data="managing_course_delete_back"))
        return keyboard

    @staticmethod
    def managing_courses_edit_button(user : User) -> InlineKeyboardMarkup():
        """Отправляет кнопки с выбором что отредактировать в боте"""
        keyboard = InlineKeyboardMarkup(row_width=2)
        data_text = get_text_but(user,"managing_courses_edit_buttons")
        name = InlineKeyboardButton(data_text['name'], callback_data="managing_courses_edit_name")
        descripiton = InlineKeyboardButton(data_text['description'], callback_data="managing_courses_edit_description")
        cost = InlineKeyboardButton(data_text['cost'], callback_data="managing_courses_edit_cost")
        time = InlineKeyboardButton(data_text['time'], callback_data="managing_courses_edit_time")
        access_add = InlineKeyboardButton(data_text['access_add'], callback_data="managing_courses_edit_access_add")
        access_delete = InlineKeyboardButton(data_text['access_delete'], callback_data="managing_courses_edit_access_delete")
        back = InlineKeyboardButton(data_text["back"], callback_data="managing_courses_edit_back")
        keyboard.add(name, descripiton, cost, time, access_add, access_delete, back)
        return keyboard

    #endregion


    #region Клавиатуры для управления пользователя
    @staticmethod
    def admin_menu_managing_users(user : User) -> InlineKeyboardMarkup():
        """Генерирует клавиатуру для управления пользователями"""
        keyboard = InlineKeyboardMarkup(row_width=2)
        data = get_text_but(user, 'managing_users_main_menu')
        add_course = InlineKeyboardButton(data['add_course'], callback_data="managing_users_main_menu_add_course")
        delete_course = InlineKeyboardButton(data['delete_course'], callback_data="managing_users_main_menu_delete_course")
        add_time = InlineKeyboardButton(data['add_time'], callback_data="managing_users_main_menu_add_time")
        delete_time = InlineKeyboardButton(data['delete_time'], callback_data="managing_users_main_menu_delete_time")
        keyboard.add(add_course, delete_course, add_time, delete_time)
        back = InlineKeyboardButton(data['back'], callback_data='managing_users_main_menu_back')
        keyboard.add(back)
        return keyboard

    @staticmethod
    def managing_user_add_course(user : User, user_add_course : User) -> InlineKeyboardMarkup():
        """ Генерирует клавиатуру с выбором курсов для добавления пользователю"""
        keyboard = InlineKeyboardMarkup(row_width=2)
        user_courses = DataBaseFunc.get_user_subscribes(user_add_course)

        courses = DataBaseFunc.get_courses()
        courses = [course for course in courses if ((course.id in [cs.courses.id for cs in user_courses]) == False)]

        buttons = []
        for course in courses:
            buttons.append(InlineKeyboardButton(course.name, callback_data=f"managing_users_add_course_{course.id}"))
        keyboard.add(*buttons)
        keyboard.add(InlineKeyboardButton(get_text_but(user, 'managing_users_add_course_back'), callback_data="managing_users_add_course_back"))
        return keyboard


    

    @staticmethod
    def admin_menu_managing_users_add_course(user : User) -> InlineKeyboardMarkup():
        """"Генерирует клавиатуру при выборе пользователя курса"""
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(get_text_but(user, 'admin_menu_managing_users_add_course_back'), callback_data='admin_menu_managing_users_add_course_back'))
        return keyboard

    @staticmethod
    def managing_users_main_menu_add_course_choose_user(user : User) -> InlineKeyboardMarkup():
        """Подтвердить или отменить добавление курса"""
        keyboard = InlineKeyboardMarkup()
        data = get_text_but(user, 'managing_users_main_menu_add_course_choose_user')
        add = InlineKeyboardButton(text = data['add'], callback_data='managing_users_main_menu_add_course_choose_user_add')
        cancel = InlineKeyboardButton(text = data['cancel'], callback_data='managing_users_main_menu_add_course_choose_user_cancel')
        keyboard.add(add, cancel)
        return keyboard

    @staticmethod
    def managing_users_main_menu_delete_course(user : User) -> InlineKeyboardMarkup():
        """Кнопка назад при выборе пользователя для удаления курса."""
        keyboard = InlineKeyboardMarkup()
        back = get_text_but(user, 'managing_users_main_menu_delete_course_back')
        keyboard.add(InlineKeyboardButton(back, callback_data="managing_users_main_menu_delete_course"))
        return keyboard

    @staticmethod
    def managin_users_main_menu_delete_course_choose_use(user : User) -> InlineKeyboardMarkup():
        """Возвращает доступные курсы для удаления"""
        keyboard = InlineKeyboardMarkup(row_width=2)
        buttons = []
        for ph in DataBaseFunc.get_user_subscribes(user):
            buttons.append(InlineKeyboardButton(ph.courses.name, callback_data=f"managin_users_main_menu_delete_course_choose_use_{ph.courses.id}"))
        keyboard.add(*buttons)
        keyboard.add(InlineKeyboardButton(get_text_but(user, 'managin_users_main_menu_delete_course_choose_use_back'), callback_data="managin_users_main_menu_delete_course_choose_use_back"))
        return keyboard

    @staticmethod
    def managing_users_delete_course_final(user : User) -> InlineKeyboardMarkup():
        """Возвращает клавиатуру для подтверждения или отмены удаления курса у пользователя"""
        keyboard = InlineKeyboardMarkup(row_width=2)
        successfull = InlineKeyboardButton(get_text_but(user, 'managing_users_delete_course_final_add'), callback_data="managing_users_delete_course_final_add")
        cancel = InlineKeyboardButton(get_text_but(user, 'managing_users_delete_course_final_cancel'), callback_data="managing_users_delete_course_final_cancel")
        keyboard.add(successfull, cancel)
        return keyboard

    @staticmethod
    def managign_users_add_time(user : User) -> InlineKeyboardMarkup():
        """Кнопка назад для первого этапа добавления времени подписки"""
        keyboard = InlineKeyboardMarkup()
        back = InlineKeyboardButton(get_text_but(user, 'managign_users_add_time_back'), callback_data="managign_users_add_time_back")
        keyboard.add(back)
        return keyboard

    @staticmethod
    def admin_menu_managing_users_add_time_choose_user_back(user : User) -> InlineKeyboardMarkup():
        keyboard = InlineKeyboardMarkup()
        back = InlineKeyboardButton(get_text_but(user, 'managign_users_add_time_back'), callback_data="admin_menu_managing_users_add_time_choose_user_back")
        keyboard.add(back)
        return keyboard

    @staticmethod
    def managing_users_add_time_choose_course(user : User) -> InlineKeyboardMarkup():
        """Возвращает кнопки с активными подписками пользователя"""
        keyboard = InlineKeyboardMarkup(row_width=2)
        buttons = []
        for ph in DataBaseFunc.get_user_subscribes(user):
            buttons.append(InlineKeyboardButton(ph.courses.name, callback_data=f"managing_users_add_time_choose_course_{ph.courses.id}"))
        keyboard.add(*buttons)
        keyboard.add(InlineKeyboardButton(get_text_but(user, 'managing_users_add_time_choose_course_back'), callback_data="managing_users_add_time_choose_course_back"))
        return keyboard

    @staticmethod
    def managing_users_add_time_choose_time(user : User) -> InlineKeyboardMarkup():
        keyboard = InlineKeyboardMarkup()
        back = InlineKeyboardButton(get_text_but(user, 'managing_users_add_time_choose_time_back'), callback_data="managing_users_add_time_choose_time_back")
        keyboard.add(back)
        return keyboard

    @staticmethod
    def managing_users_add_time_final(user : User) -> InlineKeyboardMarkup():
        """Подтверждение добавления времени"""
        keyboard = InlineKeyboardMarkup()
        add = InlineKeyboardButton(get_text_but(user, 'managing_users_add_time_final_add'), callback_data="managing_users_add_time_final_add")
        cancel = InlineKeyboardButton(get_text_but(user, 'managing_users_add_time_final_cancel'), callback_data="managing_users_add_time_final_cancel")
        keyboard.add(add, cancel)
        return keyboard
    #endregion


    #region Клавиатуры для управления администрацией
    @staticmethod
    def admin_menu_managing_admins(user : User) -> InlineKeyboardMarkup():
        """Отправляет меню управления администрацией"""
        keyboard = InlineKeyboardMarkup(row_width=2)
        data = get_text_but(user, 'admin_menu_managing_admins')
        list_admins = InlineKeyboardButton(data['list_admins'], callback_data="managing_admins_main_menu_list_admins")
        add_admin = InlineKeyboardButton(data['add_admin'], callback_data="managing_admins_main_menu_add_admin")
        delete_admin = InlineKeyboardButton(data['delete_admin'], callback_data="managing_admins_main_menu_delete_admin")
        back = InlineKeyboardButton(data['back'], callback_data="managing_admins_main_menu_back")
        keyboard.add(list_admins),
        keyboard.add(add_admin, delete_admin)
        keyboard.add(back)
        return keyboard

    @staticmethod
    def managing_admin_list_admins(user : User):
        """Кнопка назад после списка админов"""
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(get_text_but(user, 'managing_admin_list_admins_back'), callback_data="managing_admin_list_admins_back"))
        return keyboard


    @staticmethod
    def managing_admins_main_menu_add_admin(user : User):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(get_text_but(user,'managing_admins_main_menu_add_admin_back'), callback_data="managing_admins_main_menu_add_admin_back"))
        return keyboard

    @staticmethod
    def managing_admins_main_menu_delete_admin(user : User):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(get_text_but(user,'managing_admins_main_menu_add_admin_back'), callback_data="managing_admins_main_menu_delete_admin_back"))
        return keyboard
    #endregion