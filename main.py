from email import message
import os
import telebot
import schedule
from telebot import types
from flask import Flask, request


TOKEN = '5496930108:AAGNV22359NcshQ2CJSngqz0Rd3fmjJyMmM'
APP_URL = f'https://detective-1.herokuapp.com/{TOKEN}'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    menu_but = types.ReplyKeyboardMarkup(resize_keyboard=True)
    first = types.KeyboardButton("Qahvaxonadagi qotillik")
    second = types.KeyboardButton("Bo`yalgan qo`g`irchoqlar")
    three = types.KeyboardButton("*Bo'sh*")
    menu_but.add(first, second, three)
    bot.send_message(message.chat.id, f"Salom, detektiv {message.from_user.first_name}. Ishlar ko'payib ketgan. Xo'sh, qay biridan boshlaymiz?", reply_markup=menu_but)

@bot.message_handler()
def menu_answer(message):
    if message.text == "Qahvaxonadagi qotillik":
        bot.send_message(message.chat.id, f"Hali tayyormas🤔")
    elif message.text == "*Bo'sh*":
        bot.send_message(message.chat.id, f"Hali tayyormas🤔")
    elif message.text == "Bo`yalgan qo`g`irchoqlar":
        doll_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        police = types.KeyboardButton("Politsiya mahkamasi")
        dalil = types.KeyboardButton("Dalillar ombori")
        ekspertiza = types.KeyboardButton("Ekspertiza")
        bank = types.KeyboardButton("Markaziy Bank")
        qahvaxona = types.KeyboardButton("'Morning' qahvaxona")
        kinoteatr = types.KeyboardButton("Kinoteatr")
        goodlife = types.KeyboardButton("'Good life' savdo markazi")
        doll_menu.add(police, dalil, ekspertiza, bank, qahvaxona, kinoteatr, goodlife)
        bot.send_photo(message.chat.id, photo=open("images/doll_blood.jpeg", 'rb'), caption= 'Its work?', reply_markup=doll_menu)
        # bot.send_photo(message.chat.id, photo=open("/images/police.jpg", 'rb'), caption= "PostMail' xabar beryapti:\nPolitsiya hali hamon 'bo`yoqchi'ni tutolmadi. Detektivlar esa manzillar orasidagi bog`liqlikni topisholmayapti. 3 kunichida 'Goodlife' savdo markazi va uning oldidagi kinoteatrning orqa devoridan yana bitta 'qurbon' topildi. Jurnalistlarning turli savollariga politsiya qisqagina javob berdi:<<Hozircha aniq tafsilotlarimiz yo`q, lekin detektivlarimiz qo`g`irchoqlar faqat orqa devorlardan topilayotganini aniqlashdi. Ekspertiza xulosalarini esa oshkor qilish niyatimiz yo`q!>>\nBu holat aholi o`rtasida vahima uyg'otmoqda. Umid qilamizki shahar detektivi 'bo`yoqchi'ni qo`lga oladi... ")












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