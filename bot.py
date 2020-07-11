import telebot
import neuralnetwork
import os
from flask import Flask, request
picture_URL = ""
style_URL = ""
TOKEN = '1354173088:AAHaseJVed9YIM4VkFW6znKVA8swPoldpWU'
bot = telebot.TeleBot('1354173088:AAHaseJVed9YIM4VkFW6znKVA8swPoldpWU')
user_photos = {}
server = Flask(__name__) 
@bot.message_handler(commands=['start']) 
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Этот бот умеет смешивать две картинки так, что первая будет выглядеть в стиле второй.Для дополнительной информации напиши /help')

@bot.message_handler(commands=['help']) 
def help_message(message):
    bot.send_message(message.chat.id,
    '1. Пришли боту картинку, которую нужно обработать.\n' +
    '2. Пришли боту картинку, в стиле которой нужно обработать первую')

@bot.message_handler(content_types= ['photo'])
def handle_photo(message):
    global user_photos
    global picture_URL
    global style_URL
    if not user_photos.get(message.chat.id):
        user_photos[message.chat.id] = [1]
        id = message.photo[-1].file_id
        picture_URL = bot.get_file_url(id)
        user_photos[message.chat.id].append(picture_URL)
    else:
        user_photos[message.chat.id][0] += 1
    if user_photos[message.chat.id][0] == 2:
        id = message.photo[-1].file_id
        style_URL = bot.get_file_url(id)
        user_photos[message.chat.id].append(style_URL)
        print(user_photos)
        bot.send_photo(message.chat.id,neuralnetwork.save_image(user_photos[message.chat.id][1],user_photos[message.chat.id][2]))
        user_photos[message.chat.id].clear()

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://tensorflowbot.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))