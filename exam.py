import asyncio
import datetime
from aiogram import Bot, Dispatcher,types,F
from aiogram.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from func import *
import keyboards
import config


bot = Bot(token=config.token)
dp = Dispatcher()


class PizzaOrderForm(StatesGroup):
    waiting_pizza_size = State()
    waiting_pizza_type = State()
    waiting_quantity = State()
    waiting_address = State()
    waiting_phone = State()
    waiting_confirmation = State()

    waiting_password_admin = State()

    waiting_name_pizza_adm = State()
    waiting_photo_pizza_adm= State()
    waiting_sort_pizza_adm= State()
    waiting_price_pizza_adm= State()
    waiting_id_delete_pizza = State()

    waiting_name_promo = State()
    waiting_sale_promo = State()

    waiting_id_delete_promo = State()

    waiting_id_for_sell = State()
    waiting_size_for_sell = State()
    waiting_num_for_sele = State()
    waiting_addres_for_sele = State()
    waiting_number_for_sele = State()
    waiting_promo_isTrue = State()

    waiting_id_new = State()
    waiting_id_cooking = State()
    waiting_id_ready = State()
    waiting_id_inRoad = State()
    waiting_id_deliver = State()
    
    waiting_callback = State()


@dp.message(Command("command"))
async def command(message:types.Message):
    await message.answer("""
⁉️ <b>Команды:</b>
<i>/start - начать заказ,посмотреть заказ</i>
                         
<i>/info - информация о пиццерии и боте</i>
                         
<i>/command - посмотреть команды</i>
""",
parse_mode='HTML')
    
@dp.message(Command("info"))
async def command(message:types.Message):
    await message.answer("""
🍕 <i>Пиццерия - </i><b>misty</b>                       

<i>-- Информация  о пиццерии --</i>
                         
✨<i>Bot created by @qARHANGEL</i>
""",
parse_mode='HTML')

#ОБРАБОТКА /start ПРИЕМ ПОЛЬЗОВАТЕЛЕЙ
@dp.message(Command("start"))
async def st(message:types.Message,state:FSMContext):
    await state.clear()
    await asyncio.to_thread(new_user,message.from_user.id,message.from_user.first_name,message.from_user.username)
    await message.answer("👋 <i>Приветствую!</i>",
                         parse_mode='HTML',
                         reply_markup=keyboards.start_order)

async def cencel_f(callback:CallbackQuery,state:FSMContext):
    await state.clear()
    await callback.message.answer("<i>Все действия отменены\nНачать заказ /start\nПосмотреть команды /command</i>",
                                  parse_mode="HTML",
                                reply_markup=ReplyKeyboardRemove())
    await callback.answer()
async def cencel_f_m(message:types.Message,state:FSMContext):
    await state.clear()
    await message.answer("<i>Все действия отменены\nНачать заказ /start\nПосмотреть команды /command</i>",
                                  parse_mode="HTML",
                                reply_markup=ReplyKeyboardRemove())
#ОБРАБОТКА КНОПКИ ОТМЕНА cencel
@dp.callback_query(F.data == "cencel")
async def cencel(callback:CallbackQuery,state:FSMContext):
    await cencel_f(callback,state)


async def start_order_f(message:types.Message,state:FSMContext):
    await state.clear()
    try:
        await message.edit_text(text="😁 <i>Начали заказ)</i>",
                                     parse_mode='HTML',
                                     reply_markup=None)
    except:
        pass
    pizzas = await asyncio.to_thread(get_pizza)
    if not pizzas:
        await message.answer("❌ <i>Извините, произошла ошибка, попробуйте позже</i>",
                                      parse_mode='HTML')
        await state.clear()
        await cencel_f_m(message,state)
        return
    for pizza in pizzas:
        id,name,photo,sort,priceL,priceM,priceB,date = pizza
        await message.answer_photo(photo=photo,
                                            caption=f"""
🆔 <b>id:</b><code>{id}</code>. <b>{name}</b>

💸 <b>Цена L:</b> {priceL}
💸 <b>Цена M:</b> {priceM}
💸 <b>Цена B:</b> {priceB}

🧂 <i>Ингридиенты: {sort}</i>
""",
                                            parse_mode='HTML')
    mess = await message.answer("🆔 <i>Напиши id пиццы, которую хочешь заказать</i>\n<b>Далее разберемся с размером и количеством</b>",
                                  parse_mode='HTML',
                                  reply_markup=keyboards.cencel)
    await state.update_data(mess = mess.message_id)
    await state.set_state(PizzaOrderForm.waiting_id_for_sell)


#
@dp.callback_query(F.data == "callback_ot")
async def callback_ot_f(callback:CallbackQuery,state:FSMContext):
    data = await state.get_data()
    try:
        mess = data['mess']
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                            message_id=mess,
                                            reply_markup=None)
    except:
        pass
    user_id = callback.from_user.id
    await callback.message.answer("🥰 <i>Напишите свой отзыв следущим сообщением</i>",
                                  parse_mode='HTML',
                                  reply_markup=keyboards.cencel)
    await state.update_data(user_id = user_id)
    await state.set_state(PizzaOrderForm.waiting_callback)
@dp.message(PizzaOrderForm.waiting_callback)
async def waiting_callback_(message:types.Message,state:FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    text = message.text
    text_for_admin = f"""
💌 <b>Новый отзыв:</b>

<i>[{text}]</i>

🙋‍♂️ <b>От user_id:</b> {user_id}
"""
    isOk = await input_callback(user_id,text)
    if not isOk:
        await message.answer("❌ Произошла ошибка")
        return
    try:
        await bot.send_message(chat_id=config.admin,
                           text=text_for_admin,
                           parse_mode='HTML',
                           reply_markup=keyboards.check_callback)
        await message.answer("📩 <i>Ваш отзыв успешно отправлен</i>",
                             parse_mode='HTML',
                             reply_markup=keyboards.start_order)
    except:
        await message.answer("❌ Произошла ошибка")
    await state.clear()


#
@dp.callback_query(F.data == "check_callback")
async def check_callback_(callback:CallbackQuery,state:FSMContext):
    data = await state.get_data()
    try:
        mess = data['mess']
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                            message_id=mess,
                                            reply_markup=None)
    except:
        pass
    callbacks = await get_callback()
    if not callbacks:
        await callback.message.answer("😔 <i>Отзывов нет</i>",
                                      parse_mode='HTML',
                                      reply_markup=keyboards.back_to_admin_orders)
        await callback.answer()
        return
    text_mes = "📬 <b>Все отзывы:</b> \n"
    for i, call1 in enumerate(callbacks,1):
        id,user_id,text,date = call1
        text_mes += f"""
💌 {i}. <b>ID:</b> <code>{id}</code>

<i>[{text}]</i>

🙋‍♂️ <b>От user_ID:</b> <i>{user_id}</i>
⌛ <b>Дата создания:</b> <i>{date}</i>
----------------------------------
"""
    await callback.message.answer(text_mes,
                                  parse_mode='HTML',
                                  reply_markup=keyboards.back_to_admin_orders)
    await callback.answer()


