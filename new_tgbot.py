from telebot import TeleBot, types
from dotenv import load_dotenv
from loguru import logger
from time import strftime
import os

# ! tgbot class

class TGBot():
    def __init__(self, token : str, admin : int) -> None:
        self.token = token
        self.bot = TeleBot(token)
        self.running = False
        self.admin = admin
    
    def start(self) -> None:
        self.bot.remove_webhook()
        self.running = True
        logger.info(f"Bot has been successfully started: {self.running = }")
        self.bot.send_message(self.admin, "Bot has been successfully started")
    
        self.bot.polling(non_stop=True)

        self.bot.send_message(self.admin, "Bot has been successfully stopped")
        return
    
    def stop(self) -> None:
        self.bot.stop_polling()
        return
    
    def __str__(self) -> str:
        return f"bot running: {self.running}"


# ! main

def main():
    # ! env-VARS
    load_dotenv()

    TOKEN = str(os.getenv("TOKEN"))
    ADMIN = int(str(os.getenv("ADMIN")))
    
    # ! logger
    if not os.path.exists("logs"):
        os.mkdir("logs")
    logger.add(f"logs/tgbot_{strftime('%d-%m-%Y')}.log", format="{time} | {level} | {message}", level="INFO", rotation="00:00")
    # logger.remove(0)

    # ! telegram BOT
    admin_bot = TGBot(TOKEN, ADMIN)

    # # ! tgbot functions
    
    # !* start
    @admin_bot.bot.message_handler(commands=["start", ])
    def start(message: types.Message) -> None:
        
        logger.info(f"'{message.from_user.first_name}'|{message.chat.id} : {message.text}")
        admin_bot.bot.send_message(message.chat.id, "Привет! Я бот для чего-то. Пока просто разработка :)")
        return

    # !* q
    @admin_bot.bot.message_handler(commands=["q", ])
    def q(message: types.Message) -> None:
        
        logger.info(f"'{message.from_user.first_name}'|{message.chat.id} : {message.text}")
        admin_bot.bot.send_message(ADMIN, "I'm offline - by telegram")
        logger.info("I'm offline - by telegram\n\n")
        admin_bot.running = False
        admin_bot.stop()
        return
    
    # todo /status and /logs
    
    # !* logs - f"logs/tgbot_{strftime('%d-%m-%Y')}.log"
    
    # !* status - hz poka chto

    
    # * run
    admin_bot.start()
    


if __name__ == "__main__":
    main()



