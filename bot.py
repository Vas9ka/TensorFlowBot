import telebot
import neuralnetwork
picture_URL = ""
style_URL = ""
bot = telebot.TeleBot('1376136022:AAHhUQo_rcGMqI7QeJrzwNsm0hwNt4w4vXc') 
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



bot.polling(none_stop= True,interval= 0)