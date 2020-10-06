from aiogram.dispatcher.filters.state import State, StatesGroup

class UserStateMainMenu(StatesGroup):
    chooselng = State()
    main_menu = State()
    get_subscribe = State()

class UserStateProfile(StatesGroup):
    menu_profile = State()
    choose_language = State()
    history = State()

class UserStateGetAccessCourse(StatesGroup):
    choose_course = State()
    choose_channels = State()

class UserStateRegister(StatesGroup):
    main_menu = State()
    write_phone = State()
    write_mail = State()