#
@dp.callback_query(F.data == "show_me_order")
async def show_me_order_(callback:CallbackQuery,state:FSMContext):
    user_id = callback.from_user.id
    orders = await get_unDeliv_orders_user(user_id)
    if not orders:
        await callback.message.answer("<i>У вас нет заказов</i>",
                                      parse_mode='HTML')
        await callback.answer()
        return
    status_list = {
        "new": "🆕 Новый ",
        "cooking": "🧑‍🍳 Готовится ",
        "ready": "🍽 Готов ",
        "inRoad": "🚚 В дороге ",
        "deliver": "✅ Доставлен ",
    }
    text = "👀 <b>Ваши заказы: </b> \n"
    for i , order in enumerate(orders, 1):
        idOrder, size, name, num, address, phone, date, status = order
        status_text = status_list.get(status,"Не известный статус")
        text += f"""
📌 <b>Заказ:</b> {i}. <b>ID:</b> <code>{idOrder}</code>
🎲 <b>Статус:</b> <i>{status_text}</i>

🍕 <b>{name}</b>
📏 <b>Размер:</b> <i>{size}</i>
🔥 <b>Количество:</b> <i>{num}</i>

🏘 <b>Адрес:</b> <i>{address}</i>
📞 <b>Телефон:</b> <i>{phone}</i>
🙋‍♂️ <b>User ID:</b> <i>{user_id}</i>

📅 <b>Дата заказа:</b> <i>{date}</i>
----------------------------------
"""
    await callback.message.answer(text,
                                  parse_mode='HTML',
                                  reply_markup=keyboards.start_order)
    await state.clear()
    await callback.answer()

#ОБРАБОТКА КНОПКИ НАЧАТЬ ЗАКАЗ start_order
@dp.callback_query(F.data == "start_order")
async def start_order(callback:CallbackQuery,state:FSMContext):
    await state.clear()
    await callback.message.edit_text(text="😁 <i>Начали заказ)</i>",
                                     parse_mode='HTML',
                                     reply_markup=None)
    pizzas = await asyncio.to_thread(get_pizza)
    if not pizzas:
        await callback.message.answer("❗️ <i>Извините, произошла ошибка, попробуйте позже</i>",
                                      parse_mode='HTML')
        await state.clear()
        await cencel_f(callback,state)
        return
    for pizza in pizzas:
        id,name,photo,sort,priceL,priceM,priceB,date = pizza
        await callback.message.answer_photo(photo=photo,
                                            caption=f"""
🆔 <b>id:</b><code>{id}</code>. <b>{name}</b>

💸 <b>Цена L:</b> {priceL}
💸 <b>Цена M:</b> {priceM}
💸 <b>Цена B:</b> {priceB}

🧂 <i>Ингридиенты: {sort}</i>
""",
                                            parse_mode='HTML')
    mess = await callback.message.answer("🆔 <i>Напиши id пиццы, которую хочешь заказать</i>\n<b>Далее разберемся с размером и количеством</b>",
                                  parse_mode='HTML',
                                  reply_markup=keyboards.cencel)
    await state.update_data(mess = mess.message_id)
    await state.set_state(PizzaOrderForm.waiting_id_for_sell)
    await callback.answer()
@dp.message(PizzaOrderForm.waiting_id_for_sell)
async def id_for_sell(message:types.Message, state:FSMContext):
    try:
        id_p = int(message.text.strip())
        pizza = await asyncio.to_thread(get_pizza_1,id_p)
        print(pizza)
        if pizza is None:
            print("Я")
            await message.answer("❗️ <i>Вы ввели не существующий id пиццы</i>\nВведите еще раз",
                                 parse_mode='HTML',
                                 reply_markup=keyboards.cencel_or)
            return
    except Exception as e:
        print(f"ЯЯ, {e}")
        await message.answer("❗️ <i>Вы ввели не существующий id пиццы</i>\nВведите еще раз",
                                 parse_mode='HTML',
                                 reply_markup=keyboards.cencel_or)
        return
    await state.update_data(user_id = message.from_user.id)
    data = await state.get_data()
    mess = data['mess']
    await bot.edit_message_reply_markup(chat_id=message.chat.id,
                                        message_id=mess,
                                        reply_markup=None)
    id,name,photo,sort,priceL,priceM,priceB,date = pizza
    size_key = await asyncio.to_thread(make_keyboard,priceL,priceM,priceB)
    await message.answer_photo(photo=photo,
                                            caption=f"""
<b>{name}:</b>

<b>Цена L:</b> {priceL}
<b>Цена M:</b> {priceM}
<b>Цена B:</b> {priceB}

<i>Ингридиенты: {sort}</i>
""",
                                            parse_mode='HTML',
                                            reply_markup=size_key)
    await state.set_state(PizzaOrderForm.waiting_size_for_sell)
    await state.update_data(id = id,
                            name = name,
                            photo = photo,
                            sort =sort,
                            priceL = priceL,
                            priceM = priceM,
                            priceB = priceB,
                            date = date)
@dp.message(PizzaOrderForm.waiting_size_for_sell)
async def size_for_sell(message:types.Message, state:FSMContext):
    mt = message.text
    data = await state.get_data()
    if mt == "📌 Изменить пиццу":
        await state.clear()
        await message.answer("😅 <i>Хорошо, выбирай другую пиццу</i>",
                             parse_mode='HTML')
        await start_order_f(message,state)
        return
    if mt == "😣 Отмена заказа":
        await state.clear()
        await cencel_f_m(message,state)
        return
    mt = mt.split(" ")
    if len(mt) != 3 or mt[0] != "Size:" or (mt[1] not in ["L","M","B"]) or not mt[2].startswith("Цена:"):
        await message.answer("❗️❗️❗️ <i>Воспользуйтесь кнопками</i> ❗️❗️❗️",
                             parse_mode='HTML')
        return
    if mt[1] == "L":
        price = data['priceL']
        size = "L"
    if mt[1] == "M":
        price = data['priceM']
        size = "M"
    if mt[1] == "B":
        price = data['priceB']
        size = "B"
    mess = await message.answer("🎲 <i>Напишите количество пицц для заказа или воспользуйтесь кнопками</i>",
                         parse_mode='HTML',
                         reply_markup=keyboards.quantity_keyboard)
    await state.set_state(PizzaOrderForm.waiting_num_for_sele)
    await state.update_data(mess = mess.message_id,
                            price = price,
                            size = size)
