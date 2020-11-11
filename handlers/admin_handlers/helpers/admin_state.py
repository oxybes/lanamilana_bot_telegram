from aiogram.dispatcher.filters.state import State, StatesGroup

class AdminStateMainMenu(StatesGroup):
    admin_menu = State()
    managing_courses = State()
    whos = State()
    write_new_shedule = State()

class AdminStateManagingCourses(StatesGroup):
    add_course = State()
    write_description = State()
    write_cost = State()
    write_time = State()
    add_channels = State()
    confirm = State()

class AdminStateManaginCourseEdit(StatesGroup):
    get_course = State()
    choose_edit = State()
    edit_name = State()
    edit_description = State()
    edit_cost = State()
    edit_time = State()
    edit_access_add = State()
    edit_access_delete = State()

class AdminStateManaginCourseDelete(StatesGroup):
    get_course = State()

class AdminStateManagingUser(StatesGroup):
    main_menu = State()
    add_course = State()
    add_course_choouse_user = State()
    add_course_choouse_user_final = State()
    delete_course = State()
    delete_course_choouse_user = State()
    delete_course_final = State()
    add_time_choose_user = State()
    add_time_choose_course = State()
    add_time_write_time = State()
    add_time_final = State()
    delete_time_choose_user = State()
    delete_time_choose_course = State()
    delete_time_write_time = State()
    delete_time_final = State()

class AdminStateManagingAdmin(StatesGroup):
    main_menu = State()
    add_admin = State()
    add_admin_final = State()
    delete_admin = State()
    delete_admin_final = State()