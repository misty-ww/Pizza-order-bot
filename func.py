import sqlite3
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
#УДАЛИТЬ ПРОМО
def delete_promo_is(id):
    try:
        baze = sqlite3.connect('pizza_order.db')
        cursor = baze.cursor()
        cursor.execute("DELETE FROM promo WHERE id = ?",(id,))
        baze.commit()
        if cursor.rowcount == 0:
            return False
        return True
    finally:
        if cursor:
            cursor.close()
        if baze:
            baze.close()
#ПРОВЕРКА СУЩЕСТВУЕТ ЛИ ПРОМО
def is_promo_id(id):
    try:
        baze = sqlite3.connect('pizza_order.db')
        cursor = baze.cursor()
        cursor.execute("SELECT 1 FROM promo WHERE id = ?",(id,))
        if cursor.fetchone():
            return True
        return False
    finally:
        if cursor:
            cursor.close()
        if baze:
            baze.close()
#ПОЛУЧЕНИЕ ПРОМО ИЗ БД
def get_promo_1(name):
    try:
        baze = sqlite3.connect('pizza_order.db')
        cursor = baze.cursor()
        cursor.execute("SELECT 1 FROM promo WHERE name = ?",(name,))
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()
        if baze:
            baze.close()
#ПРОВЕРКА СУЩЕСТВУЕТ ЛИ ПРОМО
def is_promo(name):
    try:
        baze = sqlite3.connect('pizza_order.db')
        cursor = baze.cursor()
        cursor.execute("SELECT 1 FROM promo WHERE name = ?",(name,))
        if cursor.fetchone():
            return True
        return False
    finally:
        if cursor:
            cursor.close()
        if baze:
            baze.close()
#ПОЛУЧЕНИЕ ВСЕХ ПРОМО
def get_promo():
    try:
        baze = sqlite3.connect('pizza_order.db')
        cursor = baze.cursor()
        cursor.execute("SELECT 1 FROM promo")
        if cursor.fetchone():
            cursor.execute("SELECT * FROM promo")
            return cursor.fetchall()
        return False
    finally:
        if cursor:
            cursor.close()
        if baze:
            baze.close()
    
#ДОБОВLЯЕМ ПРОМО В БД
def add_promo(name,sale):
    try:
        baze = sqlite3.connect('pizza_order.db')
        cursor = baze.cursor()
        cursor.execute("INSERT INTO 'promo' ('name','sale') VALUES (?,?)",
                       (name,sale))
        baze.commit()
        if cursor.rowcount == 1:
            return True
        return False
    finally:
        if cursor:
            cursor.close()
        if baze:
            baze.close()

#СОЗДАНИЕ КЛАВИАТУРЫ С ЦЕНАМИ
def make_keyboard(priceL,priceM,priceB):
    size_key = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=f"Size: L Цена:{priceL}")],
            [KeyboardButton(text=f"Size: M Цена:{priceM}")],
            [KeyboardButton(text=f"Size: B Цена:{priceB}")],
            [KeyboardButton(text=f"📌 Изменить пиццу")],
            [KeyboardButton(text=f"😣 Отмена заказа")]
        ], resize_keyboard= True
    )
    return size_key

#УДАЛЯЕМ ПИЦЦУ ИЗ БД
def delete_pizza(id):
    try:
        baze = sqlite3.connect('pizza_order.db')
        cursor = baze.cursor()
        cursor.execute("DELETE FROM pizza WHERE id = ?",(id,))
        baze.commit()
        if cursor.rowcount == 0:
            return False
        return True
    finally:
        if cursor:
            cursor.close()
        if baze:
            baze.close()


#ПОЛУЧАЕМ ПИЦЦУ ИЗ БД
def get_pizza_1(id):
    try:
        baze = sqlite3.connect('pizza_order.db')
        cursor = baze.cursor()
        cursor.execute("SELECT id, name, photo, sort, price_L, price_M, price_B, date FROM pizza WHERE id = ?",(id,))
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()
        if baze:
            baze.close()


#ПОЛУЧАЕМ ПИЦЦЫ ИЗ БД
def get_pizza():
    try:
        baze = sqlite3.connect('pizza_order.db')
        cursor = baze.cursor()
        cursor.execute("SELECT * FROM pizza")
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if baze:
            baze.close()
