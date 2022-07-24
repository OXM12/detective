from email import message
import os
import sqlite3
from subprocess import call
from unittest import result
import telebot
import psycopg2
import config
import logging
from config import *
import schedule
from telebot import types
from flask import Flask, request



bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
logger = telebot.logger
logger.setLevel(logging.DEBUG)

db_connection = psycopg2.connect(DB_URI, sslmode="require")
db_object = db_connection.cursor

@bot.message_handler(commands=['start'])
def start(message):
    id = message.from_user.id
    username = message.from_user.username 
    db_object.execute(f"SELECT id FROM users WHERE id = {id}")
    result = db_object.fetchone()
    
    if not result:
        db_object.execute("INSERT INTO users(id, username, messages) VALUES (%s, %s, %s)"), (id, username, 0)
        db_connection.commit()
    menu_but = types.InlineKeyboardMarkup(row_width=1)
    first = types.InlineKeyboardButton("Qahvaxonadagi qotillik", callback_data="qahvaxona")
    second = types.InlineKeyboardButton("Bo`yalgan qo`g`irchoqlar", callback_data="qogirchoq")
    three = types.InlineKeyboardButton("*Bo'sh*", callback_data="teatr")
    menu_but.add(first, second, three)
    bot.send_photo(message.chat.id, photo=open("./images/detective.jpg", 'rb'), caption = f"Salom, detektiv {message.from_user.first_name}. Ishlar ko'payib ketgan. Xo'sh, qay biridan boshlaymiz?", reply_markup=menu_but)

    
@bot.callback_query_handler(func=lambda call:True)
def menu_answer(call):
    if call.message:
        if call.data == "qahvaxona":
            bot.send_message(message.chat.id, f"Hali tayyormas🤔")
        elif call.data == "teatr":
            bot.send_message(message.chat.id, f"Hali tayyormas🤔")
        elif call.data == "qogirchoq":
            with open('./images/doll_blood.jpeg', 'rb') as f1:
                doll_menu = types.InlineKeyboardMarkup(row_width=2)
                police = types.InlineKeyboardButton("Politsiya mahkamasi", callback_data="police")
                dalil = types.InlineKeyboardButton("Dalillar ombori", callback_data="dalil")
                ekspertiza = types.InlineKeyboardButton("Ekspertiza", callback_data="ekspertiza")
                bank = types.InlineKeyboardButton("Markaziy Bank", callback_data="bank")
                qahvaxona = types.InlineKeyboardButton("'Morning' qahvaxona", callback_data="qahva")
                kinoteatr = types.InlineKeyboardButton("Kinoteatr", callback_data="kinoteatr")
                goodlife = types.InlineKeyboardButton("'Good life' savdo markazi", callback_data="goodlife")
                doll_menu.add(police, dalil, ekspertiza, bank, qahvaxona, kinoteatr, goodlife)
                bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.id, caption="'PostMail' jurnali xabar bermoqda:\n1 haftadan buyon shahar binolarining orqa tarafidan qismlarga ajratib tashlanib, qizil rangga bo'yalgan qo'g'irchoqlar topilmoqda. Bu haftaning o'zida Markaziy bank va 'Morning' qahvaxonasining orqa devoridan topildi. Politsiya 'bo'yoqchi'ni topishga harakat qilmoqda.")












@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return '!', 200


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))