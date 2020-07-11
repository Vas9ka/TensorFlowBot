import telebot
import neuralnetwork
import os
from flask import Flask, request
picture_URL = ""
style_URL = ""
TOKEN = '1354173088:AAHaseJVed9YIM4VkFW6znKVA8swPoldpWU'
bot = telebot.TeleBot('1354173088:AAHaseJVed9YIM4VkFW6znKVA8swPoldpWU')
server = Flask(__name__) 
counter = 0
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
    global counter
    global style_URL
    global picture_URL
    counter += 1 
    fileID = message.photo[-1].file_id
    if(counter == 1):
        picture_URL = bot.get_file_url(fileID)
        print(picture_URL)
    if(counter == 2):
        style_URL = bot.get_file_url(fileID)
        print(style_URL)
        counter = 0
        neuralnetwork.save_image(picture_URL,style_URL)
        photo = open('img.png','rb')
        bot.send_photo(message.chat.id,photo)



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