@dp.message(PizzaOrderForm.waiting_num_for_sele)
async def num_for_sele(message:types.Message, state:FSMContext):
    mt = message.text
    data = await state.get_data()
    mess = data['mess']
    if mt == "😣 Отмена заказа":
        await state.clear()
        await cencel_f_m(message,state)
        return
    try:
        mt = int(message.text.strip())
        if mt > 15 or mt < 1:
            await message.answer("📌 <i>Можно заказать от 1 пиццы и до 15)</i> \n<b>Введи количесвто пицц для заказа повторно</b>",
                             parse_mode='HTML',
                             reply_markup=keyboards.cencel_or)
            return
    except:
        await message.answer("📌 <i>Можно заказать от 1 пиццы и до 15)</i> \n<b>Введи количесвто пицц для заказа повторно</b>",
                             parse_mode='HTML',
                             reply_markup=keyboards.cencel_or)
        return
    try:
        price = int(data['price'])
    except:
        await message.answer("❗️ <i>Произошла ошибка</i>",
                             parse_mode='HTML',
                             reply_markup=ReplyKeyboardRemove())
        return
    cost = mt * price
    await message.answer(
    "🎉 <i>Поздавляю!!!</i>",
    parse_mode='HTML',
    reply_markup=ReplyKeyboardRemove()
)
    mess = await message.answer(f"""
🛒 <b>ВАШ ЗАКАЗ:</b>
                                
🍕 <b>пицца:</b> <i>{data['name']}</i>
📌 <b>Размер:</b> <i>{data['size']}</i>
🔥 <b>Количество:</b> <i>{mt}</i>

💸 <b>К оплате:</b> <i>{cost} ₽</i>
""",
parse_mode='HTML',
reply_markup=keyboards.cencel)
    mess1 = await message.answer("🎁 <i>У вас есть промокод?</i>",
                         parse_mode='HTML',
                         reply_markup=keyboards.isPromo)
    await state.update_data(
                            num = mt,
                            cost = cost,
                            mess = mess.message_id,
                            mess1 = mess1.message_id)
@dp.callback_query(F.data == "yesPromo")
async def yesPromo_(callback:CallbackQuery,state:FSMContext):
    data = await state.get_data()
    mess = data['mess']
    mess1 = data['mess1']
    try:
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=mess,
                                        reply_markup=None)
    except:
        pass
    try:
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=mess1,
                                        reply_markup=None)
    except:
        pass
    mess = await callback.message.answer("🎁 <i>Введи промокод</i>",
                                  parse_mode='HTML',
                                  reply_markup=keyboards.Promo)
    await state.update_data(mess = mess.message_id)
    await state.set_state(PizzaOrderForm.waiting_promo_isTrue)
    await callback.answer()
@dp.message(PizzaOrderForm.waiting_promo_isTrue)
async def promoIstrue_(message:types.Message,state:FSMContext):
    data = await state.get_data()
    mess = data['mess']
    try:
        await bot.edit_message_reply_markup(chat_id=message.chat.id,
                                        message_id=mess,
                                        reply_markup=None)
    except:
        pass
    mt = message.text.strip()
    is_pr = await asyncio.to_thread(get_promo_1,mt)
    if is_pr is  None:
        mess = await message.answer("😔 <i>Такого промокода не существует\n🙃 Можете попробовать ввести снова или воспользуйтесь кнопками</i>",
                             parse_mode='HTML',
                             reply_markup=keyboards.Promo)
        await state.update_data(mess = mess.message_id)
        return
    idp , name , sale , date = is_pr
    await message.answer(f"🎉 <b>ОТЛИЧНО</b>\nДля вас действует скидка в размере {sale}%",
                         parse_mode='HTML')
    mess = await message.answer("🏘  <i>Введите адрес доставки</i>",
                                  parse_mode='HTML',
                                  reply_markup=keyboards.cencel_or,)
    await state.update_data(mess = mess.message_id,)
    await state.set_state(PizzaOrderForm.waiting_addres_for_sele)
    await state.update_data(sale = sale,
                            mess = mess.message_id)
#
async def not_addres_f(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    mess = data['mess']
    mess1 = data['mess1']
    try:
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=mess,
                                        reply_markup=None)
    except:
        pass
    try:
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=mess1,
                                        reply_markup=None)
    except:
        pass
    mess = await callback.message.answer("🏘 <i>Введите адрес доставки</i>",
                                  parse_mode='HTML',
                                  reply_markup=keyboards.cencel_or,)
    await state.update_data(mess = mess.message_id,)
    await state.set_state(PizzaOrderForm.waiting_addres_for_sele)


@dp.callback_query(F.data == "notPromo")
async def notPromo_(callback:CallbackQuery,state:FSMContext):
    await state.update_data(sale = None)
    await not_addres_f(callback,state)


@dp.message(PizzaOrderForm.waiting_addres_for_sele)
async def waiting_addres_(message:types.Message, state:FSMContext):
    date = await state.get_data()
    mess = date['mess']
    await bot.edit_message_reply_markup(chat_id=message.chat.id,
                                        message_id=mess,
                                        reply_markup=None)
    mt = message.text
    mess = await message.answer(f"🏘 <i>Адреc доставки: {mt}</i>",
                         parse_mode='HTML',
                         reply_markup=keyboards.isAddres)
    await state.update_data(mess = mess.message_id,
                            addres = mt)
@dp.callback_query(F.data == "notAddres")
async def notAddres_(callback:CallbackQuery,state:FSMContext):
    await not_addres_f(callback,state)
@dp.callback_query(F.data == "yesAddres")
async def yesAddres_(callback:CallbackQuery,state:FSMContext):
    data = await state.get_data()
    mess = data['mess']
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=mess,
                                        reply_markup=None)
    mess = await callback.message.answer("📞 <i>Напишите свой номер телефона</i>",
                                  parse_mode='HTML',
                                  reply_markup=keyboards.cencel_or)
    await state.set_state(PizzaOrderForm.waiting_number_for_sele)
    await state.update_data(mess = mess.message_id)
    await callback.answer()


async def waiting_number_f(callback:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    mess = data['mess']
    try:
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=mess,
                                        reply_markup=None)
    except:
        pass
    mess = await callback.message.answer("📞 <i>Напишите свой номер телефона</i>",
                                  parse_mode='HTML',
                                  reply_markup=keyboards.cencel_or)
    await state.set_state(PizzaOrderForm.waiting_number_for_sele)
    await state.update_data(mess = mess.message_id)
    await callback.answer()


@dp.message(PizzaOrderForm.waiting_number_for_sele)
async def waiting_number_(message:types.Message, state:FSMContext):
    mt = message.text
    mess = await message.answer(f"📞 {mt}<i> - Это ваш номер?</i>",
                         parse_mode='HTML',
                         reply_markup=keyboards.isNumber)
    await state.update_data(mess = mess.message_id,
    number = mt)


@dp.callback_query(F.data == "yesNumber")
async def yesNumber_(callback:CallbackQuery,state:FSMContext):
    data = await state.get_data()
    mess = data['mess']
    try:
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=mess,
                                        reply_markup=None)
    except:
        pass
    if data['sale'] is not None:
        cost = data['cost'] - (data['cost'] * data['sale'] / 100)
    else:
        cost = data['cost']
    mess = await callback.message.answer(f"""
😉 <i>Ваш заказ</i>
                                  
🍕 <b>пицца:</b> <i>{data['name']}</i>
📏 <b>Размер:</b> <i>{data['size']}</i>
🔥 <b>Количество:</b> <i>{data['num']}</i>

💸 <b>К оплате:</b> <i>{cost} ₽ Скидка:{data['sale'] or 0}% </i>                                
                                  """,
                                  parse_mode='HTML',
                                  reply_markup=keyboards.pay)
    await state.update_data(mess = mess.message_id,
                            cost = cost)
    
