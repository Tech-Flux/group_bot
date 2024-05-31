import telebot
from .commands import starter_help
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import Message
def send_help(message: Message, bot):
    if message.chat.type != 'private':
        bot.reply_to(message, "Send this in pm for help!")
        return
        
    markup = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("Admin", callback_data="button_admins"),
        InlineKeyboardButton("Notes", callback_data="button_notes"),
        InlineKeyboardButton("Rules", callback_data="button_rules"),
        InlineKeyboardButton("Greetings", callback_data="button_greetings"),
        InlineKeyboardButton("Locks", callback_data="button_locks"),
        InlineKeyboardButton("Downloader", callback_data="button_downloads"),
        InlineKeyboardButton("Ai", callback_data="button_ai"),
        InlineKeyboardButton("Database", callback_data="button_db"),
        InlineKeyboardButton("Qur'an", callback_data="button_isl"),
        InlineKeyboardButton("Owner", callback_data="button_owner"),
        InlineKeyboardButton("Eleventh Option", callback_data="eleventh_option"),
        InlineKeyboardButton("Twelfth Option", callback_data="twelfth_option"),
        InlineKeyboardButton("Thirteenth Option", callback_data="thirteenth_option"),
        InlineKeyboardButton("Fourteenth Option", callback_data="fourteenth_option"),
        InlineKeyboardButton("Fifteenth Option", callback_data="fifteenth_option"),
        InlineKeyboardButton("Sixteenth Option", callback_data="sixteenth_option"),
        InlineKeyboardButton("Seventeenth Option", callback_data="seventeenth_option"),
        InlineKeyboardButton("Eighteenth Option", callback_data="eighteenth_option")
    ]

    for i in range(0, len(buttons), 3):
        if i + 2 < len(buttons):
            markup.row(buttons[i], buttons[i + 1], buttons[i + 2])
        elif i + 1 < len(buttons):
            markup.row(buttons[i], buttons[i + 1])
        else:
            markup.row(buttons[i])

    bot.send_message(message.chat.id, starter_help, reply_markup=markup)
