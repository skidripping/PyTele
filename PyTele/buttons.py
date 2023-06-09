from telegram_wrapper.bot import bot

class Button:
    def __init__(self, text):
        self.text = text

    def __call__(self, func):
        bot.buttons[self.text] = func
        return func