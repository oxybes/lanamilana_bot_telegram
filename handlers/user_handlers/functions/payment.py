import datetime
from database.function import DataBaseFunc
from database.models import User
from misc import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from config import get_text, TEXTS, TOKEN_SHOP_YANDEX
from handlers.user_handlers.helpers.generator_keyboards import UserGeneratorKeyboard
from handlers.user_handlers.helpers.help import UserHelp
from handlers.user_handlers.helpers.user_state import UserStateMainMenu

def save_timestamp_in_user(user:User, timestamp:float) -> None:
    """Сохраняет время последнего платежа юзера для идентификации инвойса"""
    user.last_payload_timestamp = timestamp
    DataBaseFunc.commit()


def get_timestamp(user: User) -> float:
    timestamp = datetime.datetime.now().timestamp()
    save_timestamp_in_user(user, timestamp)
    return timestamp


@dp.callback_query_handler(state=UserStateMainMenu.get_subscribe)
async def subscribe_menu_choose_course(callback:types.CallbackQuery, state: FSMContext):
    """Отправляет чек для оплаты выбраноого курса"""
    user = DataBaseFunc.get_user(callback.from_user.id)

    if (TOKEN_SHOP_YANDEX.split(':')[1] == "TEST"):
        await callback.message.edit_text(text=get_text(user, 'subscribe_menu_test_payments'))
    
    course = DataBaseFunc.get_course(int(callback.data[20:]))
    timestamp = get_timestamp(user)

    PRICE = types.LabeledPrice(label=course.name, amount=int(f"{course.cost}00"))

    await state.update_data(last_course_id=int(callback.data[20:]))

    await bot.send_invoice(
        callback.message.chat.id,
        title = course.name,
        description= course.description,
        provider_token = TOKEN_SHOP_YANDEX,
        currency = "rub",
        is_flexible=False,
        prices = [PRICE],
        start_parameter = f"course_id_{course.id}",
        payload = timestamp,
        # reply_markup=UserGeneratorKeyboard.course_back_in_list(user)
        # start_parameter = f"lol-lel-cheburek",
        # payload = "test-payload-check"
    )


@dp.pre_checkout_query_handler(state='*')
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)



@dp.message_handler(state = '*', content_types=types.ContentTypes.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message, state:FSMContext):
    user = DataBaseFunc.get_user(message.from_user.id)

    data = await state.get_data()
    course = DataBaseFunc.get_course(data['last_course_id'])
    DataBaseFunc.add_course_in_user(user, course)
    user.subscribe_end = False
    DataBaseFunc.commit()
    await bot.send_message(
        message.chat.id,
        str(get_text(user, 'subscribe_menu_good_pay')).format(amount=course.cost,currency=message.successful_payment.currency, coursename=course.name))
    await bot.send_message(message.chat.id, get_text(user, 'start'), reply_markup=UserGeneratorKeyboard.start_button(user))
    await UserStateMainMenu.main_menu.set()

    
@dp.callback_query_handler(lambda callback: callback.data == "subscribe_continue_pay",state = '*')
async def subscribe_continue_pay(callback : types.CallbackQuery, state : FSMContext):
    """Продлить подписку после её окончания"""
    await callback.answer()
    user = DataBaseFunc.get_user(callback.from_user.id)
    if (TOKEN_SHOP_YANDEX.split(':')[1] == "TEST"):
        await callback.message.edit_text(text=get_text(user, 'subscribe_menu_test_payments'))
    
    course = DataBaseFunc.get_course(user.course_id)
    timestamp = get_timestamp(user)

    PRICE = types.LabeledPrice(label=course.name, amount=int(f"{course.cost}00"))

    await state.update_data(last_course_id=user.course_id)

    await bot.send_invoice(
        callback.message.chat.id,
        title = course.name,
        description= course.description,
        provider_token = TOKEN_SHOP_YANDEX,
        currency = "rub",
        is_flexible=False,
        prices = [PRICE],
        start_parameter = f"course_id_{course.id}",
        payload = timestamp,
        # reply_markup=UserGeneratorKeyboard.course_back_in_list(user)
        # start_parameter = f"lol-lel-cheburek",
        # payload = "test-payload-check"
    )

