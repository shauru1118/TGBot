from telebot import TeleBot

class TgBot(TeleBot):
    token : str
    main_admin : int
    admins : list[int]

    def __init__(self, _token, _main_admin, _admins):
        super().__init__(_token)
        self.token = _token
        self.main_admin = _main_admin
        self.admins = _admins