@dp.callback_query(F.data == "notNumber")
async def notNumber_(callback:CallbackQuery,state:FSMContext):
    await waiting_number_f(callback,state)
@dp.callback_query(F.data == "crypt")
async def crypt_(callback:CallbackQuery,state:FSMContext):
    data = await state.get_data()
    mess = data['mess']
    try:
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=mess,
                                        reply_markup=None)
    except:
        pass
    isOK = await save_dataBase(data)
    if not isOK:
        await callback.message.answer("❌ <i>Произошла ошибка</i>",
                                      parse_mode='HTML',
                                      reply_markup=keyboards.start_order)
        callback.answer()
        return
    isOK = await new_order(data['user_id'])
    if not isOK:
        await callback.message.answer("❌ <i>Произошла ошибка</i>",
                                      parse_mode='HTML',
                                      reply_markup=keyboards.start_order)
        callback.answer()
        return
    await callback.message.answer("😁 <i>Система оплаты пока что не проработана, поэтому сделаем вид, что вы оплатили)</i>",
                                  parse_mode='HTML')
    await callback.message.answer(f"""
🎉 <i>Ваш заказ принят!!!</i>
                                  
🍕 <b>пицца:</b> <i>{data['name']}</i>
📏 <b>Размер:</b> <i>{data['size']}</i>
🔥 <b>Количество:</b> <i>{data['num']}</i>

☎️ Горячая линия: <b>{config.hotline}</b>                     
""",
parse_mode='HTML',
reply_markup=keyboards.start_order)
    await bot.send_message(chat_id=config.admin,
                           text=f"""
📌 <i>Новый заказ</i> 🆕

🍕 <b>пицца:</b> <i>{data['name']}</i>
📏 <b>Размер:</b> <i>{data['size']}</i>
🔥 <b>Количество:</b> <i>{data['num']}</i>

🙋‍♂️ <b>userId</b> {data['user_id']}

👨‍🍳 <i>СРОЧНО ГОТОВИМ!</i>
""",
parse_mode='HTML')
    await callback.answer()
@dp.callback_query(F.data == "pay_num")
async def pay_num_(callback:CallbackQuery,state:FSMContext):
    data = await state.get_data()
    mess = data['mess']
    try:
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=mess,
                                        reply_markup=None)
    except:
        pass
    isOK = await save_dataBase(data)
    if not isOK:
        await callback.message.answer("❌ <i>Произошла ошибка</i>",
                                      parse_mode='HTML',
                                      reply_markup=keyboards.start_order)
        callback.answer()
        return
    isOK = await new_order(data['user_id'])
    if not isOK:
        await callback.message.answer("❌ <i>Произошла ошибка</i>",
                                      parse_mode='HTML',
                                      reply_markup=keyboards.start_order)
        callback.answer()
        return
    await callback.message.answer("😁 <i>Система оплаты пока что не проработана, поэтому сделаем вид, что вы оплатили)</i>",
                                  parse_mode='HTML')
    await callback.message.answer(f"""
🎉 <i>Ваш заказ принят!!!</i>
                                  
🍕 <b>пицца:</b> <i>{data['name']}</i>
📏 <b>Размер:</b> <i>{data['size']}</i>
🔥 <b>Количество:</b> <i>{data['num']}</i>

☎️ Горячая линия: <b>{config.hotline}</b>                     
""",
parse_mode='HTML',
reply_markup=keyboards.start_order)
    await bot.send_message(chat_id=config.admin,
                           text=f"""
📌 <i>Новый заказ</i> 🆕

🍕 <b>пицца:</b> <i>{data['name']}</i>
📏 <b>Размер:</b> <i>{data['size']}</i>
🔥 <b>Количество:</b> <i>{data['num']}</i>

🙋‍♂️ <b>userId</b> {data['user_id']}

👨‍🍳 <i>СРОЧНО ГОТОВИМ!</i>
""",
parse_mode='HTML',
reply_markup=keyboards.back_to_admin_orders)
    await callback.answer()
@dp.callback_query(F.data == "link_pay")
async def link_pay_(callback:CallbackQuery,state:FSMContext):
    data = await state.get_data()
    mess = data['mess']
    try:
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=mess,
                                        reply_markup=None)
    except:
        pass
    isOK = await save_dataBase(data)
    if not isOK:
        await callback.message.answer("❌ <i>Произошла ошибка</i>",
                                      parse_mode='HTML',
                                      reply_markup=keyboards.start_order)
        callback.answer()
        return
    isOK = await new_order(data['user_id'])
    if not isOK:
        await callback.message.answer("❌ <i>Произошла ошибка</i>",
                                      parse_mode='HTML',
                                      reply_markup=keyboards.start_order)
        callback.answer()
        return
    await callback.message.answer("😁 <i>Система оплаты пока что не проработана, поэтому сделаем вид, что вы оплатили)</i>",
                                  parse_mode='HTML')
    await callback.message.answer(f"""
🎉 <i>Ваш заказ принят!!!</i>
                                  
🍕 <b>пицца:</b> <i>{data['name']}</i>
📏 <b>Размер:</b> <i>{data['size']}</i>
🔥 <b>Количество:</b> <i>{data['num']}</i>

☎️ Горячая линия: <b>{config.hotline}</b>                     
""",
parse_mode='HTML',
reply_markup=keyboards.start_order)
    await bot.send_message(chat_id=config.admin,
                           text=f"""
📌 <i>Новый заказ</i> 🆕

🍕 <b>пицца:</b> <i>{data['name']}</i>
📏 <b>Размер:</b> <i>{data['size']}</i>
🔥 <b>Количество:</b> <i>{data['num']}</i>

🙋‍♂️ <b>userId</b> {data['user_id']}

👨‍🍳 <i>СРОЧНО ГОТОВИМ!</i>
""",
parse_mode='HTML')
    await state.clear()
    await callback.answer()
    


#ВЫЗОВ АДМИН ПАНЕЛИ /admin
@dp.message(Command("admin"))
async def admin(message:types.Message,state:FSMContext):
    await message.answer("🔒 Введи пароль для входа в <i>AdminPanel</i>",
                         parse_mode='HTML')
    await state.set_state(PizzaOrderForm.waiting_password_admin)
@dp.message(PizzaOrderForm.waiting_password_admin)
async def password_admin_panel(message:types.Message,state:FSMContext):
    password = message.text.strip()
    if password != config.password:
        await message.answer("<b>🔒 Не верный пароль!!!</b>\n<i>Попробуй еще раз</i>",
                             parse_mode='HTML')
        return
    await message.answer("<i>😉 AdminPanel</i>",
                       parse_mode='HTML',
                       reply_markup=keyboards.admin_panel)
#ОБРАТНО В АДМИН ПАНЕЛЬ back_to_admin
@dp.callback_query(F.data == "back_to_admin")
async def back_to_admin(callback:CallbackQuery,state:FSMContext):
    await state.clear()
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("<i>😉 AdminPanel</i>",
                       parse_mode='HTML',
                       reply_markup=keyboards.admin_panel)
    await callback.answer()
