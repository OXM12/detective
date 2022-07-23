from email import message
import os
from subprocess import call
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
    menu_but = types.InlineKeyboardMarkup(row_width=1)
    first = types.InlineKeyboardButton("Qahvaxonadagi qotillik", callback_data="qahvaxona")
    second = types.InlineKeyboardButton("Bo`yalgan qo`g`irchoqlar", callback_data="qogirchoq")
    three = types.InlineKeyboardButton("*Bo'sh*", callback_data="teatr")
    menu_but.add(first, second, three)
    bot.send_message(message.chat.id, f"Salom, detektiv {message.from_user.first_name}. Ishlar ko'payib ketgan. Xo'sh, qay biridan boshlaymiz?", reply_markup=menu_but)

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
                qahvaxona = types.InlineKeyboardButton("'Morning' qahvaxona", callback_data="qahvaxona")
                kinoteatr = types.InlineKeyboardButton("Kinoteatr", callback_data="kinoteatr")
                goodlife = types.InlineKeyboardButton("'Good life' savdo markazi", callback_data="goodlife")
                doll_menu.add(police, dalil, ekspertiza, bank, qahvaxona, kinoteatr, goodlife)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text = "'PostMail' jurnali xabar bermoqda:\n1 haftadan buyon shahar binolarining orqa tarafidan qismlarga ajratib tashlanib, qizil rangga bo'yalgan qo'g'irchoqlar topilmoqda. Bu haftaning o'zida Markaziy bank va 'Morning' qahvaxonasining orqa devoridan topildi. Politsiya 'bo'yoqchi'ni topishga harakat qilmoqda.")
                bot.send_message(chat_id=call.message.chat.id, message_id=call.message.id, text = "'PostMail' xabar beryapti:\nPolitsiya hali hamon 'bo`yoqchi'ni tutolmadi. Detektivlar esa manzillar orasidagi bog`liqlikni topisholmayapti. 3 kunichida 'Goodlife' savdo markazi va uning oldidagi kinoteatrning orqa devoridan yana bitta 'qurbon' topildi. Jurnalistlarning turli savollariga politsiya qisqagina javob berdi:<<Hozircha aniq tafsilotlarimiz yo`q, lekin detektivlarimiz qo`g`irchoqlar faqat orqa devorlardan topilayotganini aniqlashdi. Ekspertiza xulosalarini esa oshkor qilish niyatimiz yo`q!>>\nBu holat aholi o`rtasida vahima uyg'otmoqda. Umid qilamizki shahar detektivi 'bo`yoqchi'ni qo`lga oladi... ", reply_markup=doll_menu)












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