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
        entry_points=[RegexHandler('^(RUN)$', menu, pass_user_data=True)],
        states={
            "choose": [MessageHandler(Filters.regex('^(Хочу бежать!)$'), next_menu, pass_user_data=True),
                       MessageHandler(Filters.regex('^(Статьи и материалы о беге)$'), get_article, pass_user_data=True),
                       MessageHandler(Filters.regex('^(Полезные youtube-каналы)$'), get_chanel, pass_user_data=True),
                       MessageHandler(Filters.regex('^(О боте и его создателях)$'), about, pass_user_data=True)],
            "race_world": [MessageHandler(Filters.regex('^(В России)$'), race_in_russia, pass_user_data=True),
                           MessageHandler(Filters.regex('^(За границей)$'), race_in_border, pass_user_data=True)],
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
    text = 'Ну что, как говорил Гагарин : "Побежали?"'
    my_keyboard = ReplyKeyboardMarkup([['RUN']], resize_keyboard=True)
    #print('Привет!')
    update.message.reply_text(text, reply_markup=my_keyboard, resize_keyboard=True)


def menu(bot, update, user_data):
    update.message.reply_text("Перед вами меню:", reply_markup=ReplyKeyboardRemove())
    button1 = KeyboardButton('Хочу бежать!')
    button2 = KeyboardButton('Статьи и материалы о беге')
    button3 = KeyboardButton('Полезные youtube-каналы')
    button4 = KeyboardButton('О боте и его создателях')
    kb = [[button1, button2],
          [button3, button4]]
    kb_markup = ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=False) 

    update.message.reply_text('Нажми на кнопку и будет результат!', reply_markup=kb_markup)
    return "choose"


def get_article(bot, update, user_data):
    articles = ["https://marathonec.ru/first-5-km/",
                "http://runninghero.ru/", "https://nogibogi.com/",
                "http://run-and-travel.com/", "https://stridemag.ru/",
                "https://www.mann-ivanov-ferber.ru/tag/run-books/"]
    for article in articles:          
        update.message.reply_text(article)


def get_chanel(bot, update, user_data):
    chanel_list = ["https://www.youtube.com/channel/UCN8-IYaiBH13zZ4uIRC2HKQ", 
                    "https://www.youtube.com/channel/UChlEGT8AuIStL6F9p1G4JPg",
                    "https://www.youtube.com/user/TREtherunexperience/featured",
                    "https://www.youtube.com/channel/UCYpnlxljje6xE_xFwe29LwA/featured"]
    for chanel in chanel_list:
        update.message.reply_text(chanel)


def about(bot, update, user_data): 
    text = ''' Этот бот был разработан в рамках сдачи проекта на курсе https://learn.python.ru/. Бот предлагает агрегированную информацию о забегах в рамках введенной даты. 
    Над ботом работали: Светлана @Demidenko_Svetlana   и Екатерина @marukova, а так же наш наставник и ментор - Собир.
    Ссылка на проект https://github.com/demidenko-svetlana/chat_bot_run .  '''
    update.message.reply_text(text)


def next_menu(bot, update, user_data):
    button_1 = KeyboardButton('В России')
    button_2 = KeyboardButton('За границей')
    keyboard = [[button_1, button_2]]
    m_keyboard = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True) 
    update.message.reply_text("Выбери,где хочешь бежать:", reply_markup=m_keyboard)
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
    country = 'За рубежом' if user_data['choosing_country'] == 'За границей' else 'Россия'
    print(country, date, "that's all")
    if date not in match:
        update.message.reply_text("Ты ввёл неправильную дату")
    else:
        events_list = event_date_country(date, country)
        events_names = " "
        for i in events_list:
            events_names = events_names + f' {i.date} Забег "{i.event}" в {i.places} на дистанцию {i.distance} по типу {i.race_type}. Подробности: {i.links} \n\n'

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
    return "choose"


def dontknow(bot, update, user_data):
    update.message.reply_text("Не понимаю", reply_markup=greet_user(bot, update))
    return ConversationHandler.END


main()
