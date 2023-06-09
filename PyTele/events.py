from .bot import TelegramBot

class Event:
    def __init__(self, event_filter):
        self.event_filter = event_filter

    def __call__(self, func):
        bot.events[self.event_filter] = func
        return func