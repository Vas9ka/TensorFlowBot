import telebot
import neuralnetwork
import os
import user
from telebot import types
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from flask import Flask, request
picture_URL = ""
style_URL = ""
TOKEN = '1354173088:AAHaseJVed9YIM4VkFW6znKVA8swPoldpWU'
bot = telebot.TeleBot('1354173088:AAHaseJVed9YIM4VkFW6znKVA8swPoldpWU')
server = Flask(__name__) 
users = {}
markup = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('Отправить фотографию')
itembtn2 = types.KeyboardButton('Отправить стиль')
markup.add(itembtn1,itembtn2)
markup_photo = types.ReplyKeyboardMarkup(row_width=1)
markup_photo.add(itembtn1)
markup_style = types.ReplyKeyboardMarkup(row_width=1)
markup_style.add(itembtn2)
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Этот бот умеет смешивать две картинки так, что первая будет выглядеть в стиле второй',reply_markup=markup)

@bot.message_handler(content_types = ['text'])
def handle_text(message):
    if not users.get(message.chat.id):
        user_ = user.User()
        users[message.chat.id] = user_
    else:
        if(message.text == "Отправить фотографию"):
            users[message.chat.id].is_photo = True
            users[message.chat.id].is_style = False
            bot.send_message(message.chat.id,"Пришли фотографию")
        elif(message.text == "Отправить стиль"):
            users[message.chat.id].is_style = True
            if users[message.chat.id].photo_url == "":
                users[message.chat.id].is_photo = False
            bot.send_message(message.chat.id,"Пришли стиль")
        else:
            bot.send_message(message.chat.id,'Выбери, что прислать первым: фотографию или стиль',reply_markup = markup)
@bot.message_handler(content_types= ['photo'])
def handle_photo(message):
    global users
    if users.get(message.chat.id):
        if users[message.chat.id].is_photo:
            id = message.photo[-1].file_id
            picture_URL = bot.get_file_url(id)
            users[message.chat.id].photo_url = picture_URL
            users[message.chat.id].is_photo = False
            if users[message.chat.id].style_url == "":
                bot.send_message(message.chat.id,"Отлично! Теперь нажми на Отправить стиль",reply_markup = markup_style)
        if users[message.chat.id].is_style:
            id = message.photo[-1].file_id
            style_URL = bot.get_file_url(id)
            users[message.chat.id].style_url = style_URL
            if users[message.chat.id].photo_url == "":
                bot.send_message(message.chat.id,"Отлично! Теперь нажми на Отправить фотографию",reply_markup= markup_photo)
            users[message.chat.id].is_style = False
        if users[message.chat.id].photo_url != "" and users[message.chat.id].style_url != "":
            bot.send_message(message.chat.id,"Фотография и стиль получены, теперь надо немного потерпеть...")
            print(users[message.chat.id].photo_url)
            print(users[message.chat.id].style_url)
            neuralnetwork.save_image(users[message.chat.id].photo_url,users[message.chat.id].style_url)
            photo = open('photo.png','rb')
            bot.send_photo(message.chat.id,photo)
            photo.close()
            users[message.chat.id].is_photo = False
            users[message.chat.id].is_style = False
            users[message.chat.id].photo_url = ""
            users[message.chat.id].style_url = ""
            os.remove("photo.png")

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://tensorflowbot.herokuapp.com/' + TOKEN)
    return "!", 200

if __name__ == '__main__':
    server.debug = True
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))