from aiogram.dispatcher.filters.state import State, StatesGroup

class UserStateMainMenu(StatesGroup):
    chooselng = State()
    main_menu = State()
    get_subscribe = State()

class UserStateProfile(StatesGroup):
    menu_profile = State()
    choose_language = State()