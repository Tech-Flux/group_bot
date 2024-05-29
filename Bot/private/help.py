import telebot
from .commands import starter_help
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import Message
def send_help(message: Message, bot):
    markup = InlineKeyboardMarkup()

    # Create 20 inline buttons with custom labels
    buttons = [
        InlineKeyboardButton("Admin", callback_data="first_option"),
        InlineKeyboardButton("Second Option", callback_data="second_option"),
        InlineKeyboardButton("Third Option", callback_data="third_option"),
        InlineKeyboardButton("Fourth Option", callback_data="fourth_option"),
        InlineKeyboardButton("Fifth Option", callback_data="fifth_option"),
        InlineKeyboardButton("Sixth Option", callback_data="sixth_option"),
        InlineKeyboardButton("Seventh Option", callback_data="seventh_option"),
        InlineKeyboardButton("Eighth Option", callback_data="eighth_option"),
        InlineKeyboardButton("Ninth Option", callback_data="ninth_option"),
        InlineKeyboardButton("Tenth Option", callback_data="tenth_option"),
        InlineKeyboardButton("Eleventh Option", callback_data="eleventh_option"),
        InlineKeyboardButton("Twelfth Option", callback_data="twelfth_option"),
        InlineKeyboardButton("Thirteenth Option", callback_data="thirteenth_option"),
        InlineKeyboardButton("Fourteenth Option", callback_data="fourteenth_option"),
        InlineKeyboardButton("Fifteenth Option", callback_data="fifteenth_option"),
        InlineKeyboardButton("Sixteenth Option", callback_data="sixteenth_option"),
        InlineKeyboardButton("Seventeenth Option", callback_data="seventeenth_option"),
        InlineKeyboardButton("Eighteenth Option", callback_data="eighteenth_option")
    ]
    
    # Add buttons to the markup, 3 buttons per row
    for i in range(0, len(buttons), 3):
        if i + 2 < len(buttons):
            markup.row(buttons[i], buttons[i + 1], buttons[i + 2])
        elif i + 1 < len(buttons):
            markup.row(buttons[i], buttons[i + 1])
        else:
            markup.row(buttons[i])

    bot.send_message(message.chat.id, starter_help, reply_markup=markup)