#ПРОСМОТР ПИЦЦ check_pizzas
@dp.callback_query(F.data == "check_pizzas")
async def check_orders(callback:CallbackQuery):
    await callback.message.edit_text(text="🔍 <i>Проверяем все пиццы</i>",
                                     parse_mode='HTML',
                                     reply_markup=None)
    pizzas = await asyncio.to_thread(get_pizza)
    if not pizzas:
        await callback.message.answer(f"😔 <i>Пицц нет</i>",
                                  parse_mode='HTML',
                                  reply_markup=keyboards.back_to_admin)
        return
    await callback.message.answer(f"<i>Пиццы в меню:</i>",
                                  parse_mode='HTML')
    for pizza in pizzas:
        id,name,photo,sort,priceL,priceM,priceB,date = pizza
        await callback.message.answer_photo(photo=photo,
                                            caption=f"""
🆔 <b>id:</b> {id} 
🍕 <b>Наименование:</b> {name}
🧂 <b>Ингредиенты:</b> {sort}
💸 <b>Цена:</b> L:{priceL} M:{priceM} B:{priceB}
⏳ <b>Дата создания:</b> {date}""",
parse_mode='HTML',
reply_markup=keyboards.cencel)
    await callback.message.answer("<i>😉 AdminPanel</i>",
                                  parse_mode='HTML',
                                  reply_markup=keyboards.back_to_admin_orders)
    await callback.answer()
#ПРОСМОТР ЗАКАЗОВ check_orders
async def orders_by_status(callback: CallbackQuery, 
                                   state: FSMContext, 
                                   status_key,
                                   status_text,
                                   emoji,
                                   state_class):
    data = await state.get_data()
    orders = data['orders']
    order = orders.get(status_key, [])
    
    try:
        mess = data.get('mess')
        if mess:
            await bot.edit_message_reply_markup(
                chat_id=callback.message.chat.id,
                message_id=mess,
                reply_markup=None
            )
    except:
        pass
    
    if not order:
        await callback.message.answer(
            "<i>😔 Заказов в этом статусе нет</i>",
            parse_mode='HTML',
            reply_markup=keyboards.back_to_admin_orders
        )
        return
    
    # Отображаем все заказы
    for i, orderW in enumerate(order, 1):
        idOrder, user_id, size, type_, quantity, address, phone, order_date = orderW
        await callback.message.answer(f"""
📌 <b>Заказ:</b> {i}. <b>ID:</b> <code>{idOrder}</code>
🎲 <b>Статус:</b> {emoji} <i>{status_text}</i>

🍕 <b>{type_}</b>
📏 <b>Размер:</b> <i>{size}</i>
🔥 <b>Количество:</b> <i>{quantity}</i>

🏘 <b>Адрес:</b> <i>{address}</i>
📞 <b>Телефон:</b> <i>{phone}</i>
🙋‍♂️ <b>User ID:</b> <i>{user_id}</i>

📅 <b>Дата заказа:</b> <i>{order_date}</i>
""", parse_mode='HTML')
    
    mess = await callback.message.answer(
        "<i>Напишите ID заказа для изменения статуса</i>",
        parse_mode='HTML',
        reply_markup=keyboards.back_to_admin_orders
    )
    
    await state.update_data(mess=mess.message_id)
    await state.set_state(state_class)
    await callback.answer()

async def order_id_input(message: types.Message, 
                                state: FSMContext, 
                                status_text,
                                emoji):
    data = await state.get_data()
    
    try:
        mess = data.get('mess')
        if mess:
            await bot.edit_message_reply_markup(
                chat_id=message.chat.id,
                message_id=mess,
                reply_markup=None
            )
    except:
        pass
    
    idOrder = message.text.strip()
    order = await asyncio.to_thread(get_1_order, idOrder)
    
    if order is None:
        await message.answer(
            "<i>😔 Несуществующий ID заказа</i>\nПопробуйте ввести заново",
            parse_mode='HTML',
            reply_markup=keyboards.back_to_admin_orders
        )
        return
    
    user_id, size, name, num, address, phone, order_date = order
    
    await state.update_data(
        order=order,
        id_order=idOrder
    )
    
    mess = await message.answer(f"""
🕹 <i>С помощью кнопок можно изменить статус заказа</i>

📌 <b>Заказ с ID:</b> <code>{idOrder}</code>
🎲 <b>Статус:</b> {emoji} <i>{status_text}</i>

🍕 <b>{name}</b>
📏 <b>Размер:</b> <i>{size}</i>
🔥 <b>Количество:</b> <i>{num}</i>

🏘 <b>Адрес:</b> <i>{address}</i>
📞 <b>Телефон:</b> <i>{phone}</i>
🙋‍♂️ <b>User ID:</b> <i>{user_id}</i>

📅 <b>Дата заказа:</b> <i>{order_date}</i>
""", parse_mode='HTML', reply_markup=keyboards.change_status)
    
    await state.update_data(mess=mess.message_id)

# обновляем хэндлеры

@dp.callback_query(F.data == "check_orders")
async def check_orders(callback: CallbackQuery, state: FSMContext):
    orders = await asyncio.to_thread(get_all_orders)
    if not orders:
        await callback.message.edit_text(
            "❌ Не удалось загрузить заказы",
            reply_markup=keyboards.back_to_admin
        )
        await callback.answer()
        return
    
    await state.update_data(orders=orders)
    await callback.message.edit_text(
        text="👀 <i>Выбираем что посмотреть</i>",
        parse_mode='HTML',
        reply_markup=keyboards.orders_all
    )
    await callback.answer()

@dp.callback_query(F.data == "new")
async def new_order_(callback: CallbackQuery, state: FSMContext):
    await orders_by_status(
        callback, state, 
        status_key="new",
        status_text="новый",
        emoji="🆕",
        state_class=PizzaOrderForm.waiting_id_new
    )

@dp.callback_query(F.data == "cooking")
async def cooking_order_(callback: CallbackQuery, state: FSMContext):
    await orders_by_status(
        callback, state,
        status_key="cooking",
        status_text="готовится",
        emoji="🧑‍🍳",
        state_class=PizzaOrderForm.waiting_id_cooking
    )

@dp.callback_query(F.data == "ready")
async def ready_order_(callback: CallbackQuery, state: FSMContext):
    await orders_by_status(
        callback, state,
        status_key="ready",
        status_text="готов",
        emoji="🍽",
        state_class=PizzaOrderForm.waiting_id_ready
    )

@dp.callback_query(F.data == "inRoad")
async def inRoad_order_(callback: CallbackQuery, state: FSMContext):
    await orders_by_status(
        callback, state,
        status_key="inRoad",
        status_text="в пути",
        emoji="🚚",
        state_class=PizzaOrderForm.waiting_id_inRoad
    )

@dp.callback_query(F.data == "deliver")
async def deliver_order_(callback: CallbackQuery, state: FSMContext):
    await orders_by_status(
        callback, state,
        status_key="deliver",
        status_text="доставлен",
        emoji="✅",
        state_class=PizzaOrderForm.waiting_id_deliver
    )
