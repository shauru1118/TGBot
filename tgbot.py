from telebot import TeleBot
from telebot import types
from loguru import logger
from moviepy import VideoFileClip
from  threading import Thread
from os import system
import os
from time import sleep
import subprocess

# * config
ADMIN_ID = 5572914505
BOT_API_TOKEN = "7420625782:AAGkULTg5EgP1cFHZ0zT6zzj-pTwhxtPl-s"
logger.add("logs/tgbot.log", format="{time} - {level} - {message}", level="INFO", rotation="00:00")
logger.remove(0)

# * global

running : bool = False
programm_running : bool = True
console_thread = None

# * bot
bot = TeleBot(BOT_API_TOKEN)

@bot.message_handler(commands=["start", ])
def start(message: types.Message) -> None:
    
    logger.info(f"'{message.from_user.first_name}'|{message.chat.id} : {message.text}")
    bot.send_message(message.chat.id, "Привет! Я бот для чего-то. Пока просто разработка :)")

@bot.message_handler(commands=["q", ])
def q(message: types.Message) -> None:
    
    logger.info(f"'{message.from_user.first_name}'|{message.chat.id} : {message.text}")
    bot.send_message(ADMIN_ID, "I'm offline - by telegram")
    print("\n\nI'm offline - by telegram\n\n")
    global programm_running
    programm_running = False

@bot.message_handler(commands=["status", ])
def status(message: types.Message) -> None:
    global running, programm_running
    logger.info(f"'{message.from_user.first_name}'|{message.chat.id} : {message.text}")
    bot.send_message(ADMIN_ID, f"{running = }\n{programm_running = }")

@bot.message_handler(content_types=["video", ])
def video(message: types.Message) -> None:
    try:
        logger.info(f"'{message.from_user.first_name}'|{message.chat.id} : {message.text}")
        bot.send_message(message.chat.id, "Превращаю видео в кружок...")
        
        width = message.video.width
        height = message.video.height
        size = message.video.file_size  # может быть None
        bot.send_message(ADMIN_ID, f"{message.chat.id} - {message.from_user.first_name}\n — размер: {width}×{height}\n — длина: {message.video.duration}с\n — файл: {f'{size/1024/1024:.2f}' or 'не указан'} мб")

        if size > 10 * 1024 * 1024:
            bot.send_message(message.chat.id, "Слишком большой размер видео :()")
            return
        videdo_info = bot.get_file(message.video.file_id)
        download_file = bot.download_file(videdo_info.file_path)
        if not os.path.exists("videos"):
            os.mkdir("videos")
        with open(f"videos/input_{message.chat.id}.mp4", "wb") as f:
            f.write(download_file)
        
        import test
        output_path = test.resize_video(message.chat.id)
        
        bot.send_video_note(message.chat.id, open(output_path, "rb"))
        bot.send_video_note(ADMIN_ID, open(output_path, "rb"), )
        bot.send_message(message.chat.id, "Video has been sent")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"Video has not been sent: {e}")
        bot.send_message(message.chat.id, f"Some error... ")
# * functions

# # * tgbot posibilities




# # * tgbot management
def run_tgbot() -> None:
    global bot, running
    
    running = True
    
    try:
        bot.remove_webhook()
        bot.polling(non_stop=True)
    except Exception as e:
        print("Бот не запущен:", e)
    finally:
        running = False

def start_tgbot() -> None:
    global running
    if running:
        print(f"Bot is already running: {running = }")
    else:
        thread = Thread(target=run_tgbot, daemon=True)
        thread.start()
        print(f"Bot has been successfully started: {thread.is_alive() = }")
    
    global console_thread
    if console_thread is None:
        tgbot_console(COMAND_DICT)
    return

def stop_tgbot() -> None:
    global running
    if not running:
        print(f"Bot is not running: {running = }")
    else:
        print(f"Bot stopping in progress...")
        bot.stop_polling()
        running = False
        print(f"Bot has been stopped: {running = }")
    return

# # * utils

def clear() -> None:
    system("clear" if os.name == "posix" else "cls")
    return


def cmd_help() -> None:
    print()
    for key, value in COMAND_DICT.items():
        print(f"\t{key:<10}  {value[0]}\n")
    return

def cmd_start() -> None:
    
    start_tgbot()
    return

def cmd_stop() -> None:
    stop_tgbot()
    return

def cmd_q() -> None:
    global programm_running, bot
    bot.send_message(ADMIN_ID, "\n\nI'm offline - by console\n\n")
    programm_running = False
    return

def tgbot_console(cmd_list : dict[str, (str, callable)]) -> None:
    
    global console_thread, programm_running
    def console() -> None:
        while programm_running:
            try:
                cmd = input("bot_console $ ")
                if cmd not in cmd_list:
                    print("Command not found")
                    continue
                
                cmd_list[cmd][1]()           

            except EOFError:
                print("\nGoodbye!\n")
                logger.info("Goodbye!")
                cmd_stop()
                return
    
    def check() -> None:
        while programm_running:
            pass
        return
    console_thread = Thread(target=console, daemon=True)
    console_thread.start()
    
    check_thread = Thread(target=check, daemon=False)
    check_thread.start()
    return
    
# * global 

COMAND_DICT : dict[str, (str, callable)] = {
    "help": ("show avaliable commands", cmd_help), 
    "start" : ("start telegram bot", cmd_start), 
    "q" : ("stop WHOLE program", cmd_q), 
    "stop" : ("stop telegram bot", cmd_stop), 
    "clear" : ("clear console", clear),
}


# * main

if __name__ == "__main__":
    
    if os.path.exists("logs"):
        pass
    else:
        os.mkdir("logs")
    
    clear()
    sleep(2)
    logger.info("Start programm")

    start_tgbot()
    logger.info(f"Bot has been successfully started: {running = }")
