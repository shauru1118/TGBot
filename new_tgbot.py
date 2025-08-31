from telebot import TeleBot, types
from dotenv import load_dotenv
from loguru import logger
from time import strftime, sleep
import os
import requests
import schedule
import threading

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
        bot_discription = self.bot.get_me().to_json().replace("{", "{\n ").replace("}", "\n}").replace(",", ",\n")
        return bot_discription


class utils:
    @classmethod
    def today(cls) -> str:
        return strftime("%d-%m-%Y")
    
    @classmethod
    def log(cls, message : types.Message) -> str:
        return f"'{message.from_user.first_name}'|{message.chat.id} : {message.text}"
        
    @classmethod
    def get_rates(cls) -> dict:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        data = requests.get(url).json()["Valute"]

        rates = {
            "USD": f'{data["USD"]["Value"]:.2f}',
            "EUR": f'{data["EUR"]["Value"]:.2f}',
            "CNY": f'{data["CNY"]["Value"]:.2f}',
            "JPY": f'{data["JPY"]["Value"]/100:.2f}' ,  # у ЦБ курс за 100 иен
        }
        return rates

    @classmethod
    def send_message(cls, bot_, users: set) -> None:
        exchange_rate = ""
        valutes = cls.get_rates()
        for key, value in valutes.items():
            exchange_rate = exchange_rate + f"1 {key} : {value} руб.\n"
        
        for id in users:
            bot_.bot.send_message(id, exchange_rate)

    @classmethod
    def scheduler(cls, bot_, users: set):
        schedule.every().day.at("08:00").do(cls.send_message, bot_=bot_, users=users)
        while True:
            schedule.run_pending()
            sleep(1)


    
# ! main

def main():
    # ! env-VARS
    load_dotenv()

    TOKEN = str(os.getenv("TOKEN"))
    ADMIN = int(str(os.getenv("ADMIN")))
    
    # ! logger
    if not os.path.exists("logs"):
        os.mkdir("logs")
    logger.add(f"logs/tgbot_{utils.today()}.log", level="INFO", rotation="00:00")
    # logger.remove(0)

    # ! telegram BOT
    admin_bot = TGBot(TOKEN, ADMIN)

    # # ! tgbot functions
    
    # !* start
    @admin_bot.bot.message_handler(commands=["start", ])
    def start(message: types.Message) -> None:
        
        logger.info(utils.log(message))
        admin_bot.bot.send_message(message.chat.id, "Привет! Я бот для чего-то. Пока просто разработка :)")
        return

    # !* q
    @admin_bot.bot.message_handler(commands=["q", ])
    def q(message: types.Message) -> None:
        
        logger.info(utils.log(message))
        admin_bot.bot.send_message(ADMIN, "I'm offline - by telegram")
        logger.info("I'm offline - by telegram\n\n")
        admin_bot.running = False
        admin_bot.stop()
        return
    
    # !* logs
    @admin_bot.bot.message_handler(commands=["logs", ])
    def logs(message : types.Message) -> None:
        
        logger.info(utils.log(message))
        with open(f"logs/tgbot_{utils.today()}.log", "r") as f:
            logs_text = f.read()
        text_to_send = "```log\n" + logs_text + "\n```"
        admin_bot.bot.send_message(ADMIN, text_to_send, parse_mode="MarkdownV2")
        return
    
    # !* status
    @admin_bot.bot.message_handler(commands=["status", ])
    def status(message : types.Message) -> None:
        
        logger.info(utils.log(message))
        admin_bot.bot.send_message(ADMIN, "```json\n"+str(admin_bot)+"\n```", parse_mode="MarkdownV2")
        return
    
    # !* exchange rate
    @admin_bot.bot.message_handler(commands=["exchange_rate", ])
    def exchange_rate(message : types.Message) -> None:
        
        logger.info(utils.log(message))
        exchange_rate = ""
        valutes = utils.get_rates()
        for key, value in valutes.items():
            exchange_rate = exchange_rate + f"1 {key} : {value} руб.\n"
        
        admin_bot.bot.send_message(message.chat.id, exchange_rate)
        return
    
    users = set([ADMIN, 5207969556, 1301873508, -1002773279927])

    threading.Thread(target=utils.scheduler, daemon=True, kwargs={"bot_" : admin_bot, "users" : users}).start()

    # * run
    admin_bot.start()
    


if __name__ == "__main__":
    main()



