from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, constants
import logging

from queries import event_date_country

import os
import re

from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
 

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def main():
    API_KEY = os.environ.get("API_KEY")    
    mybot = Updater(API_KEY, request_kwargs=PROXY) 
    dp = mybot.dispatcher

    race_in = ConversationHandler(
        entry_points=[RegexHandler('^(RUN)$', go_to_menu, pass_user_data=True)],
        states={
            "race_world": [MessageHandler(Filters.regex('^(Россия)$'), race_in_russia, pass_user_data=True),
                           MessageHandler(Filters.regex('^(Заграница)$'), race_in_border, pass_user_data=True)],
            "date_world": [MessageHandler(Filters.text, date_world, pass_user_data=True)],
        },
        fallbacks=[MessageHandler(
            Filters.text | Filters.video | Filters.photo | Filters.document, 
            dontknow, 
            pass_user_data=True
            )]
    )

    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(race_in)    


    mybot.start_polling() #проверка, есть ли что-то новое
    mybot.idle()


def greet_user(bot, update):
    my_keyboard = ReplyKeyboardMarkup([['RUN']])
    print('Привет!')
    update.message.reply_text('что-нибудь', reply_markup=my_keyboard, resize_keyboard=True)


def go_to_menu(bot, update, user_data):
    reply_keyboard = [["Россия"], ["Заграница"]]
    update.message.reply_text("Выбери где хочешь бежать", reply_markup=ReplyKeyboardMarkup(reply_keyboard), resize_keyboard=True)
    return "race_world"

def race_in_russia(bot, update, user_data):
    update.message.reply_text("Ты выбрал Россию. Укажи дату в формате «‎мм.гггг». Например: 04.2020", reply_markup=ReplyKeyboardRemove())
    user_data['choosing_country'] = update.message.text
    print(user_data['choosing_country'])
    return "date_world"

def race_in_border(bot, update, user_data):
    update.message.reply_text("Ты выбрал заграницу. Укажи дату в формате «‎мм.гггг». Например: 04.2020", reply_markup=ReplyKeyboardRemove())
    user_data['choosing_country'] = update.message.text
    print(user_data['choosing_country'])
    return "date_world"

def date_world(bot, update, user_data):
    date = update.message.text
    match = str(re.fullmatch(r'\d{2}\.\d{4}', date))
    country = 'За рубежом' if user_data['choosing_country'] == 'Заграница' else 'Россия'
    print(country, date, "that's all")
    if date not in match:
        update.message.reply_text("Ты ввёл неправильную дату")
    else:
        events_list = event_date_country(date, country)
        events_names = " "
        for i in events_list:
            events_names = events_names + f'Забег "{i.event}" в {i.places} на дистанцию {i.distance} по типу {i.race_type} проводится {i.date}. Подробности: {i.links} \n\n'

        if len(events_names) <= constants.MAX_MESSAGE_LENGTH:
            return update.message.reply_text(f"Забеги в месяце {date}:\n\n{events_names[:-2]}")
        
        parts = []
        while len(events_names) > 0:
            if len(events_names) > constants.MAX_MESSAGE_LENGTH:
                part = events_names[:constants.MAX_MESSAGE_LENGTH]
                first = part.rfind('\n')
                if first != -1:
                    parts.append(part[:first])
                    events_names = events_names[first:]
                else:
                    parts.append(part)
                    events_names = events_names[constants.MAX_MESSAGE_LENGTH:]
            else:
                parts.append(events_names)
                break
        print(parts)
        for part in parts:
            update.message.reply_text(f"Забеги в месяце {date}:\n\n{part}")
    return ConversationHandler.END
    

def dontknow(bot, update, user_data):
    update.message.reply_text("Не понимаю", reply_markup=greet_user(bot, update))
    return ConversationHandler.END

main()   