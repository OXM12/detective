from email import message
import os
from colorama import Cursor
import telebot
import schedule
from telebot import types
from flask import Flask, request
from threading import Thread
from datetime import datetime
import time
import sqlite3

TOKEN = '5496930108:AAGNV22359NcshQ2CJSngqz0Rd3fmjJyMmM'
APP_URL = f'https://detective-1.herokuapp.com/{TOKEN}'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    
    cursor.execute("""CREATE TABLE IF NOT EXIST user_id(
        id INTEGER 
        )""")
    
    connect.commit()
    
    users_id = [message.chat.id]
    cursor.execute("INSERT INTO user_id VALUES(?);", users_id)
    connect.commit()
    
    menu_but = types.ReplyKeyboardMarkup(resize_keyboard=True)
    first = types.KeyboardButton("Qahvaxonadagi qotillik")
    second = types.KeyboardButton("*Bo'sh*")
    three = types.KeyboardButton("*Bo'sh*")
    menu_but.add(first, second, three)
    bot.send_message(message.chat.id, f"Salom, detektiv {message.from_user.first_name}. Ishlar ko'payib ketgan. Xo'sh, qay biridan boshlaymiz?", reply_markup=menu_but)

@bot.message_handler()
def menu_answer(message):
    if message.text == "Qahvaxonadagi qotillik":
        bot.send_message(message.chat.id, f"Hali tayyormas🤔")
    elif message.text == "*Bo'sh*":
        bot.send_message(message.chat.id, f"Hali tayyormas🤔")






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