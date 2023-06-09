class InlineKeyboardMarkup:
    def __init__(self, inline_keyboard=None):
        self.inline_keyboard = inline_keyboard or []

    def add_row(self, row):
        self.inline_keyboard.append(row)

    def add_button(self, button, row_index=-1):
        if row_index < 0:
            row_index = len(self.inline_keyboard) + row_index
        if 0 <= row_index < len(self.inline_keyboard):
            self.inline_keyboard[row_index].append(button)

    def to_dict(self):
        return {
            'inline_keyboard': self.inline_keyboard
        }


class InlineKeyboardButton:
    def __init__(self, text, callback_data):
        self.text = text
        self.callback_data = callback_data

    def to_dict(self):
        return {
            'text': self.text,
            'callback_data': self.callback_data
        }