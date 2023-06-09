import requests
from .keyboard import InlineKeyboardButton, InlineKeyboardMarkup

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.base_url = f'https://api.telegram.org/bot{token}/'
        self.commands = {}
        self.events = {}
        self.buttons = {}
        self.message_filters = []
        self.error_handler = None
        self.middleware = []

    def send_message(self, chat_id, text, reply_markup=None):
        params = {'chat_id': chat_id, 'text': text}
        if reply_markup:
            params['reply_markup'] = reply_markup
        response = requests.get(self.base_url + 'sendMessage', params=params)
        return response.json()

    def edit_message_text(self, chat_id, message_id, text, reply_markup=None):
        params = {'chat_id': chat_id, 'message_id': message_id, 'text': text}
        if reply_markup:
            params['reply_markup'] = reply_markup
        response = requests.get(self.base_url + 'editMessageText', params=params)
        return response.json()

    def send_document(self, chat_id, document):
        files = {'document': document}
        response = requests.post(self.base_url + 'sendDocument', data={'chat_id': chat_id}, files=files)
        return response.json()
    
    def send_photo(self, chat_id, photo, caption=None, reply_markup=None):
        files = {'photo': photo}
        params = {'chat_id': chat_id}
        if caption:
            params['caption'] = caption
        if reply_markup:
            params['reply_markup'] = reply_markup
        response = requests.post(self.base_url + 'sendPhoto', data=params, files=files)
        return response.json()

    def send_chat_action(self, chat_id, action):
        params = {'chat_id': chat_id, 'action': action}
        response = requests.get(self.base_url + 'sendChatAction', params=params)
        return response.json()

    def process_update(self, update):
        message = update.get('message')
        callback_query = update.get('callback_query')

        if message:
            self.process_message(message)
        elif callback_query:
            self.process_callback_query(callback_query)

    def process_message(self, message):
        text = message.get('text')
        chat_id = message['chat']['id']

        if text.startswith('/'):
            self.process_command(chat_id, text)
        else:
            self.process_event(chat_id, text)

    def process_command(self, chat_id, text):
        command_parts = text.split(' ')
        command_name = command_parts[0]
        command_args = command_parts[1:]

        if command_name in self.commands:
            command_func = self.commands[command_name]
            command_func(chat_id, command_args)
        else:
            self.send_message(chat_id, 'Unknown command. Please try again.')

    def process_event(self, chat_id, text):
        print('Processing event:', text)  # Debug statement
        for event_filter, event_func in self.events.items():
            if event_filter(text):
                event_func(chat_id)

    def process_callback_query(self, callback_query):
        data = callback_query['data']
        chat_id = callback_query['message']['chat']['id']

        if data in self.buttons:
            button_func = self.buttons[data]
            button_func(chat_id)

    def command(self, name):
        def decorator(func):
            self.commands[name] = func
            return func

        return decorator

    def event(self, event_filter):
        def decorator(func):
            self.events[event_filter] = func
            return func

        return decorator

    def send_buttons(self, chat_id, text, buttons):
        keyboard = InlineKeyboardMarkup()
        for button_row in buttons:
            row = []
            for button_text, button_callback in button_row:
                button = InlineKeyboardButton(text=button_text, callback_data=button_callback)
                row.append(button)
            keyboard.add_row(*row)
        reply_markup = keyboard.to_dict()
        self.send_message(chat_id, text, reply_markup=reply_markup)
    
    def button(self, text):
        def decorator(func):
            if text not in self.buttons:
                self.buttons[text] = func
            return func

        return decorator

    def message_filter(self, filter_func):
        self.message_filters.append(filter_func)

    def error(self, error_handler):
        self.error_handler = error_handler

    def use_middleware(self, middleware_func):
        self.middleware.append(middleware_func)

    def handle_update(self, update):
        try:
            for middleware_func in self.middleware:
                update = middleware_func(update)

            for filter_func in self.message_filters:
                if filter_func(update):
                    self.process_update(update)
                    break
        except Exception as e:
            if self.error_handler:
                self.error_handler(e)

    def run(self):
        offset = None
        while True:
            updates = self.get_updates(offset)
            if updates:
                print('Received updates:', updates)  # Debug statement
                for update in updates:
                    self.handle_update(update)
                    offset = update['update_id'] + 1

    def get_updates(self, offset=None):
        params = {'timeout': 10, 'offset': offset}
        response = requests.get(self.base_url + 'getUpdates', params=params)
        return response.json()['result']