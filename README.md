# PyTele

PyTele is a Python wrapper that simplifies interaction with the Telegram Bot API. It provides a set of classes and decorators for building Telegram bots more easily.

## File Structure

- `bot.py`: Contains the `TelegramBot` class, which serves as the main interface for interacting with the Telegram Bot API.
- `keyboard.py`: Defines the `InlineKeyboardMarkup` and `InlineKeyboardButton` classes used for creating inline keyboards.
- `buttons.py`: Defines the `Button` decorator for registering button handlers.
- `commands.py`: Defines the `Command` decorator for registering command handlers.
- `error_handler.py`: Defines the `error` function for registering an error handler.
- `events.py`: Defines the `Event` decorator for registering event handlers.
- `message_filters.py`: Contains utility functions for registering message filters.
- `middleware.py`: Contains utility functions for registering middleware functions.

## Usage Examples

### Sending a Message

```python
bot = TelegramBot('YOUR_BOT_TOKEN')
bot.send_message(chat_id, 'Hello, world!')
```

### Sending a Document

```python
bot.send_document(chat_id, document_path)
```

### Sending a Photo

```python
bot.send_photo(chat_id, photo_path, caption='Check out this photo!')
```

### Sending a Chat Action

```python
bot.send_chat_action(chat_id, 'typing')
```

### Editing a Message

```python
bot.edit_message_text(chat_id, message_id, 'Updated text')
```

### Registering a Command Handler

```python
@bot.command('/start')
def handle_start_command(chat_id, args):
    bot.send_message(chat_id, 'Welcome to the bot!')
```

### Registering an Event Handler

```python
@bot.event(lambda text: 'hello' in text.lower())
def handle_hello_event(chat_id):
    bot.send_message(chat_id, 'Hello there!')
```

### Registering a Button Handler

```python
@bot.button('Click Me')
def handle_button_click(chat_id):
    bot.send_message(chat_id, 'You clicked the button!')
```

### Registering an Error Handler

```python
def handle_error(error):
    print(f'An error occurred: {error}')

bot.error(handle_error)
```

### Registering a Message Filter

```python
@bot.message_filter(lambda update: update['message']['text'].startswith('Important'))
def handle_important_message(update):
    # Process the important message
    pass
```

### Registering Middleware

```python
def preprocess_update(update):
    # Perform preprocessing on the update
    return update

bot.use_middleware(preprocess_update)
```

### Running the Bot

```python
bot.run()
```

### Handling Bot Connections

```python
@bot.event(lambda text: text == 'connected')
def handle_bot_connected(chat_id):
    bot.send_message(chat_id, 'Bot connected to the server.')

@bot.event(lambda text: text == 'disconnected')
def handle_bot_disconnected(chat_id):
    bot.send_message(chat_id, 'Bot disconnected from the server')
```

These examples provide a basic understanding of how to use the `TelegramBot` class and the decorators/functions provided in the wrapper components.

Make sure to replace `'YOUR_BOT_TOKEN'` with your actual bot token in the `TelegramBot` initialization.

Please note that the usage examples assume you have imported the required components correctly and have the necessary setup (e.g., `chat_id`, file paths, etc.) in your code.