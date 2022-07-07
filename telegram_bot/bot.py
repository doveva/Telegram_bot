import telebot

from Parser.parser import loader
import requests
import json


def start_bot():
    bot = telebot.TeleBot("5423385740:AAGuMrCVdaKhwxi6uFMrohHhyy2DvXVD5f8")

    @bot.message_handler(content_types=['text'])
    def text_handler(message):
        if message.text == "/updateDB":
            url = "https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D1%81%D0%BA%D0%B8%D0%B5_%D0%BD%D0%B0%D1%81%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D1%8B%D0%B5_%D0%BF%D1%83%D0%BD%D0%BA%D1%82%D1%8B_%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%B9_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D0%B8"
            data = loader(url)
            db_url_post = "http://localhost:8000/api/data/"
            requests.post(db_url_post, json=json.dumps(data, ensure_ascii=False))
            bot.send_message(message.from_user.id, "База успешно обновлена")

        elif message.text == "/help":
            bot.send_message(message.from_user.id, "Есть команда /updateDB для обновления базы данных или можно "
                                                   "ввести название города в Москве, тогда я попробую найти его в базе")
        elif message.text == "/start":
            bot.send_message(message.from_user.id, "Это бот для поиска городов Подмосковья.\n"
                                                   "Есть команда /updateDB для обновления базы данных.\n"
                                                   "Можно ввести название города в Москве, "
                                                   "тогда я попробую найти его в базе")
        else:
            db_url_get = "http://localhost:8000/api/data/"
            db_data = requests.get(db_url_get, params={"name": message.text}).json()
            keyboard = telebot.types.InlineKeyboardMarkup()
            for data in db_data:
                button = telebot.types.InlineKeyboardButton(text=data["city_name"], callback_data=data["city_name"])
                keyboard.add(button)
            if len(db_data) == 0:
                bot.send_message(message.from_user.id, text='Увы, ничего не найдено, попробуй написать по-другому')
            else:
                bot.send_message(message.from_user.id, text='Выбери один из найденных пунктов', reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: True)
    def city_selector(call):
        db_url_get = "http://localhost:8000/api/data/"
        data_fetch = requests.get(db_url_get, params={"name": call.data}).json()[0]
        bot.send_message(call.message.chat.id, text=f'Выбранный пункт: {data_fetch["city_name"]}\n'
                                                    f'Население: {data_fetch["city_population"]} чел. \n'
                                                    f'Ссылка: {data_fetch["city_url"]}')

    bot.polling(none_stop=True, interval=0)
