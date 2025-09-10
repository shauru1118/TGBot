from math import inf
from telebot import types
from loguru import logger
import os, sys
from time import sleep
from tgbot import TgBot
from dotenv import load_dotenv
import requests
import json


load_dotenv()
TOKEN = str(os.getenv("TOKEN"))
MAIN_ADMIN = int(str(os.getenv("ADMIN")))
ADMINS = [MAIN_ADMIN, ]
LOGGER_FILE = "logs/tgbot.log"
STOPPED_MESSAGE: types.Message | None = None
PHIS_MATH = "phis"
INFO_MATH = "inf"


def greeting(name : str) -> str:
    return f"""

Привет, {name}! Я бот с домашними заданиями. 
Пора зарегистрироваться! Какой твой профиль?

"""


def main(args : list):
    # start
    logger.info("Starting program")
    logger.info(f"{args = }")

    # logs
    logger.warning("logs:")
    if not os.path.exists("logs"):
        os.mkdir("logs")
        logger.success("\tmade dir 'logs'")
    logger.add(LOGGER_FILE, level="INFO")
    logger.success(f"\tnew logger file '{LOGGER_FILE}'")

    bot = TgBot(TOKEN, MAIN_ADMIN, ADMINS)
    logger.success(f"new bot : TgBot - {bot=}")


    @bot.message_handler(commands=["start"])
    def start(message : types.Message):
        logger.info(f"message: {message.chat.id}|{message.from_user.username} : {message.text}")
        res = requests.get("https://shauru.pythonanywhere.com/api/get-users")
        if res.status_code != 200:
            bot.send_message(message.chat.id, f"Ошибка :( \nУже чиним!")
            bot.send_message(bot.main_admin, f"Error : ```\n{res.status_code}\n```\n```json\n{res.text}\n```\n", parse_mode="MarkdownV2")
            return
        users = res.json()
        if message.from_user.id in users or str(message.from_user.id) in users:
            bot.send_message(message.chat.id, "Вы уже зарегистрированы в боте!\nИспользуйте команду /help")
            return
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        phis_button = types.InlineKeyboardButton(text="Физика", callback_data="1")
        inf_button = types.InlineKeyboardButton(text="Информатика", callback_data="0")
        markup.add(phis_button, inf_button)
        bot.send_message(message.chat.id, greeting(message.from_user.first_name), reply_markup=markup)
    
    # register callback data
    @bot.callback_query_handler(func=lambda call: call.data in ["1", "0"])
    def register(call : types.CallbackQuery):
        logger.info(f"message: {call.from_user.id}|{call.from_user.username} : {call.data}")
        requests.post(f"https://shauru.pythonanywhere.com/api/add-user", json={"id": call.from_user.id, "prof": call.data})
        bot.answer_callback_query(callback_query_id=call.id, text="Вы успешно зарегистрировались в боте!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        bot.send_message(call.message.chat.id, "Успешная регистрация!\nИспользуйте команду /help")

    @bot.message_handler(commands=["help"])
    def help(message : types.Message):
        logger.info(f"message: {message.chat.id}|{message.from_user.username} : {message.text}")
        markup = types.InlineKeyboardMarkup(row_width=1)
        button = types.InlineKeyboardButton(text="Веб-приложение", web_app=types.WebAppInfo(url="https://shauru.pythonanywhere.com/"))
        markup.add(button)
        bot.send_message(message.chat.id, "Используйте Web-приложение для просмотра домашних заданий!"+
                        "\nЕсли есть вопросы или проблемы обращайтесь в поддержку /support",
                        reply_markup=markup)
        

    @bot.message_handler(commands=["support"])
    def support(message : types.Message):
        logger.info(f"message: {message.chat.id}|{message.from_user.username} : {message.text}")
        msg = bot.send_message(message.chat.id, "Опишите вашу проблему или вопрос, и мы ответим в ближайшее время!")
        bot.register_next_step_handler(msg, support_handler)

    def support_handler(message : types.Message):
        logger.info(f"message: {message.chat.id}|{message.from_user.username} : {message.text}")
        bot.send_message(message.chat.id, "Спасибо за обращение в поддержку! В скором времени мы ответим на ваш вопрос!")
        bot.send_message(bot.main_admin, f"SUPPORT\n\nПользователь @{message.from_user.username} :\n\n{message.text}")

    @bot.message_handler(commands=["q"])
    def q(message: types.Message):
        logger.info(f"message: {message.chat.id}|{message.from_user.username} : {message.text}")
        bot.send_message(bot.main_admin, "Bot : stop")
        global STOPPED_MESSAGE
        STOPPED_MESSAGE = message
        bot.stop_polling()

    @bot.message_handler(commands=["get_users"])
    def get_users(message : types.Message):
        logger.info(f"message: {message.chat.id}|{message.from_user.username} : {message.text}")
        if message.from_user.id != bot.main_admin:
            bot.send_message(message.chat.id, "not allowed")
            return
        res = requests.get("https://shauru.pythonanywhere.com/api/get-users")
        if res.status_code != 200:  
            bot.send_message(message.chat.id, f"Ошибка :( \nУже чиним!")
            bot.send_message(bot.main_admin, f"Error : ```\n{res.status_code}\n```\n```json\n{res.text}\n```\n", parse_mode="MarkdownV2")
            return
        bot.send_message(message.chat.id, f"\n```json\n{json.dumps(res.json(), indent=2, ensure_ascii=False)}\n```\n", parse_mode="MarkdownV2")

    @bot.message_handler(commands=["add_user"])
    def add_user(message : types.Message):
        logger.info(f"message: {message.chat.id}|{message.from_user.username} : {message.text}")
        if message.from_user.id != bot.main_admin:
            bot.send_message(message.chat.id, "not allowed")
        name, prof = message.text.split(" ")[1:]
        res = requests.post(f"https://shauru.pythonanywhere.com/api/add-user", json={"id": message.from_user.id, "prof": prof})
        bot.send_message(message.chat.id, f"```json\n{json.dumps(res.json(), indent=2, ensure_ascii=False)}\n```", parse_mode="MarkdownV2")

    @bot.message_handler(content_types=["text"])
    def echo(message: types.Message):
        logger.info(f"message: {message.chat.id}|{message.from_user.username} : {message.text}")

    global STOPPED_MESSAGE

    bot.remove_webhook()
    logger.success("Bot : start")
    bot.send_message(bot.main_admin, "Bot : start")
    while True:
        try:
            bot.polling(non_stop=True)
            if STOPPED_MESSAGE is not None:
                break
        except KeyboardInterrupt:
            break
        except:
            sleep(1)

    logger.warning(f"Bot : stop by telegram : {STOPPED_MESSAGE.chat.id}|{STOPPED_MESSAGE.from_user.username}")
    bot.send_message(bot.main_admin, f"Bot : stop by telegram : {STOPPED_MESSAGE.chat.id}|{STOPPED_MESSAGE.from_user.username}")
    logger.success(f"Bot : stop")

if __name__ == "__main__":
    main(sys.argv)