@dp.callback_query(F.data == "deliver_all")
async def deliver_order_(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        mess = data.get('mess')
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                            message_id=mess,
                                            reply_markup=None)
    except:
        pass
    orders = await get_deliver_orders()
    if not orders:
        await callback.message.answer(
                "❌ Не удалось загрузить заказы",
                reply_markup=keyboards.back_to_admin_orders
            )
        await state.clear()
        await callback.answer()
        return
    text ="😁 <b>Это все доставленные заказы</b> \n"
    for order in orders:
       id_order,user_id,size,name,num,address,phone,order_date = order
       text +=f"""
📌 <b>Заказ с ID:</b> <code>{id_order}</code>
🎲 <b>Статус:</b> <i>доставлен</i>

🍕 <b>{name}</b>
📏 <b>Размер:</b> <i>{size}</i>
🔥 <b>Количество:</b> <i>{num}</i>

🏘 <b>Адрес:</b> <i>{address}</i>
📞 <b>Телефон:</b> <i>{phone}</i>
🙋‍♂️ <b>User ID:</b> <i>{user_id}</i>

📅 <b>Дата заказа:</b> <i>{order_date}</i>
-----------------------------
"""
    await callback.message.answer(text,
                                  parse_mode='HTML',
                                  reply_markup=keyboards.back_to_admin_orders)
    await state.clear()
    await callback.answer()

# для ввода ID
@dp.message(PizzaOrderForm.waiting_id_new)
async def id_new_order_(message: types.Message, state: FSMContext):
    await order_id_input(message, state, "новый", "🆕")

@dp.message(PizzaOrderForm.waiting_id_cooking)
async def id_cooking_order_(message: types.Message, state: FSMContext):
    await order_id_input(message, state, "готовится", "🧑‍🍳")

@dp.message(PizzaOrderForm.waiting_id_ready)
async def id_ready_order_(message: types.Message, state: FSMContext):
    await order_id_input(message, state, "готов", "🍽")

@dp.message(PizzaOrderForm.waiting_id_inRoad)
async def id_inRoad_order_(message: types.Message, state: FSMContext):
    await order_id_input(message, state, "в пути", "🚚")

@dp.message(PizzaOrderForm.waiting_id_deliver)
async def id_deliver_order_(message: types.Message, state: FSMContext):
    await order_id_input(message, state, "доставлен", "✅")

# Функция для изменения статуса 
async def input_status(callback: CallbackQuery, state: FSMContext, status):
    data = await state.get_data()
    order = data.get('order')
    id_order = data.get('id_order')
    
    if not order or not id_order:
        await callback.answer("❌ Данные заказа не найдены")
        return
    
    try:
        mess = data.get('mess')
        if mess:
            await bot.edit_message_reply_markup(
                chat_id=callback.message.chat.id,
                message_id=mess,
                reply_markup=None
            )
    except:
        pass
    
    user_id, size, name, num, address, phone, order_date = order
    
    # Обновляем статус в базе данных
    isTrue = await asyncio.to_thread(new_status, status, id_order)
    if not isTrue:
        await callback.message.answer(
            "❗️ <i>Произошла ошибка при обновлении статуса</i>",
            parse_mode='HTML',
            reply_markup=keyboards.back_to_admin_orders
        )
        return
    
    # Определяем текстовое представление статуса
    status_fil = {
        "new": "🆕 новый заказ",
        "cooking": "🧑‍🍳 готовится",
        "ready": "🍽 готов",
        "inRoad": "🚚 в доставке",
        "deliver": "✅ доставлен"
    }
    
    status_text = status_fil.get(status, "неизвестный статус")
    
    # Показываем обновленный заказ
    await callback.message.answer(f"""
📌 <b>Заказ с ID:</b> <code>{id_order}</code>
🎲 <b>Статус:</b> <i>{status_text}</i>

🍕 <b>{name}</b>
📏 <b>Размер:</b> <i>{size}</i>
🔥 <b>Количество:</b> <i>{num}</i>

🏘 <b>Адрес:</b> <i>{address}</i>
📞 <b>Телефон:</b> <i>{phone}</i>
🙋‍♂️ <b>User ID:</b> <i>{user_id}</i>

📅 <b>Дата заказа:</b> <i>{order_date}</i>
""", parse_mode='HTML', reply_markup=keyboards.back_to_admin_orders)
    
    #Отправляем уведомление клиенту
    try:
        message_to_client = f"""
📌 <b>Заказ с ID:</b> <code>{id_order}</code>
🎲 <b>Статус изменен на:</b> <i>{status_text}</i>

🍕 <b>{name}</b>
📏 <b>Размер:</b> <i>{size}</i>
🔥 <b>Количество:</b> <i>{num}</i>

☎️ Горячая линия: <b>{config.hotline}</b>
"""
        
        if status != "deliver":
            await bot.send_message(
                chat_id=user_id,
                text=message_to_client,
                parse_mode='HTML'
            )
        else:
            await bot.send_message(
                chat_id=user_id,
                text=message_to_client,
                parse_mode='HTML',
                reply_markup=keyboards.start_order_call
            )
        
        await callback.message.answer(
            "📱 <i>Клиенту отправлено уведомление об изменении статуса заказа</i>",
            parse_mode='HTML'
        )
    except Exception as e:
        logging.error(f"Ошибка при отправке уведомления клиенту: {e}")
        await callback.message.answer(
            "❌ <i>Не удалось отправить уведомление клиенту</i>",
            parse_mode='HTML'
        )
    
    await state.clear()
    await callback.answer()

# для изменения статуса
@dp.callback_query(F.data == "new_status")
async def new_status_call(callback: CallbackQuery, state: FSMContext):
    await input_status(callback, state, "new")

@dp.callback_query(F.data == "cooking_status")
async def cooking_status_call(callback: CallbackQuery, state: FSMContext):
    await input_status(callback, state, "cooking")

@dp.callback_query(F.data == "ready_status")
async def ready_status_call(callback: CallbackQuery, state: FSMContext):
    await input_status(callback, state, "ready")

@dp.callback_query(F.data == "inRoad_status")
async def inRoad_status_call(callback: CallbackQuery, state: FSMContext):
    await input_status(callback, state, "inRoad")

@dp.callback_query(F.data == "deliver_status")
async def deliver_status_call(callback: CallbackQuery, state: FSMContext):
    await input_status(callback, state, "deliver")



#add_promo СОЗДАТЬ ПРОМО - СКИДКУ
@dp.callback_query(F.data == "add_promo")
async def add_promo_notf(callback:CallbackQuery,state:FSMContext):
    await state.set_state(PizzaOrderForm.waiting_name_promo)
    await callback.message.edit_text("😋 <i>Создаем промокод</i>",
                                  parse_mode='HTML',
                                  reply_markup=None)
    mess = await callback.message.answer("✏️ <i>Введи название промокоду</i>",
                                  parse_mode='HTML',
                                  reply_markup=keyboards.cencel)
    await state.update_data(mess = mess.message_id)
    await callback.answer()
