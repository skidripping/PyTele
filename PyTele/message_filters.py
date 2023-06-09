from telegram_wrapper.bot import bot

def message_filter(filter_func):
    bot.message_filters.append(filter_func)