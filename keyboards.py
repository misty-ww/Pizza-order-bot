from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

start_order = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🍕 Заказать пиццу",callback_data="start_order")],
            [InlineKeyboardButton(text="👀 Посмотреть заказ",callback_data="show_me_order")],
            [InlineKeyboardButton(text="😑 Нажми, если передумал",callback_data="cencel")]
        ]
)
start_order_call = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🍕 Заказать пиццу",callback_data="start_order")],
            [InlineKeyboardButton(text="📸 Оставить отзыв",callback_data="callback_ot")],
            [InlineKeyboardButton(text="😑 Нажми, если передумал",callback_data="cencel")]
        ]
)

admin_panel = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👀 Посмотрим все заказы)",callback_data="check_orders")],
            [InlineKeyboardButton(text="🔍 Проверим все пиццы",callback_data="check_pizzas")],
            [InlineKeyboardButton(text="🍕 Добавим пиццу?",callback_data="add_pizza"),
            InlineKeyboardButton(text="😢 Удалим пиццу?(",callback_data="delete_pizza")],
            [InlineKeyboardButton(text="📊 Статистика",callback_data="stat_admin")],
            [InlineKeyboardButton(text="💌 Какие промо существуют",callback_data="check_promo")],
            [InlineKeyboardButton(text="💸 Создать промокод",callback_data="add_promo"),
            InlineKeyboardButton(text="💥 Удалить промокод",callback_data="delete_promo")],
            [InlineKeyboardButton(text="💌 Посмотреть отзывы",callback_data="check_callback")],
            [InlineKeyboardButton(text="😑 Нажми, если передумал",callback_data="cencel")]
        ]
)
back_to_admin = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🍕 Обратно в AdminPanel?",callback_data="back_to_admin")],
            [InlineKeyboardButton(text="👀 Посмотрим все заказы)",callback_data="check_orders")],
            [InlineKeyboardButton(text="😑 Нажми, если передумал",callback_data="cencel")]
        ]
)
check_callback = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🍕 в AdminPanel?",callback_data="back_to_admin")],
            [InlineKeyboardButton(text="💌 Посмотреть отзывы",callback_data="check_callback")]
        ]
)
orders_all = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🍕 Обратно в AdminPanel?",callback_data="back_to_admin")],
            [InlineKeyboardButton(text="🆕 Новые",callback_data="new")],
            [InlineKeyboardButton(text="🧑‍🍳 Готовятся",callback_data="cooking"),
             InlineKeyboardButton(text="🍽 Готовые",callback_data="ready")],
            [InlineKeyboardButton(text="🚚 В доставке",callback_data="inRoad"),
             InlineKeyboardButton(text="✅ Доставленные сегодня",callback_data="deliver")],
            [InlineKeyboardButton(text="🫦 Доставленные все",callback_data="deliver_all")],
            [InlineKeyboardButton(text="😑 Нажми, если передумал",callback_data="cencel")]
        ]
)
change_status = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🆕 Новый",callback_data="new_status")],
            [InlineKeyboardButton(text="🧑‍🍳 Готовится",callback_data="cooking_status"),
             InlineKeyboardButton(text="🍽 Готовый",callback_data="ready_status")],
            [InlineKeyboardButton(text="🚚 В доставке",callback_data="inRoad_status"),
             InlineKeyboardButton(text="✅ Доставлен",callback_data="deliver_status")],
            [InlineKeyboardButton(text="😑 Нажми, если передумал",callback_data="cencel_status")]
        ]
)
back_to_admin_orders = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🍕 Обратно в AdminPanel?",callback_data="back_to_admin")],
            [InlineKeyboardButton(text="😑 Нажми, если передумал",callback_data="cencel")]
        ]
)
isPromo = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Ввести промокод",callback_data="yesPromo")],
            [InlineKeyboardButton(text="➡️ Продолжить",callback_data="notPromo")],
            [InlineKeyboardButton(text="😑 Отменить заказ",callback_data="cencel")]
        ]
)
Promo = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➡️ Продолжить без промокода",callback_data="notPromo")],
            [InlineKeyboardButton(text="😑 Отменить заказ",callback_data="cencel")]
        ]
)
pay = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💲 Криптовалюта",callback_data="crypt")],
            [InlineKeyboardButton(text="💳 Перевод",callback_data="pay_num")],
            [InlineKeyboardButton(text="💵 При получении (Нал/безнал)",callback_data="link_pay")],
            [InlineKeyboardButton(text="😑 Отменить заказ",callback_data="cencel")]
        ]
)
isNumber = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Верно",callback_data="yesNumber")],
            [InlineKeyboardButton(text="📛 Изменить номер",callback_data="notNumber")],
            [InlineKeyboardButton(text="😑 Отменить заказ",callback_data="cencel")]
        ]
)
isAddres = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Верно",callback_data="yesAddres")],
            [InlineKeyboardButton(text="📛 Изменить адрес",callback_data="notAddres")],
            [InlineKeyboardButton(text="😑 Отменить заказ",callback_data="cencel")]
        ]
)
back_to_admin_delete = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="😢 Удалим еще 1 пиццу?",callback_data="delete_pizza")],
            [InlineKeyboardButton(text="🍕 Обратно в AdminPanel?",callback_data="back_to_admin")],
            [InlineKeyboardButton(text="😑 Нажми, если передумал",callback_data="cencel")]
        ]
)
back_to_admin_delete_promo = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="😢 Удалим еще 1 промокод?",callback_data="delete_promo")],
            [InlineKeyboardButton(text="🍕 Обратно в AdminPanel?",callback_data="back_to_admin")],
            [InlineKeyboardButton(text="😑 Нажми, если передумал",callback_data="cencel")]
        ]
)
back_to_admin_promo = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💸 Создадим еще 1 промокод?",callback_data="add_promo")],
            [InlineKeyboardButton(text="🍕 Обратно в AdminPanel?",callback_data="back_to_admin")],
            [InlineKeyboardButton(text="😑 Нажми, если передумал",callback_data="cencel")]
        ]
)
cencel = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="😑 Нажми, если передумал",callback_data="cencel")]
        ]
)
cencel_or = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="😑 Отменить заказ",callback_data="cencel")]
        ]
)


quantity_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1")],
            [KeyboardButton(text="2")],
            [KeyboardButton(text="3")],
            [KeyboardButton(text="4")],
            [KeyboardButton(text="5")],
            [KeyboardButton(text="😣 Отмена заказа")]
        ], resize_keyboard=True
    )