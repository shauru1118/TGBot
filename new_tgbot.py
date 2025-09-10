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
Пора зарегистрироваться! Напиши своё имя и профиль ('физ' или 'инф'), например:

Иван Иванов 
физ

Жду твои данные!

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
        msg = bot.send_message(message.chat.id, greeting(message.from_user.first_name))
        bot.register_next_step_handler(msg, register_user)

    def register_user(message : types.Message) -> None:
        args = list(map(lambda x: x.lower(), message.text.split("\n")))
        if len(args) != 2:
            msg = bot.send_message(message.chat.id, "Ошибка! Напиши своё имя и профиль ещё раз.")
            bot.register_next_step_handler(msg, register_user)
            return
        name, prof = args
        if prof not in ["физ", "инф"] or not name:
            msg = bot.send_message(message.chat.id, "Профиль должен быть 'физ' или 'инф'. Напиши своё имя и профиль ещё раз.")
            bot.register_next_step_handler(msg, register_user)
            return
        requests.post(f"https://shauru.pythonanywhere.com/add", json={"id": message.from_user.id,"name": name, "prof": prof})
        logger.info(f"message: {message.chat.id}|{message.from_user.username} : {message.text}")
        logger.info(f"new user: {name=}, {prof=}")
        bot.send_message(message.chat.id, "Вы успешно зарегистрировались в боте!")

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
        res = requests.get("https://shauru.pythonanywhere.com/get")
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
        res = requests.post(f"https://shauru.pythonanywhere.com/add?name={name}&prof={prof}")
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