#f ДОБАВЛЕНИЕ НОВОЙ пиццы
def add_pizzaW(name,photo,sort,price_L,price_M,price_B):
    try:
        baze = sqlite3.connect('pizza_order.db')
        cursor = baze.cursor()
        cursor.execute("INSERT INTO 'pizza' ('name','photo','sort','price_L','price_M','price_B') VALUES (?,?,?,?,?,?)",(name,photo,sort,price_L,price_M,price_B,))
        baze.commit()
        if cursor.rowcount == 1:
            return True
        return False
    finally:
        if cursor:
            cursor.close()
        if baze:
            baze.close()

#ОБРАБОТКА НОВОВОГО user
def new_user(user_id,name,username):
    try:
        baze = sqlite3.connect('dp.db')
        cursor = baze.cursor()
        cursor.execute("SELECT 1 FROM users WHERE tg_id = ?",(user_id,))
        if cursor.fetchone():
            return
        cursor.execute("INSERT INTO 'users' ('tg_id','name','username') VALUES (?,?,?)",(user_id,name,username or None))
        baze.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        if cursor:
            cursor.close()
        if baze:
            baze.close()

# ОБНОВЛЕНИЕ СТАТУСА ЗАКАЗА
def new_status(status,id_order):
    try:
        conn = sqlite3.connect('pizza_order.db')
        cursor = conn.cursor()
        cursor.execute("""
UPDATE orders SET status = ? WHERE id = ?
""",(status,id_order))
        conn.commit()
        if cursor.rowcount > 0:
            return True
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# СОХРАНЕНИЕ ЗАКАЗА В БД
async def save_dataBase(data: dict):
    try:
        conn = sqlite3.connect('pizza_order.db')
        cursor = conn.cursor()
        insert_sql = """
        INSERT INTO orders (user_id,size,type,quantity,address,phone)
    VALUES (?,?,?,?,?,?)
    """
        insert_values = (
        data['user_id'],
        data['size'],
        data['name'],
        data['num'],
        data['addres'],
        data['number'],
    )
        cursor.execute(insert_sql,insert_values)
        conn.commit()
        if cursor.rowcount > 0:
            return True
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


#ОБНОВЛЕНИЕ СЧЕТЧИКА ЗАКАЗОВ КЛИЕНТА
async def new_order(user_id: int,):
    conn = sqlite3.connect('dp.db')
    cursor = conn.cursor()
    try:
        sq_inpbaze = """ 
        SELECT total_orders FROM users WHERE tg_id = ?
        """
        user_id
        cursor.execute(sq_inpbaze,(user_id,))
        result = cursor.fetchone()
        if result:
            orders = result[0] or 0
        else:
            orders = 0
        orders +=1
        sq_com = """
        UPDATE users SET total_orders = ? WHERE tg_id = ?
        """

        sq_input = (orders,user_id)
        cursor.execute(sq_com,sq_input)
        conn.commit()
        if cursor.rowcount >0:
            return True
        return False
    except Exception as e:
        print(e)
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# ПОЛУЧАЕМ СПИСОК ЗАКАЗОВ
def order_list(user_id: int):
    conn = sqlite3.connect('pizza_order.db')
    cursor = conn.cursor()
    try:
        cursor.execute("""
                   SELECT id,user_id,size,type,quantity, address, order_date, status
                   FROM orders 
                   WHERE user_id = ?
                   ORDER BY order_date DESC
                   """,(user_id,))
        orders = cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        return orders
    

