from telegram_wrapper.bot import bot

def error(error_handler):
    bot.error_handler = error_handler