@dp.message(PizzaOrderForm.waiting_name_promo)
async def name_promo(message:types.Message,state:FSMContext):
    name = message.text
    isName = await asyncio.to_thread(is_promo,name)
    if isName:
        await message.answer("❌ <i>Промокод с таким название уже существует</i>\nВведи другое имя",
                             parse_mode='HTML')
        return
    await state.set_state(PizzaOrderForm.waiting_sale_promo)
    data = await state.get_data()
    mess = data['mess']
    await bot.edit_message_reply_markup(chat_id=message.chat.id,
                                        message_id=mess,
                                        reply_markup=None)
    mess = await message.answer("✏️ <i>Напиши скидку, которая будет рассчитываться в %\nОт тебя требуется только число\nНапример:</i>\n<b>10</b>\n<b>15</b>\n<b>30</b>",
                                parse_mode='HTML',
                                reply_markup=keyboards.cencel)
    await state.update_data(name = name,
                            mess = mess.message_id)
@dp.message(PizzaOrderForm.waiting_sale_promo)
async def sale_promo_notf(message:types.Message,state:FSMContext):
    sale = message.text.strip()
    if not int(sale):
        await message.answer("❌ <i>Введено не число</i>\nПопробуй снова",
                             parse_mode='HTML')

        return
    sale = int(sale)
    if (sale < 1 or sale > 50):
        await message.answer("❌ Скидка слишком большая или меньше 1\nВведи число >0 и <51" )
        return
    data = await state.get_data()
    mess = data['mess']
    await bot.edit_message_reply_markup(chat_id=message.chat.id,
                                        message_id=mess,
                                        reply_markup=None)
    isOk = await asyncio.to_thread(add_promo,data['name'],sale)
    if not isOk:
        await message.answer("❌ <i>Произошла ошибка</i>",
                             parse_mode='HTML',
                             reply_markup=keyboards.back_to_admin)
        await state.clear()
        return
    await message.answer(f"""
🎉 <b>Промокод успешно создан!</b>
🎫 <b>Имя:</b> {data['name']} - <i>пользователь вводит при покупке, что бы получить скидку</i>
🎁 <b>Размер скидки:</b> {sale}%                         
""",
parse_mode='HTML',
reply_markup=keyboards.back_to_admin_promo)
    await state.clear()
#УДАЛИТЬ ПРОМО delete_promo
@dp.callback_query(F.data == "delete_promo")
async def delete_promo_f(callback:CallbackQuery,state:FSMContext):
    await callback.message.edit_text(text="🤔 <i>Удаляем промокод:</i>",
                                     parse_mode='HTML',
                                     reply_markup=None)
    promos = await asyncio.to_thread(get_promo)
    if not promos:
        await callback.message.answer("<i>😔 Промокодов нет</i>",
                                      parse_mode='HTML',
                                      reply_markup=keyboards.back_to_admin)
        await callback.answer()
        return
    promo_text = "<i>👇 Все промокоды:</i>\n\n"
    for promo in promos:
        id, name, sale, date = promo
        promo_text += f"""
🆔 <b>ID:</b> <code>{id}</code>
🎫 <b>Имя:</b> <i>{name}</i>
🎁 <b>Скидка:</b> <i>{sale}%</i>
⏳ <b>Дата создания:</b> <i>{date}</i>
{'─' * 30}
"""
    
    await callback.message.answer(
        promo_text,
        parse_mode='HTML'
    )
    mess = await callback.message.answer("🆔 <i>Напиши id промокода для удаления:</i>",
                                  parse_mode='HTML',
                                  reply_markup=keyboards.cencel)
    await state.update_data(mess = mess.message_id)
    await state.set_state(PizzaOrderForm.waiting_id_delete_promo)
    await callback.answer()
@dp.message(PizzaOrderForm.waiting_id_delete_promo)
async def id_delete_promo_F(message:types.Message,state:FSMContext):
    try:
        pr_id = int(message.text.strip())
    except ValueError:
        await message.answer("<i>❌ Вы ввели не число\nПопробуйте еще раз:</i>",
                         parse_mode='HTML')
        return
    isOk = await asyncio.to_thread(is_promo_id,pr_id)
    if not isOk:
        await message.answer("❗️ <i>Промокод с таким id не существует</i>\nВведи другое id",
                             parse_mode='HTML')
        return
    data = await state.get_data()
    mess = data['mess']
    await bot.edit_message_reply_markup(chat_id=message.chat.id,
                                        message_id=mess,
                                        reply_markup=None)
    isOk2 = await asyncio.to_thread(delete_promo_is,pr_id)
    if not isOk2:
        await message.answer("❌ <i>Произошла ошибка</i>",
                             parse_mode='HTML',
                             reply_markup=keyboards.back_to_admin)
        await state.clear()
        return
    await message.answer(f"👌 <i>Промокод с id: {pr_id} \n✅ Успешно удален</i>",
                         parse_mode='HTML',
                         reply_markup=keyboards.back_to_admin_delete_promo)
    await state.clear()
    


    
#ПРОСМОТР ВСЕХ ПРОМО check_promo
@dp.callback_query(F.data == "check_promo")
async def check_promo_notF(callback:CallbackQuery):
    await callback.message.edit_text(text="👀 <i>Смотрим на промокоды:</i>",
                                     parse_mode='HTML',
                                     reply_markup=None)
    promos = await asyncio.to_thread(get_promo)
    if not promos:
        await callback.message.answer("<i>😔 Промокодов нет</i>",
                                      parse_mode='HTML',
                                      reply_markup=keyboards.back_to_admin)
        await callback.answer()
        return
    for promo in promos:
        id, name , sale, date = promo
        await callback.message.answer(f"""
🆔 <b>id:</b> <i>{id}</i>
🎫 <b>Имя:</b> <i>{name}</i>
🎁 <b>Скидка:</b> <i>{sale}%</i>
⏳ <b>Дата создания:</b> <i>{date}</i>
""",
                                parse_mode='HTML')
    await callback.message.answer(">>>",
                                  reply_markup=keyboards.back_to_admin)
    await callback.answer()

#delete_pizza
@dp.callback_query(F.data == "delete_pizza")
async def delete_pizza_notf(callback:CallbackQuery,state:FSMContext):
    await callback.message.edit_text(text="😔 <i>Удаляем пиццу</i>",
                                     parse_mode='HTML',
                                     reply_markup=None)
    pizzas = await asyncio.to_thread(get_pizza)
    if not pizzas:
        await callback.message.answer(f"😔 <i>Пицц нет</i>",
                                  parse_mode='HTML',
                                  reply_markup=keyboards.back_to_admin)
        return
    await callback.message.answer(f"🍕 <i>Пиццы в меню:</i>",
                                  parse_mode='HTML')
    for pizza in pizzas:
        id,name,photo,sort,priceL,priceM,priceB,date = pizza
        await callback.message.answer_photo(photo=photo,
                                            caption=f"""
🆔 <b>id:</b> {id} 
🍕 <b>Наименование:</b> {name}
🧂 <b>Ингредиенты:</b> {sort}
💸 <b>Цена:</b> L:{priceL} M:{priceM} B:{priceB}
⏳ <b>Дата создания:</b> {date}""",
parse_mode='HTML')
    await state.set_state(PizzaOrderForm.waiting_id_delete_pizza)
    await callback.message.answer("🆔 <i>Напиши id пиццы, котрую стоит удалить</i>",
                                  parse_mode='HTML',
                                  reply_markup=keyboards.cencel)
    await callback.answer()