# ОБНОВЛЕНИЕ ЗАКАЗА
def update_order(order_id: int, new_status: str):
    try:
        db = sqlite3.connect('pizza_order.db')
        cursor = db.cursor()

        print(f"🔍 DEBUG: Обновляем заказ {order_id} на статус '{new_status}'")     

        cursor.execute("""
        UPDATE orders SET status = ? WHERE id = ?
        """, (new_status, order_id))
        db.commit()
        rows_updated = cursor.rowcount

        print(f"🔍 DEBUG: Обновлено строк: {rows_updated}")

        return rows_updated > 0 # T F
    
    except Exception as e:
        print(f"❌ Ошибка обновления заказа: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


#ДЛЯ ПРОВЕРОК
def check_data():
    conn = sqlite3.connect('pizza_order.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    orders1 = cursor.fetchall()
    for order in orders1:
        print(order)
    conn.close()

#ПОЛУЧАЕМ ОДИН ЗАКАЗ
def get_1_order(id):
    try:
        db = sqlite3.connect('pizza_order.db')
        cursor = db.cursor()
        cursor.execute("SELECT user_id,size,type,quantity,address,phone,order_date FROM orders WHERE id = ?",(id,))
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
#ПОЛУЧАЕМ ВСЕ ЗАКАЗЫ
def get_all_orders():
    try:
        db = sqlite3.connect('pizza_order.db')
        cursor = db.cursor()
        orders = {}
        cursor.execute("SELECT id,user_id,size,type,quantity,address,phone,order_date FROM orders WHERE status = 'new'")
        orders['new'] = cursor.fetchall()
        cursor.execute("SELECT id,user_id,size,type,quantity,address,phone,order_date FROM orders WHERE status = 'cooking'")
        orders['cooking'] = cursor.fetchall()
        cursor.execute("SELECT id,user_id,size,type,quantity,address,phone,order_date FROM orders WHERE status = 'ready'")
        orders['ready'] = cursor.fetchall()
        cursor.execute("SELECT id,user_id,size,type,quantity,address,phone,order_date FROM orders WHERE status = 'inRoad'")
        orders['inRoad'] = cursor.fetchall()
        cursor.execute("SELECT id,user_id,size,type,quantity,address,phone,order_date FROM orders WHERE status = 'deliver' AND DATE(order_date) = DATE('now')")
        orders['deliver'] = cursor.fetchall()
        return orders
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


#БЕРЕМ ОТЗЫВЫ
async def get_callback():
    try:
        db = sqlite3.connect('dp.db')
        cursor = db.cursor()
        cursor.execute("SELECT id,user_id,text,date FROM callback")
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

#ВСТАВЛЯЕМ ОТЗЫВ В БД
async def input_callback(user_id,text):
    try:
        db = sqlite3.connect('dp.db')
        cursor = db.cursor()
        cursor.execute("""
                       INSERT INTO callback
                       (user_id,text) 
                       VALUES (?,?)""",(user_id,text))
        db.commit()
        if cursor.rowcount > 0:
            return True
        return False
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


#БЕРЕМ ЗАКАЗЫ КЛИЕНТА
async def get_unDeliv_orders_user(user_id):
    try:
        db = sqlite3.connect('pizza_order.db')
        cursor = db.cursor()
        cursor.execute("""SELECT id,size,type,quantity,address,phone,order_date,status 
                       FROM orders 
                       WHERE user_id = ?
                       ORDER BY order_date DESC
                       LIMIT 5""",(user_id,))
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

#БЕРЕМ ДОСТАВЛЕНЫЕ ЗАКАЗЫ
async def get_deliver_orders():
    try:
        db = sqlite3.connect('pizza_order.db')
        cursor = db.cursor()
        cursor.execute("SELECT id,user_id,size,type,quantity,address,phone,order_date FROM orders WHERE status = 'deliver'")
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

#БЕРЕМ СТАТИСТИКУ
def get_pizza_stats():
    db = sqlite3.connect('pizza_order.db')
    cursor = db.cursor()
    stats = {} # "листок" для записей (словарь stats)

    cursor.execute("SELECT COUNT(*) FROM orders") #COUNT(*) - "посчитать все" 
    stats['total_orders'] = cursor.fetchone()[0] #fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT user_id) FROM orders") # DISTINCT user_id - "уникальные юзер айди" (исключает повторения)
                                                                 # COUNT(DISTINCT user_id) - "посчитать уникальных пользователей"
    stats['unique_users'] = cursor.fetchone()[0]

    cursor.execute("""
                   SELECT type, COUNT(*) as count
                   FROM orders
                   GROUP BY type
                   ORDER BY count DESC
                   LIMIT 3
                   """)
    stats['popular_pizzas'] = cursor.fetchall()

    cursor.execute("""
                   SELECT COUNT(*)
                   FROM orders
                   WHERE DATE(order_date) = DATE('now')
                   """)
    stats['today_orders'] = cursor.fetchone()[0]

    db.close
    return stats