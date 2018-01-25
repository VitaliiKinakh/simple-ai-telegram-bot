import telebot
from googletrans import Translator
import apiai
import json
import random

# Set bot token
bot = telebot.TeleBot("466884027:AAEbXLMoJOxOKcDh4OvxhSRh6pXzziUYHVY")

# Set translator
translator = Translator()

# Error messages
error_messages = [
    "Щось я себе хренево почуваю. Давай ще щось пиши",
    "Я не розумію тебе. Пиши нормально",
    "Що ти як пес. Будь людиною!",
    "Впав, братан!",
    "А знаєш, в мене були і цікавіші співрозмовники",
    "Гав - гав",
    "Що ти як методичка Гнатіва - нічого не понятно",
    "Ще раз таке повториться, я напишу твоїй мамі",
    "Зрозуміліше будь ласка",
    "Нормально ж спілкувалися, ну шо ти починаєш",
    "Думаєш написав якийсь рандомний текст і я його зрозумію",
    "Щасливої дороги!",
    "Але ти пиріжок!",
    "Відповіді нема, але ти тримайся!",
    "Але ти орігинальна!",
    "Мавпи і то зрозуміліше пишуть",
    "А бодай би тя шляк трафив",
    "В нас на районі на таке вбивають",
    "Я пішов слухати Pink Floyd",
    "Зрооозуміліше",
    "Будь ласка, пиши зрозуміло",
    "Ваш абонент знаходиться поза зоною досяжності",
    "Лол кек чебурек",
    "А якби я так писав?",
    "Ти пяний - йди спати!",
    "Завтра поговоримо!"
]

# Some standart answers
standart_answers = {
    "слава україні" : "Героям слава!",
    "слава нації" : "Смерть ворогам",
    "україна" : "Понад усе!",
    "гав" : "Гав"
}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Здарова бандіти! ' +
                     'Якщо Вам вам хочеться повіситись або вскритись, то я найкраще вирішення вашої проблеми. ' +
                     'Поговорю з вами по душах, почешу язиками про бабу і просто скажу пару добрих слів.' +
                     'Пиши бро, не соромся. Тут всі свої!')


@bot.message_handler()
def answer(message):
    request = apiai.ApiAI('559a5401a1ab471ea756ff7cbc4fee09').text_request()  # Dialogflow access token
    # Detect language of message
    try:
        # Check for standart answers
        mess = message.text.lower()
        if mess in standart_answers.keys():
            bot.send_message(message.chat.id, standart_answers[message.text])
        else:
            # Translate text into russian
            english_text = translator.translate(mess, dest="en")
            # Make a request to Dialogflow
            request.lang = 'en'  # request language
            request.session_id = 'BoringBot'
            request.query = english_text.text
            responseJson = json.loads(request.getresponse().read().decode('utf-8'))
            response = responseJson['result']['fulfillment']['speech']
            if response:
                # Translate into language of message
                translated_response = translator.translate(response, dest="uk")
                bot.send_message(message.chat.id, translated_response.text)
            else:
                bot.send_message(message.chat.id, error_messages[random.randint(0, len(error_messages) - 1)])
    except Exception as e:
        print(str(e))
        bot.send_message(message.chat.id, error_messages[random.randint(0, len(error_messages) - 1)])


bot.polling()




