import telebot
from telebot import types
from loguru import logger
from  threading import Thread
import os

# * config
ADMIN_ID = 5572914505
BOT_API_TOKEN = "7420625782:AAGkULTg5EgP1cFHZ0zT6zzj-pTwhxtPl-s"
logger.add("logs/tgbot.log", format="{time} - {level} - {message}", level="INFO", rotation="00:00")
logger.remove(0)
COMAND_LIST = ["help", "start", "q", "stop", ""]

# * global
stop = False

# * bot
bot = telebot.TeleBot(BOT_API_TOKEN)

@bot.message_handler(commands=["start", ])
def start(message: types.Message) -> None:
    
    logger.info(f"'{message.from_user.first_name}'|{message.chat.id} : {message.text}")
    bot.send_message(message.chat.id, "Привет! Я бот для чего-то. Пока просто разработка :)")


@bot.message_handler(commands=["q", ])
def q(message: types.Message) -> None:
    logger.info(f"'{message.from_user.first_name = }'/{message.chat.id = } :  {message.text = }")
    bot.send_message(ADMIN_ID, "I'm offline - by telegram")
    global stop
    stop = True

# * utils

def cheak_stop() -> None:
    while True:
        global stop
        if stop:
            global bot
            bot.send_message(ADMIN_ID, "I'm offline")
            return

def tgbot_console(cmd_list) -> None:
    global stop, tgbot_thread, bot
    while True:
        try:
            cmd = input("bot_console $ ")
            if cmd not in cmd_list:
                print("Command not found")
                continue
            
            if cmd == "help":
                print("Avaliable commands: ", *cmd_list, sep=" | ")
                continue
            if cmd == "q":
                bot.send_message(ADMIN_ID, "I'm offline - by console")
                stop = True
                break
            if cmd == "start":
                tgbot_thread.start()
                print(f"Bot has been successfully started: {tgbot_thread.is_alive() = }")
                continue
            if cmd == "stop":
                bot.stop_polling()
                print(f"Bot has been stopped: {tgbot_thread.is_alive() = }")
                continue

        except EOFError:
            stop = True
            print("\nGoodbye!\n")
            logger.info("Goodbye!")
            return       
            

# * threads
tgbot_thread = Thread(target=bot.infinity_polling, daemon=True)
tgbot_console_thread = Thread(target=tgbot_console, daemon=True, args=(COMAND_LIST,))
cheak_thread = Thread(target=cheak_stop, daemon=False)


# * main 

if __name__ == "__main__":
    os.system("cls")
    logger.info("Start programm")

    tgbot_console_thread.start()
    cheak_thread.start()

    cheak_thread.join()
    
    logger.info("Goodbye!")

