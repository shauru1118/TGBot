from telebot import types
from loguru import logger
import os, sys
import tgbot
from tgbot.tgbot import TgBot

TOKEN = "7420625782:AAGkULTg5EgP1cFHZ0zT6zzj-pTwhxtPl-s"
MAIN_ADMIN = 5572914505
ADMINS = [5572914505, ]
FORMAT_TO_LOGS = "{time}|{name} : <lvl>{message}</lvl>"
LOGGER_FILE = "logs/tgbot.log"
STOPPED_MESSAGE: types.Message | None = None


def greeting(name : str) -> str:
    return f"Hello, {name}! I'm a bot for admin your groups. I have many useful commands and funcs."

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
        logger.warning(f"message: {message.chat.id}|{message.from_user.username} : {message.text}")
        bot.send_message(message.chat.id, greeting(message.from_user.first_name))

    @bot.message_handler(commands=["q"])
    def q(message: types.Message):
        bot.send_message(bot.main_admin, "Bot : stop")
        global STOPPED_MESSAGE
        STOPPED_MESSAGE = message
        bot.stop_polling()

    @bot.message_handler(content_types=["text"])
    def echo(message: types.Message):
        bot.send_message(message.chat.id, "wtf?")

    global STOPPED_MESSAGE

    bot.remove_webhook()
    logger.success("Bot : start")
    bot.send_message(bot.main_admin, "Bot : start")
    bot.polling(non_stop=True)
    logger.warning(f"Bot : stop by telegram : {STOPPED_MESSAGE.chat.id}|{STOPPED_MESSAGE.from_user.username}")
    bot.send_message(bot.main_admin, f"Bot : stop by telegram : {STOPPED_MESSAGE.chat.id}|{STOPPED_MESSAGE.from_user.username}")
    logger.success(f"Bot : stop")

if __name__ == "__main__":
    main(sys.argv)
