from .bot import TelegramBot

class Command:
    def __init__(self, name):
        self.name = name

    def __call__(self, func):
        bot.commands[self.name] = func
        return func