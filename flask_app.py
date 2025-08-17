# * importing

import telebot
from telebot import types
import flask

from  threading import Thread

# * config
BOT_API_TOKEN = "7420625782:AAGkULTg5EgP1cFHZ0zT6zzj-pTwhxtPl-s"

# * global
app = flask.Flask(__name__)
bot = telebot.TeleBot(BOT_API_TOKEN)

# * bot
@bot.message_handler(commands=["start", ])
def start(message: types.Message) -> None:
    bot.send_message(message.chat.id, "Привет! Я бот для чего-то. Пока просто разработка :)")


# * flask
@app.route("/")
def index() -> str:
    return "Hello World!"

if __name__ == "__main__":
    
    flask_thread = Thread(target=app.run)
    flask_thread.start()
    telegram_thread = Thread(target=bot.infinity_polling)
    telegram_thread.start()