@dp.message(PizzaOrderForm.waiting_id_delete_pizza)
async def id_delete_pizza(message:types.Message,state:FSMContext):
    id = message.text.strip()
    pizza = await asyncio.to_thread(get_pizza_1,id)
    if not pizza:
        await message.answer("❌ <i>Пиццы с таким id не существует введи заново</i>",
                             parse_mode='HTML')
        return
    isDelete = await asyncio.to_thread(delete_pizza,id)
    if not isDelete:
        await message.answer("❌ <i>Произошла ошибка!"
        "</i>",
                             parse_mode='HTML')
        await state.clear()
        return
    await state.clear()
    await message.answer(f"Пицца с id {id} успешно удалена",
                         parse_mode='HTML',
                         reply_markup=keyboards.back_to_admin_delete)
@dp.callback_query(F.data == "add_pizza")
async def add_pizza(callback:CallbackQuery,state:FSMContext):
    await callback.message.edit_text("😋 <b>Создаем пиццу)</b>",
                                     parse_mode='HTML',
                                     reply_markup=None)
    await state.set_state(PizzaOrderForm.waiting_name_pizza_adm)
    mess = await callback.message.answer("🍕 <i>Введи название пиццы</i>",
                                  parse_mode='HTML',
                                  reply_markup=keyboards.cencel)
    await state.update_data(mess = mess.message_id)
    await callback.answer()
@dp.message(PizzaOrderForm.waiting_name_pizza_adm)
async def name_pizza_adm(message:types.Message,state:FSMContext):
    data = await state.get_data()
    mess = data['mess']
    await bot.edit_message_reply_markup(chat_id=message.chat.id,
                                        message_id=mess,
                                        reply_markup=None)
    name = message.text.strip()
    await state.update_data(name=name)
    await state.set_state(PizzaOrderForm.waiting_photo_pizza_adm)
    mess = await message.answer("📸 <i>Жду фото вашей аппетитной пиццы</i>\n<b>Отправь фото пиццы</b>\n❗️После отправки не удаляй его, иначе оно пропадет из базы данных( ",
                         parse_mode='HTML',
                         reply_markup=keyboards.cencel)
    await state.update_data(mess=mess.message_id)
@dp.message(PizzaOrderForm.waiting_photo_pizza_adm)
async def photo_pizza_adm(message:types.Message,state:FSMContext):
    if not message.photo:
        await message.answer("❗️ <i>Это не фото, проверь формат отправляеимого (.png, .jpg)</i>\n<b>Отправь снова</b>",
                             parse_mode='HTML',
                             reply_markup=keyboards.cencel)
        return
    data = await state.get_data()
    mess = data['mess']
    await bot.edit_message_reply_markup(chat_id=message.chat.id,
                                        message_id=mess,
                                        reply_markup=None)
    photo = message.photo[-1]
    photo_id = photo.file_id
    await state.update_data(photo=photo_id)
    await state.set_state(PizzaOrderForm.waiting_sort_pizza_adm)
    mess = await message.answer("🧂 <i>Напиши ингредиенты через запятую</i>\nПример: Сыр, Лук, Мясо, ...s",
                         reply_markup=keyboards.cencel,
                         parse_mode='HTML')
    await state.update_data(mess=mess.message_id)
@dp.message(PizzaOrderForm.waiting_sort_pizza_adm)
async def sort_pizza_adm(message:types.Message,state:FSMContext):
    data = await state.get_data()
    mess = data['mess']
    await bot.edit_message_reply_markup(chat_id=message.chat.id,
                                        message_id=mess,
                                        reply_markup=None)
    sort = message.text.strip()
    await state.update_data(sort=sort)
    await state.set_state(PizzaOrderForm.waiting_price_pizza_adm)
    mess = await message.answer("💸 <i>Введи цену пиццы</i>\nПример: <code>100,200,300</code> \n<i>(L,M,B - без пробелов,через запаятую)</i>",
                         parse_mode='HTML',
                         reply_markup=keyboards.cencel,)
    await state.update_data(mess=mess.message_id)
    await state.update_data(mess=mess.message_id)
@dp.message(PizzaOrderForm.waiting_price_pizza_adm)
async def price_pizza_adm(message:types.Message,state:FSMContext):
    size = message.text.strip()
    size = size.split(",")
    if len(size) != 3:
        await message.answer("<i>❌ Неверный формат ввода\nВведи заново\nПример: 100,200,300</i>",
                             parse_mode='HTML',
                             reply_markup=keyboards.cencel)
        return
    data = await state.get_data()
    mess = data['mess']
    await bot.edit_message_reply_markup(chat_id=message.chat.id,
                                        message_id=mess,
                                        reply_markup=None)
    data = await state.get_data()
    isTrue = await asyncio.to_thread(add_pizzaW,
                                     data['name'],
                                     data['photo'],
                                     data['sort'],
                                     size[0],
                                     size[1],
                                     size[2])
    if not isTrue:
        await message.answer("<i>😔 К сожелению произошла ошибка(</i>",
                             reply_markup=keyboards.back_to_admin,
                             parse_mode='HTML')
    await message.answer_photo(photo=data['photo'],
                               caption=f"""
🎊 <i>Поздравляю, пицца добавлена!</i>
🍕 <b>Название:</b> {data['name']}
🧂 <b>Ингридиенты:</b> {data['sort']}
💸 <b>Цена за L:</b> {size[0]}               
💸 <b>Цена за M:</b> {size[1]}               
💸 <b>Цена за B:</b> {size[2]}               
""",
                         reply_markup=keyboards.back_to_admin,
                         parse_mode='HTML')
#СТАТИСТИКА stat_admin
@dp.callback_query(F.data == "stat_admin")
async def stats(callback:CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    stats = get_pizza_stats()
    text = f"""
📊 СТАТИСТИКА ПИЦЦЕРИИ:

🍕 Всего заказов: {stats['total_orders']}
👥 Уникальных клиентов: {stats['unique_users']}
📅 Заказов сегодня: {stats['today_orders']}

🏆 Самые популярные пиццы:
"""
    for i, (pizza_type, count) in enumerate(stats['popular_pizzas'], 1):
        text += f"  {i}. {pizza_type} - {count} заказов\n"
    
    await callback.message.answer(text,
                         parse_mode='HTML',
                         reply_markup=keyboards.back_to_admin)
    await callback.answer()


import logging
logging.basicConfig(level=logging.INFO)
async def main():
    logging.basicConfig(level=logging.INFO)
    try:
        print("🚀 Бот запущен")
        await dp.start_polling(bot)
    except UnicodeDecodeError as e:
        print(f"🚫 Ошибка декодирования: {e}")
    except Exception as e:
        print(f"💥 Непредвиденная ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())