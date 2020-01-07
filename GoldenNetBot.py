# -*- coding: utf-8 -*-
import telebot
from telebot import types
import time
from datetime import datetime
import logging
import pymysql.cursors
import pymysql
from pymysql import *
from pymysql.cursors import DictCursor
import sys
import requests
import json

reload(sys)
sys.setdefaultencoding('utf8')
to_chat_id = ''
bot_token = ''
bot = telebot.TeleBot(token=bot_token, threaded=False)
t = datetime.now().strftime("%m/%d/%Y, %H:%M")
logging.basicConfig(filename='/tmp/SupportBot.log', level=logging.INFO)

menu1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
btn = types.KeyboardButton(text="Поділитися номером телефону", request_contact=True)
menu1.add(btn)

menu2 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
btn1 = types.KeyboardButton("\xF0\x9F\x92\xB0 Стан Рахунку")
btn2 = types.KeyboardButton("\xF0\x9F\x92\xB5 Оплата")
btn3 = types.KeyboardButton("\xF0\x9F\x93\xB2 Зворотній дзвінок")
btn4 = types.KeyboardButton("\xF0\x9F\x92\xAC Чат з оператором")
btn5 = types.KeyboardButton("\xF0\x9F\x93\x8C Особистий кабінет")
btn6 = types.KeyboardButton("\xF0\x9F\x92\xB3 Кредитний період")
btn7 = types.KeyboardButton("\xF0\x9F\x92\xAF Мої Платежі")
menu2.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)

menu3 = types.InlineKeyboardMarkup()
btn8 = types.InlineKeyboardButton(text="\xF0\x9F\x92\xAC Чат з оператором",
                                  url='https://t.me/joinchat/EH6LtRbpTpMkHSa74wHAtg')
menu3.add(btn8)

menu4 = types.InlineKeyboardMarkup()
btn9 = types.InlineKeyboardButton("\xF0\x9F\x8F\xA0 Особистий кабінет", url='https://my.golden.net.ua/autorize.php')
menu4.add(btn9)

menu5 = types.InlineKeyboardMarkup()
btn10 = types.InlineKeyboardButton("EasyPay", url='https://easypay.ua/ua/catalog/internet/golden-net')
btn11 = types.InlineKeyboardButton("City24", url='https://city24.ua/Internet/GOLDEN-NET')
btn12 = types.InlineKeyboardButton("2Click", url='https://2click.money/')
btn13 = types.InlineKeyboardButton("Ligpay", url='https://www.liqpay.ua/ru/checkout/card/i33203403568')
menu5.add(btn10, btn11, btn12, btn13)

menu7 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
btn14 = types.KeyboardButton("\xF0\x9F\x92\xB3 Активувати період")
btn15 = types.KeyboardButton("\xF0\x9F\x93\x9D Головне меню")
menu7.add(btn14, btn15)

conn = (pymysql.connect(host='',
                        user='',
                        password='',
                        database='',
                        charset='utf8'))
cursor = conn.cursor()


