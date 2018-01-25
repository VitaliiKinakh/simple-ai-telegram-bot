import telebot
from googletrans import Translator
import apiai
import json


# Set bot token
bot = telebot.TeleBot("<token>")

# Set translator
translator = Translator()

#

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Здарова бандіти! ' +
                     'Якщо Вам вам хочеться повіситись або вскритись, то я найкраще вирішення вашої проблеми. ' +
                     'Поговорю з вами по душах, почешу язиками про бабу і просто скажу пару добрих слів.' +
                     'Пиши бро, не соромся. Тут всі свої!')


@bot.message_handler()
def answer(message):
    request = apiai.ApiAI('<token>').text_request()  # Dialogflow access token
    # Detect language of message
    try:
        lang = translator.detect(message.text).lang
        # Translate text into english
        english_text = translator.translate(message.text)
        # Make a request to Dialogflow
        request.lang = 'en'  # request language
        request.session_id = 'BoringBot'
        request.query = english_text.text
        responseJson = json.loads(request.getresponse().read().decode('utf-8'))
        response = responseJson['result']['fulfillment']['speech']
        if response:
            # Translate into language of message
            translated_response = translator.translate(response, dest=lang)
            bot.send_message(message.chat.id, translated_response.text)
        else:
            error_message = "I do not understand you"
            translated_error_message= translator.translate(error_message,dest=lang)
            bot.send_message(message.chat.id, translated_error_message.text)
    except Exception:
        bot.send_message(message.chat.id, "Щось я хреново себе почуваю! Давай завтра поговоримо!")


bot.polling()




