from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import logging

# from queries import event_location

import os

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
            "race_world": [RegexHandler('^(В России)$', race_in_russia, pass_user_data=True),
                           RegexHandler('^(Что есть за границей?)$', race_in_border, pass_user_data=True)],
            # "date_rus": [MessageHandler(Filters.text, available_date_rus, pass_user_data=True)]
        },
        fallbacks=[MessageHandler(
            Filters.text | Filters.video | Filters.photo | Filters.document, 
            dontknow, 
            pass_user_data=True
            )]
    )

    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(race_in)    

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling() #проверка, есть ли что-то новое
    mybot.idle()


# def greet_user(bot, update):
#     print('Вызван /start') 
#     print(update)


def greet_user(bot, update):
    text = 'Вызван /start'
    # print(text)
    my_keyboard = ReplyKeyboardMarkup([['RUN']])
    update.message.reply_text(text, reply_markup=my_keyboard)

def talk_to_me(bot, update):
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text)


def go_to_menu(bot, update, user_data):
    reply_keyboard = [["В России", "Что есть за границей?"]]
    update.message.reply_text("Выбери где хочешь бежать", reply_markup=ReplyKeyboardMarkup(reply_keyboard), resize_keyboard=True)
    return "race_world"

def race_in_russia(bot, update, user_data):
    update.message.reply_text("Ты выбрал Россию. Укажи дату в формате «‎мм.гггг». Например: 04.2020")
    user_choice = update.message.text
    update.message.reply_text(user_choice, reply_markup=ReplyKeyboardRemove())
    return "date_rus"

def race_in_border(bot, update, user_data):
    update.message.reply_text("Ты выбрал заграницу. Укажи дату в формате «‎мм.гггг». Например: 04.2020")
    user_choice1 = update.message.text
    update.message.reply_text(user_choice1, reply_markup=ReplyKeyboardRemove())
    return "date_b"

def available_date_rus(bot, update, user_data):
    date = update.message.text
    if len(date) != 7 :
        update.message.reply_text("Ты ввёл неправильную дату")
        return "date_rus"
    # else:
    #     update.message.reply_text("Вот что есть за этот месяц", event_location)
    #     return ConversationHandler.END

def dontknow(bot, update, user_data):
    update.message.reply_text("Не понимаю")


main()   