@bot.message_handler(commands=['start'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.chat.id,
                         "Для отримання даних за договором мені необхідний Ваш номер телефону прив'язаний до договору",
                         reply_markup=menu1)
        logging.info('script info run :' + 'send :' + str(message.chat.id) + ' ' + str(t))


@bot.message_handler(func=lambda message: True, content_types=['text'])
def bill(message):
    if message.text == '\xF0\x9F\x92\xB3 Кредитний період':
        time.sleep(2)
        bot.send_message(message.chat.id, 'Активувати період', reply_markup=menu7)

    elif message.text == '\xF0\x9F\x93\x9D Головне меню':
        time.sleep(2)
        bot.send_message(message.chat.id, '\xF0\x9F\x93\x9D Головне меню', reply_markup=menu2)

    elif message.text == '\xF0\x9F\x92\xAC Чат з оператором':
        time.sleep(2)
        bot.send_photo(message.chat.id,
                       'https://cdn.pixabay.com/photo/2016/11/22/06/32/girl-1848478_960_720.jpg',
                       '\xF0\x9F\x92\xAC Натисніть щоб перейти в чат', reply_markup=menu3)

    elif message.text == '\xF0\x9F\x93\x8C Особистий кабінет':
        time.sleep(2)
        bot.send_photo(message.chat.id,
                       'https://cdn.pixabay.com/photo/2016/11/29/06/18/home-office-1867761_960_720.jpg',
                       '\xF0\x9F\x92\xAC Натисніть щоб перейти в особистий кабінет', reply_markup=menu4)

    elif message.text == '\xF0\x9F\x92\xB5 Оплата':
        time.sleep(2)
        bot.send_photo(message.chat.id,
                       'https://cdn.pixabay.com/photo/2016/05/31/20/39/online-marketing-1427787_960_720.jpg',
                       reply_markup=menu5)

    elif message.text == '\xF0\x9F\x92\xB3 Активувати період':
        cursor.execute('''
                                                SELECT
                                                agreement
                                                FROM
                                                clients
                                                WHERE
                                                telegram_chat_id = %s;''', (message.chat.id))
        for money in cursor:
            URL = 'http://172.1.2.254/creditPeriod/enableWithDefrost?agreement=' + str(money[0])
            PARAMS = 'employee=31'
            credit = requests.get(url=URL, params=PARAMS)
            credit.json()
            time.sleep(2)
            bot.send_photo(message.chat.id,
                           'https://cdn.pixabay.com/photo/2016/01/29/09/57/hands-1167618_960_720.jpg',
                           '''Послуга активована  кредитний період дозволяє користуватись  послугою впродовж  4 днів при негативному балансі''')
            logging.info('user :' + str(money[0]) + ' ' + 'activate credit ' + ' ' + str(t))

    elif message.text == '\xF0\x9F\x93\xB2 Зворотній дзвінок':
        cursor.execute('''
                            SELECT
                            agreement, phone
                            FROM
                            clients
                            WHERE
                            telegram_chat_id = %s;''', (message.chat.id))
        for call in cursor:
            time.sleep(2)
            bot.send_photo(to_chat_id,
                           'https://cdn.pixabay.com/photo/2014/08/05/10/27/iphone-410311_960_720.jpg',
                           'Абонент: '
                           + str(call[0]) + '\n' + 'замовив зворотній дзвінок за номером: \n' + call[1])
            bot.send_photo(message.chat.id,
                           'https://cdn.pixabay.com/photo/2017/11/12/22/49/call-center-2944063_960_720.jpg',
                           'Очікуйте на дзвінок')

    elif message.text == '\xF0\x9F\x92\xB0 Стан Рахунку':
        cursor.execute(''' 
                            SELECT c.agreement, bill_prices.`name`,  c.balance, c.phone, CONCAT(ac.name,', ', s.name, ', ', ah.name, ', кв. ', c.apartment) address , c.telegram_chat_id
                            FROM clients c
                            JOIN addr_houses ah on ah.id = c.house
                            JOIN addr_streets s on s.id = ah.street
                            JOIN addr_cities ac on ac.id = s.city
                            JOIN client_prices on client_prices.agreement=c.id
                            JOIN bill_prices on bill_prices.id=client_prices.price
                            WHERE c.telegram_chat_id=%s ORDER BY client_prices.id DESC LIMIT 1 ''', (message.chat.id))
        for balance in cursor:
            bal = 'Договір: ' + str(balance[0]) + '\nАдреса: ' + str(balance[4]) + '\nТариф: ' + str(
                balance[1]) + '\nБаланс: ' + str(balance[2]) + '.грн'
            time.sleep(2)
            bot.send_photo(message.chat.id,
                           'https://cdn.pixabay.com/photo/2015/10/31/21/31/bookkeeper-1016299_960_720.jpg', bal)


    elif message.text == '\xF0\x9F\x92\xAF Мої Платежі':
        cursor.execute(''' 
                                     SELECT p.money, cast(time as date) time, p.comment, p.payment_type  FROM paymants p
                                     JOIN clients c on p.agreement = c.id
                                     WHERE c.telegram_chat_id= %s order by time desc limit 15;''', (message.chat.id))

        logging.info('user :' + str(message.chat.id) + 'select payments' + ' ' + str(t))
        for payment in cursor:
            pay = 'Сума :' + str(payment[0]) + '\nДата :' + str(payment[1]) + '\nДжерело :' + str(payment[2])
            time.sleep(2)
            bot.send_message(message.chat.id, pay)


    elif message.text == 'users':
        cursor.execute(''' SELECT COUNT(id) FROM clients WHERE telegram_chat_id > 1''')

        for user in cursor:
            users = 'Ботом користуеться :' + str(user[0]) + ' абонентів'
            time.sleep(2)
            bot.send_message(message.chat.id, users)


    elif message.text == 'pay':
        cursor.execute(''' SELECT ci.name name, sum(money)  sum
                           FROM paymants p
                           JOIN clients c on p.agreement = c.id
                           JOIN addr_houses h on h.id = c.house
                           JOIN addr_streets st  on st.id = h.street
                           JOIN addr_cities ci on ci.id = st.city
                           LEFT JOIN addr_groups gr on gr.id = h.group_id
                           WHERE  cast(p.time as date) = cast(NOW() as date)
                           GROUP BY ci.name
                           ORDER BY 1''')

        for pay in cursor:
            pays = 'Територія :' + str(pay[0]) + ' | ' + '\nСума :' + str(pay[1])
            time.sleep(2)
            bot.send_message(message.chat.id, pays)





    elif message.text:

        tel = str(message.text[-9:])
        logging.info('master :' + str(message.chat.id) + 'send phone' + ' ' + str(t))
        cursor.execute('''SELECT  q.created ,e.`name` created_employee ,q.reason ,s.agreement
               ,CONCAT('г.',c.name,', ', st.name, ', д.', h.`name`, ', под.',s.entrance, ', кв.', s.apartment) addr
               ,q.phone ,q.`comment`  ,q.dest_time ,re.name responsible_employee ,e.phone
               FROM questions_full q  JOIN clients s on q.agreement = s.id
               JOIN addr_houses h on h.id = s.house JOIN addr_streets st on st.id = h.street
               JOIN addr_cities c on c.id = st.city LEFT JOIN employees e on e.id = q.created_employee
               LEFT JOIN employees e2 on e2.id = q.reported_employee
               LEFT JOIN employees re on re.id = q.responsible_employee
               WHERE cast(q.dest_time as date) = cast(NOW() as date) AND re.phone LIKE %s ORDER BY dest_time ''',
                       ('%' + tel))
        logging.info('master :' + str(message.chat.id) + ' select task' + ' ' + str(t))
        time.sleep(2)
        for data in cursor:
            a = 'Создана:  ' + data[0].strftime("%m/%d/%Y, %H:%M:%S") + '\n' + 'Создатель:  ' + data[
                1] + '\n' + 'Причина:  ' + data[2] + '\n' + 'Договор:  ' + str(data[3]) + \
                '\n' + 'Адрес:  ' + data[4] + '\n' + 'Телефон:  ' + data[5] + '\n' + 'Комментарий:  ' + data[
                    6] + '\n' + 'На Когда:  ' + data[7].strftime("%m/%d/%Y, %H:%M:%S") + \
                '\n' + 'Исполнитель:  ' + str(data[8])
            bot.send_message(message.chat.id, a)


@bot.message_handler(content_types=['contact'])
def menu(message):
    phone = str(message.contact.phone_number[-9:])
    logging.info('user send phone :' + phone + ' ' + 'send :' + str(message.chat.id) + ' ' + str(t))

    try:
        row = cursor.execute('''
            SELECT  c.phone ,c.telegram_chat_id
            FROM clients c
            WHERE c.phone LIKE %s   LIMIT 1 ''', ('%' + phone))

    except Exception as e:
        # if the connection was lost, then it reconnects
        connect.ping(reconnect=True)
        logging.debug(' debug info :' + str(e) + ' ' + str(t))

        row = cursor.execute('''
                    SELECT  c.phone ,c.telegram_chat_id
                    FROM clients c
                    WHERE c.phone LIKE %s   LIMIT 1 ''', ('%' + phone))

    if row > 0:
        cursor.execute("UPDATE clients SET telegram_chat_id=%s WHERE clients.phone LIKE %s",
                       (+ message.chat.id, '%' + phone))
        conn.commit()
        bill(message)
        logging.info('script find phone and save user_id to database:' + ' ' + phone + ' ' + str(t))
        bot.send_message(message.chat.id, 'Вас вітає ГолденБотік', reply_markup=menu2)

    else:
        time.sleep(2)
        bot.send_photo(message.chat.id, 'https://cdn.pixabay.com/photo/2017/03/09/12/31/error-2129569_960_720.jpg',
                       'Номер не закріплено за договором')
        logging.info('user :' + str(message.chat.id) + 'not found in database ' + ' ' + str(t))


if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.debug(' debug info :' + str(e) + ' ' + str(t))
            # или просто print(e) если у вас логгера нет,
            # или import traceback; traceback.print_exc() для печати полной инфы
            time.sleep(15)

