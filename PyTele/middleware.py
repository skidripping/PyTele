from telegram_wrapper.bot import bot

def use_middleware(middleware_func):
    bot.middleware.append(middleware_func)
